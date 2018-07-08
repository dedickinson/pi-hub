#!/usr/bin/env python
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from hub.HubUi import HubUiMainWindow

app = QApplication(sys.argv)
app.setAttribute(Qt.AA_EnableHighDpiScaling)
app.setAttribute(Qt.AA_UseHighDpiPixmaps)
app.setAttribute(Qt.AA_UseStyleSheetPropagationInWidgetStyles, True)

main_window = HubUiMainWindow()
main_window.display()
sys.exit(app.exec_())
