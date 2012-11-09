"""
Generic error hierarchy
Leap/EIP exceptions used for exception handling,
logging, and notifying user of errors
during leap operation.

Exception hierarchy
-------------------
All EIP Errors must inherit from EIPClientError (note: move that to
a more generic LEAPClientBaseError).

Exception attributes and their meaning/uses
-------------------------------------------

* critical:    if True, will abort execution prematurely,
               after attempting any cleaning
               action.

* failfirst:   breaks any error_check loop that is examining
               the error queue.

* message:     the message that will be used in the __repr__ of the exception.

* usermessage: the message that will be passed to user in ErrorDialogs
               in Qt-land.

TODO:

* EIPClientError:
  Should inherit from LeapException

* gettext / i18n for user messages.

"""
from leap.base.exceptions import LeapException


# This should inherit from LeapException
class EIPClientError(Exception):
    """
    base EIPClient exception
    """
    critical = False
    failfirst = False
    warning = False


class CriticalError(EIPClientError):
    """
    we cannot do anything about it, sorry
    """
    critical = True
    failfirst = True


class Warning(EIPClientError):
    """
    just that, warnings
    """
    warning = True


class EIPNoPolkitAuthAgentAvailable(CriticalError):
    message = "No polkit authentication agent could be found"
    usermessage = ("We could not find any authentication "
                   "agent in your system.<br/>"
                   "Make sure you have "
                   "<b>polkit-gnome-authentication-agent-1</b> "
                   "running and try again.")


class EIPNoPkexecAvailable(Warning):
    message = "No pkexec binary found"
    usermessage = ("We could not find <b>pkexec</b> in your "
                   "system.<br/> Do you want to try "
                   "<b>setuid workaround</b>? "
                   "(<i>DOES NOTHING YET</i>)")
    failfirst = True


class EIPNoCommandError(EIPClientError):
    message = "no suitable openvpn command found"
    usermessage = ("No suitable openvpn command found. "
                   "<br/>(Might be a permissions problem)")


class EIPBadCertError(Warning):
    # XXX this should be critical and fail close
    message = "cert verification failed"
    usermessage = "there is a problem with provider certificate"


class LeapBadConfigFetchedError(Warning):
    message = "provider sent a malformed json file"
    usermessage = "an error occurred during configuratio of leap services"


class OpenVPNAlreadyRunning(EIPClientError):
    message = "Another OpenVPN Process is already running."
    usermessage = ("Another OpenVPN Process has been detected."
                   "Please close it before starting leap-client")


class HttpsNotSupported(LeapException):
    message = "connection refused while accessing via https"
    usermessage = "Server does not allow secure connections."


class HttpsBadCertError(LeapException):
    message = "verification error on cert"
    usermessage = "Server certificate could not be verified."

#
# errors still needing some love
#


class EIPInitNoKeyFileError(CriticalError):
    message = "No vpn keys found in the expected path"
    usermessage = "We could not find your eip certs in the expected path"


class EIPInitBadKeyFilePermError(Warning):
    # I don't know if we should be telling user or not,
    # we try to fix permissions and should only re-raise
    # if permission check failed.
    pass


class EIPInitNoProviderError(EIPClientError):
    pass


class EIPInitBadProviderError(EIPClientError):
    pass


class EIPConfigurationError(EIPClientError):
    pass

#
# Errors that probably we don't need anymore
# chase down for them and check.
#


class MissingSocketError(Exception):
    pass


class ConnectionRefusedError(Exception):
    pass


class EIPMissingDefaultProvider(Exception):
    pass
