from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTabWidget, QMainWindow

from .displays import *

class HubConfig:
    from PyQt5.QtCore import QSize, Qt
    from PyQt5.QtGui import QFont, QPalette, QColor, QBrush

    def __init__(self, config_file = ""):
        self.application_name = "HUB"
        self.css_file = 'hub/default.css'
        #self.font_base_family = "IBM Plex Sans"
        #self.window_size = QSize(800, 480)


class HubUi(QTabWidget):

    def __init__(self, parent: QMainWindow, config: HubConfig):

        super().__init__(parent)
        self.config = config

        self.setTabPosition(QTabWidget.South)

        #self.addTab(HomeDisplay(parent=self), "Home")
        #self.addTab(TimerDisplay(parent=self), "Timers")
        #self.addTab(CalendarDisplay(parent=self), "Calendar")

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


def main(args):
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QApplication
    
    app = QApplication(args)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app.setAttribute(Qt.AA_UseStyleSheetPropagationInWidgetStyles, True)

    main_window = HubUiMainWindow()
    main_window.display()

    sys.exit(app.exec_())


if __name__ == '__main__':
    import sys

    main(sys.argv)
