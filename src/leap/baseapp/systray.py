import logging

from PyQt4 import QtCore
from PyQt4 import QtGui

from leap import __branding as BRANDING
from leap import __version__ as VERSION

from leap.gui import mainwindow_rc

logger = logging.getLogger(__name__)


class StatusAwareTrayIconMixin(object):
    """
    a mix of several functions needed
    to create a systray and make it
    get updated from conductor status
    polling.
    """
    states = {
        "disconnected": 0,
        "connecting": 1,
        "connected": 2}

    iconpath = {
        "disconnected": ':/images/conn_error.png',
        "connecting": ':/images/conn_connecting.png',
        "connected": ':/images/conn_connected.png'}

    Icons = {
        'disconnected': lambda self: QtGui.QIcon(
            self.iconpath['disconnected']),
        'connecting': lambda self: QtGui.QIcon(
            self.iconpath['connecting']),
        'connected': lambda self: QtGui.QIcon(
            self.iconpath['connected'])
    }

    def __init__(self, *args, **kwargs):
        self.createIconGroupBox()
        self.createActions()
        self.createTrayIcon()
        #logger.debug('showing tray icon................')
        self.trayIcon.show()

        # not sure if this really belongs here, but...
        self.timer = QtCore.QTimer()

    def createIconGroupBox(self):
        """
        dummy icongroupbox
        (to be removed from here -- reference only)
        """
        con_widgets = {
            'disconnected': QtGui.QLabel(),
            'connecting': QtGui.QLabel(),
            'connected': QtGui.QLabel(),
        }
        con_widgets['disconnected'].setPixmap(
            QtGui.QPixmap(
                self.iconpath['disconnected']))
        con_widgets['connecting'].setPixmap(
            QtGui.QPixmap(
                self.iconpath['connecting']))
        con_widgets['connected'].setPixmap(
            QtGui.QPixmap(
                self.iconpath['connected'])),
        self.ConnectionWidgets = con_widgets

        self.statusIconBox = QtGui.QGroupBox("EIP Connection Status")
        statusIconLayout = QtGui.QHBoxLayout()
        statusIconLayout.addWidget(self.ConnectionWidgets['disconnected'])
        statusIconLayout.addWidget(self.ConnectionWidgets['connecting'])
        statusIconLayout.addWidget(self.ConnectionWidgets['connected'])
        statusIconLayout.itemAt(1).widget().hide()
        statusIconLayout.itemAt(2).widget().hide()

        self.leapConnStatus = QtGui.QLabel("<b>disconnected</b>")
        statusIconLayout.addWidget(self.leapConnStatus)

        self.statusIconBox.setLayout(statusIconLayout)

    def createTrayIcon(self):
        """
        creates the tray icon
        """
        self.trayIconMenu = QtGui.QMenu(self)

        self.trayIconMenu.addAction(self.connAct)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.detailsAct)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.aboutAct)
        self.trayIconMenu.addAction(self.aboutQtAct)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.setIcon('disconnected')
        self.trayIcon.setContextMenu(self.trayIconMenu)

        #self.trayIconMenu.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.trayIconMenu.customContextMenuRequested.connect(
            #self.on_context_menu)

    def bad(self):
        logger.error('this should not be called')

    def createActions(self):
        """
        creates actions to be binded to tray icon
        """
        # XXX change action name on (dis)connect
        self.connAct = QtGui.QAction(self.tr("Encryption ON     turn &off"), self,
                                     triggered=lambda: self.start_or_stopVPN())

        self.detailsAct = QtGui.QAction(self.tr("&Details..."),
                                        self,
                                        triggered=self.detailsWin)
        #self.minimizeAction = QtGui.QAction("Mi&nimize", self,
                                            #triggered=self.hide)
        #self.maximizeAction = QtGui.QAction("Ma&ximize", self,
                                            #triggered=self.showMaximized)
        #self.restoreAction = QtGui.QAction("&Restore", self,
                                           #triggered=self.showNormal)
        self.aboutAct = QtGui.QAction(self.tr("&About"), self,
                                      triggered=self.about)
        self.aboutQtAct = QtGui.QAction(self.tr("About Q&t"), self,
                                        triggered=QtGui.qApp.aboutQt)
        self.quitAction = QtGui.QAction(self.tr("&Quit"), self,
                                        triggered=self.cleanupAndQuit)

    def toggleEIPAct(self):
        # this is too simple by now.
        # XXX We need to get the REAL info for Encryption state.
        # (now is ON as soon as vpn launched)
        if self.eip_service_started is True:
            self.connAct.setText(self.tr('Encryption ON    turn o&ff'))
        else:
            self.connAct.setText(self.tr('Encryption OFF   turn &on'))

    def detailsWin(self):
        visible = self.isVisible()
        if visible:
            self.hide()
        else:
            self.show()

    def about(self):
        # move to widget
        flavor = BRANDING.get('short_name', None)
        content = ("LEAP client<br>"
                   "(version <b>%s</b>)<br>" % VERSION)
        if flavor:
            content = content + ('<br>Flavor: <i>%s</i><br>' % flavor)
        content = content + (
            "<br><a href='https://leap.se/'>"
            "https://leap.se</a>")
        QtGui.QMessageBox.about(self, self.tr("About"), self.tr(content))
        import pdb4qt as pdb; pdb.set_trace()

    def setConnWidget(self, icon_name):
        oldlayout = self.statusIconBox.layout()

        for i in range(3):
            oldlayout.itemAt(i).widget().hide()
        new = self.states[icon_name]
        oldlayout.itemAt(new).widget().show()

    def setIcon(self, name):
        icon_fun = self.Icons.get(name)
        if icon_fun and callable(icon_fun):
            icon = icon_fun(self)
            self.trayIcon.setIcon(icon)

    def getIcon(self, icon_name):
        return self.states.get(icon_name, None)

    def setIconToolTip(self):
        """
        get readable status and place it on systray tooltip
        """
        status = self.conductor.status.get_readable_status()
        self.trayIcon.setToolTip(status)

    def iconActivated(self, reason):
        """
        handles left click, left double click
        showing the trayicon menu
        """
        if reason in (QtGui.QSystemTrayIcon.Trigger,
                      QtGui.QSystemTrayIcon.DoubleClick):
            context_menu = self.trayIcon.contextMenu()
            # for some reason, context_menu.show()
            # is failing in a way beyond my understanding.
            # (not working the first time it's clicked).
            # this works however.
            context_menu.exec_(self.trayIcon.geometry().center())

    @QtCore.pyqtSlot()
    def onTimerTick(self):
        self.statusUpdate()

    @QtCore.pyqtSlot(object)
    def onStatusChange(self, status):
        """
        updates icon
        """
        icon_name = self.conductor.get_icon_name()

        # XXX refactor. Use QStateMachine

        if icon_name in ("disconnected", "connected"):
            self.changeLeapStatus.emit(icon_name)

        if icon_name in ("connecting"):
            # let's see how it matches
            leap_status_name = self.conductor.get_leap_status()
            self.changeLeapStatus.emit(leap_status_name)

        self.setIcon(icon_name)
        # change connection pixmap widget
        self.setConnWidget(icon_name)

    @QtCore.pyqtSlot(str)
    def onChangeLeapConnStatus(self, newstatus):
        """
        slot for LEAP status changes
        not to be confused with onStatusChange.
        this only updates the non-debug LEAP Status line
        next to the connection icon.
        """
        # XXX move bold to style sheet
        self.leapConnStatus.setText(
            "<b>%s</b>" % newstatus)
