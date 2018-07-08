from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPalette, QColor, QBrush


class HubConfig:
    def __init__(self, config_file = ""):
        self.application_name = "HUB"
        self.css_file = 'hub/default.css'
        #self.font_base_family = "IBM Plex Sans"

        #self.window_size = QSize(800, 480)
