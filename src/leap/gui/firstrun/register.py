"""
Register User Page, used in First Run Wizard
"""
import logging


from PyQt4 import QtCore
from PyQt4 import QtGui

from leap.gui.firstrun.mixins import UserFormMixIn

logger = logging.getLogger(__name__)

from leap.gui.constants import APP_LOGO, BARE_USERNAME_REGEX
from leap.gui.styles import ErrorLabelStyleSheet


class RegisterUserPage(QtGui.QWizardPage, UserFormMixIn):

    setSigningUpStatus = QtCore.pyqtSignal([])

    def __init__(self, parent=None):

        super(RegisterUserPage, self).__init__(parent)

        # bind wizard page signals
        self.setSigningUpStatus.connect(
            lambda: self.set_validation_status(
                'validating'))

        self.setTitle("Sign Up")

        self.setPixmap(
            QtGui.QWizard.LogoPixmap,
            QtGui.QPixmap(APP_LOGO))

        userNameLabel = QtGui.QLabel("User &name:")
        userNameLineEdit = QtGui.QLineEdit()
        userNameLineEdit.cursorPositionChanged.connect(
            self.reset_validation_status)
        userNameLabel.setBuddy(userNameLineEdit)

        # let's add regex validator
        usernameRe = QtCore.QRegExp(BARE_USERNAME_REGEX)
        userNameLineEdit.setValidator(
            QtGui.QRegExpValidator(usernameRe, self))
        self.userNameLineEdit = userNameLineEdit

        userPasswordLabel = QtGui.QLabel("&Password:")
        self.userPasswordLineEdit = QtGui.QLineEdit()
        self.userPasswordLineEdit.setEchoMode(
            QtGui.QLineEdit.Password)
        userPasswordLabel.setBuddy(self.userPasswordLineEdit)

        userPassword2Label = QtGui.QLabel("Password (again):")
        self.userPassword2LineEdit = QtGui.QLineEdit()
        self.userPassword2LineEdit.setEchoMode(
            QtGui.QLineEdit.Password)
        userPassword2Label.setBuddy(self.userPassword2LineEdit)

        rememberPasswordCheckBox = QtGui.QCheckBox(
            "&Remember username and password.")
        rememberPasswordCheckBox.setChecked(True)

        self.registerField('userName*', self.userNameLineEdit)
        self.registerField('userPassword*', self.userPasswordLineEdit)

        # XXX missing password confirmation
        # XXX validator!

        self.registerField('rememberPassword', rememberPasswordCheckBox)

        layout = QtGui.QGridLayout()
        layout.setColumnMinimumWidth(0, 20)

        validationMsg = QtGui.QLabel("")
        validationMsg.setStyleSheet(ErrorLabelStyleSheet)

        self.validationMsg = validationMsg

        layout.addWidget(validationMsg, 0, 3)
        layout.addWidget(userNameLabel, 1, 0)
        layout.addWidget(self.userNameLineEdit, 1, 3)
        layout.addWidget(userPasswordLabel, 2, 0)
        layout.addWidget(userPassword2Label, 3, 0)
        layout.addWidget(self.userPasswordLineEdit, 2, 3)
        layout.addWidget(self.userPassword2LineEdit, 3, 3)
        layout.addWidget(rememberPasswordCheckBox, 4, 3, 4, 4)
        self.setLayout(layout)

    # overwritten methods

    def initializePage(self):
        """
        inits wizard page
        """
        provider = self.field('provider_domain')
        self.setSubTitle(
            "Register a new user with provider %s." %
            provider)
        self.validationMsg.setText('')
        self.userPassword2LineEdit.setText('')

    def validatePage(self):
        """
        we only pre-validate here password weakness
        stuff, or any other client side validation
        that we think of.
        real server validation is made on next page,
        and if any errors are thrown there we come back
        and re-display the validation label.
        """
        self.setSigningUpStatus.emit()

        #username = self.userNameLineEdit.text()
        password = self.userPasswordLineEdit.text()
        password2 = self.userPassword2LineEdit.text()

        # we better have here
        # some call to a password checker...
        # to assess strenght and avoid silly stuff.

        if password != password2:
            self.set_validation_status('Password does not match.')
            return False

        if len(password) < 6:
            self.set_validation_status('Password too short.')
            return False

        if password == "123456":
            # joking
            self.set_validation_status('Password too obvious.')
            return False

        return True

    def nextId(self):
        wizard = self.wizard()
        if not wizard:
            return
        return wizard.get_page_index('signupvalidation')
