==================================
User-facing changes in Leap Client
==================================

Release 0.2.0 (2012-10-XX)
--------------------------

This release is a functionally working version in Debian Squeeze and Ubuntu 12.04.
It is able to connect to a preconfigured leap provider and autoconfigures a EIP connection.

Python Support
''''''''''''''
This release supports Python2.6 and Python2.7

New Features
''''''''''''
- Branded build: the final package includes branding info needed to connect to a default provider. 
- First run wizard: allows to register an user with the selected provider. It also downloads all
  the config files needed to connect to the eip service on this provider.
- Network checks: we do some basic network testing and warn user in case we cannot find a
  suitable network interface, or if the virtual interface dissapears after a successful eip connection.
- Debug mode and logfiles: the leap-client script allows to be invoked with the --debug flag.
  It also accepts a --logfile option that is useful for documenting bug reports.

Dependencies
''''''''''''
See the ``README.rst`` for a step-to-step install guide.

The following libraries are needed:

- PyQt4
- libgnutls
- openvpn

for building the package dependencies, you will need also:

- python-setuptools
- python-dev
- libgnutls-dev

Leap-Client depends on the following python packages:

- requests
- ping
- psutil
- netifaces
- jsonschema
- srp
- pycrypto
- keyring
- python-gnutls==1.1.9

We are freezing the python-gnutls library dependency for this release due to a bug in ubuntu, see:
https://bugs.launchpad.net/ubuntu/+source/python-gnutls/+bug/1027129


Configuration files
'''''''''''''''''''

Config files are created under ``~/.config/leap``
Currently user should be able to completely remove this folder and have it auto-generated in the first run.

- Current eip service config is stored in ``eip.json``
- Under ``.config/leap/providers``, there is a per-provider folder that contains:
  - ``provider.json``, with all options for connecting to this provider.
  - ``eip-service.json``, with eip-specific configuration options,
  - ``keys/ca``, for a copy of the ca certificates used in the tls connections to provider.
  - ``keys/client``, for a local copy of leap user certificates used in the eip connection.
- ``leap.conf`` for general application configurations (gui windows geometry, ...).
