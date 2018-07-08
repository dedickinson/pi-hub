from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTabWidget, QMainWindow

from hub.CalendarDisplay import CalendarDisplay
from hub.HomeDisplay import HomeDisplay
from hub.HubConfig import HubConfig
from hub.TimerDisplay import TimerDisplay


class HubUi(QTabWidget):
    def __init__(self, parent: QMainWindow, config: HubConfig):
        super().__init__(parent)
        self.config = config

        self.setTabPosition(QTabWidget.South)

        self.addTab(HomeDisplay(parent=self), "Home")
        self.addTab(TimerDisplay(parent=self), "Forecast")
        self.addTab(TimerDisplay(parent=self), "Timers")
        self.addTab(CalendarDisplay(parent=self), "Calendar")

        self.setCurrentIndex(0)


class HubUiMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = HubConfig()

        with open(self.config.css_file, 'r') as f:
            self.setStyleSheet(f.read())

    def display(self) -> QWidget:
        hub = HubUi(self, self.config)
        self.setCentralWidget(hub)

        self.setWindowTitle(self.config.application_name)

        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.setAutoFillBackground(True)

        self.show()
        return self
