import logging
import os
import platform
import tempfile

from leap import __branding as BRANDING
from leap import certs
from leap.util.fileutil import (which, mkdir_p, check_and_fix_urw_only)

from leap.base import config as baseconfig
from leap.baseapp.permcheck import (is_pkexec_in_system,
                                    is_auth_agent_running)
from leap.eip import exceptions as eip_exceptions
from leap.eip import specs as eipspecs

logger = logging.getLogger(name=__name__)
provider_ca_file = BRANDING.get('provider_ca_file', None)


class EIPConfig(baseconfig.JSONLeapConfig):
    spec = eipspecs.eipconfig_spec

    def _get_slug(self):
        eipjsonpath = baseconfig.get_config_file(
            'eip.json')
        return eipjsonpath

    def _set_slug(self, *args, **kwargs):
        raise AttributeError("you cannot set slug")

    slug = property(_get_slug, _set_slug)


class EIPServiceConfig(baseconfig.JSONLeapConfig):
    spec = eipspecs.eipservice_config_spec

    def _get_slug(self):
        return baseconfig.get_config_file(
            'eip-service.json',
            folder=baseconfig.get_default_provider_path())

    def _set_slug(self):
        raise AttributeError("you cannot set slug")

    slug = property(_get_slug, _set_slug)


def get_socket_path():
    socket_path = os.path.join(
        tempfile.mkdtemp(prefix="leap-tmp"),
        'openvpn.socket')
    logger.debug('socket path: %s', socket_path)
    return socket_path


def get_eip_gateway():
    """
    return the first host in eip service config
    that matches the name defined in the eip.json config
    file.
    """
    placeholder = "testprovider.example.org"
    eipconfig = EIPConfig()
    #import ipdb;ipdb.set_trace()
    eipconfig.load()
    conf = eipconfig.config

    primary_gateway = conf.get('primary_gateway', None)
    if not primary_gateway:
        return placeholder

    eipserviceconfig = EIPServiceConfig()
    eipserviceconfig.load()
    eipsconf = eipserviceconfig.get_config()
    gateways = eipsconf.get('gateways', None)
    if not gateways:
        logger.error('missing gateways in eip service config')
        return placeholder
    if len(gateways) > 0:
        for gw in gateways:
            name = gw.get('name', None)
            if not name:
                return

            if name == primary_gateway:
                hosts = gw.get('hosts', None)
                if not hosts:
                    logger.error('no hosts')
                    return
                if len(hosts) > 0:
                    return hosts[0]
                else:
                    logger.error('no hosts')
    logger.error('could not find primary gateway in provider'
                 'gateway list')


def build_ovpn_options(daemon=False, socket_path=None, **kwargs):
    """
    build a list of options
    to be passed in the
    openvpn invocation
    @rtype: list
    @rparam: options
    """
    # XXX review which of the
    # options we don't need.

    # TODO pass also the config file,
    # since we will need to take some
    # things from there if present.

    provider = kwargs.pop('provider', None)

    # get user/group name
    # also from config.
    user = baseconfig.get_username()
    group = baseconfig.get_groupname()

    opts = []

    opts.append('--client')

    opts.append('--dev')
    # XXX same in win?
    opts.append('tun')
    opts.append('--persist-tun')
    opts.append('--persist-key')

    verbosity = kwargs.get('ovpn_verbosity', None)
    if verbosity and 1 <= verbosity <= 6:
        opts.append('--verb')
        opts.append("%s" % verbosity)

    # remote
    opts.append('--remote')
    gw = get_eip_gateway()
    logger.debug('setting eip gateway to %s', gw)
    opts.append(str(gw))
    opts.append('1194')
    #opts.append('80')
    opts.append('udp')

    opts.append('--tls-client')
    opts.append('--remote-cert-tls')
    opts.append('server')

    # set user and group
    opts.append('--user')
    opts.append('%s' % user)
    opts.append('--group')
    opts.append('%s' % group)

    opts.append('--management-client-user')
    opts.append('%s' % user)
    opts.append('--management-signal')

    # set default options for management
    # interface. unix sockets or telnet interface for win.
    # XXX take them from the config object.

    ourplatform = platform.system()
    if ourplatform in ("Linux", "Mac"):
        opts.append('--management')

        if socket_path is None:
            socket_path = get_socket_path()
        opts.append(socket_path)
        opts.append('unix')

    if ourplatform == "Windows":
        opts.append('--management')
        opts.append('localhost')
        # XXX which is a good choice?
        opts.append('7777')

    # certs
    client_cert_path = eipspecs.client_cert_path(provider)
    ca_cert_path = eipspecs.provider_ca_path(provider)

    opts.append('--cert')
    opts.append(client_cert_path)
    opts.append('--key')
    opts.append(client_cert_path)
    opts.append('--ca')
    opts.append(ca_cert_path)

    # we cannot run in daemon mode
    # with the current subp setting.
    # see: https://leap.se/code/issues/383
    #if daemon is True:
        #opts.append('--daemon')

    logger.debug('vpn options: %s', opts)
    return opts


def build_ovpn_command(debug=False, do_pkexec_check=True, vpnbin=None,
                       socket_path=None, **kwargs):
    """
    build a string with the
    complete openvpn invocation

    @rtype [string, [list of strings]]
    @rparam: a list containing the command string
        and a list of options.
    """
    command = []
    use_pkexec = True
    ovpn = None

    # XXX get use_pkexec from config instead.

    if platform.system() == "Linux" and use_pkexec and do_pkexec_check:

        # check for both pkexec
        # AND a suitable authentication
        # agent running.
        logger.info('use_pkexec set to True')

        if not is_pkexec_in_system():
            logger.error('no pkexec in system')
            raise eip_exceptions.EIPNoPkexecAvailable

        if not is_auth_agent_running():
            logger.warning(
                "no polkit auth agent found. "
                "pkexec will use its own text "
                "based authentication agent. "
                "that's probably a bad idea")
            raise eip_exceptions.EIPNoPolkitAuthAgentAvailable

        command.append('pkexec')
    if vpnbin is None:
        ovpn = which('openvpn')
    else:
        ovpn = vpnbin
    if ovpn:
        vpn_command = ovpn
    else:
        vpn_command = "openvpn"
    command.append(vpn_command)
    daemon_mode = not debug

    for opt in build_ovpn_options(daemon=daemon_mode, socket_path=socket_path,
                                  **kwargs):
        command.append(opt)

    # XXX check len and raise proper error

    return [command[0], command[1:]]


def check_vpn_keys(provider=None):
    """
    performs an existance and permission check
    over the openvpn keys file.
    Currently we're expecting a single file
    per provider, containing the CA cert,
    the provider key, and our client certificate
    """
    assert provider is not None
    provider_ca = eipspecs.provider_ca_path(provider)
    client_cert = eipspecs.client_cert_path(provider)

    logger.debug('provider ca = %s', provider_ca)
    logger.debug('client cert = %s', client_cert)

    # if no keys, raise error.
    # it's catched by the ui and signal user.

    if not os.path.isfile(provider_ca):
        # not there. let's try to copy.
        folder, filename = os.path.split(provider_ca)
        if not os.path.isdir(folder):
            mkdir_p(folder)
        if provider_ca_file:
            cacert = certs.where(provider_ca_file)
        with open(provider_ca, 'w') as pca:
            with open(cacert, 'r') as cac:
                pca.write(cac.read())

    if not os.path.isfile(provider_ca):
        logger.error('key file %s not found. aborting.',
                     provider_ca)
        raise eip_exceptions.EIPInitNoKeyFileError

    if not os.path.isfile(client_cert):
        logger.error('key file %s not found. aborting.',
                     client_cert)
        raise eip_exceptions.EIPInitNoKeyFileError

    for keyfile in (provider_ca, client_cert):
        # bad perms? try to fix them
        try:
            check_and_fix_urw_only(keyfile)
        except OSError:
            raise eip_exceptions.EIPInitBadKeyFilePermError
