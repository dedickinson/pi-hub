from PyQt5.QtWidgets import QWidget, QSizePolicy, QSpacerItem, QGridLayout, QLayout, \
    QMainWindow, QVBoxLayout

from hub.widgets.desk_clock import DeskClock
from hub.widgets.weather import WeatherWidget


class HomeDisplay(QWidget):

    def __init__(self, parent: QMainWindow, object_name="tab_home"):
        super().__init__(parent)
        self.setObjectName(object_name)

        self.setAutoFillBackground(True)

        layout = QGridLayout()
        layout.setSizeConstraint(QLayout.SetMaximumSize)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding), 0, 0)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding), 1, 0)

        display_widget = QWidget(self)

        inner_layout = QVBoxLayout(self)
        inner_layout.addWidget(DeskClock(self))
        inner_layout.addWidget(WeatherWidget(self))
        display_widget.setLayout(inner_layout)

        layout.addWidget(display_widget, 1, 1)

        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Expanding), 1, 2)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Expanding, QSizePolicy.Expanding), 2, 1)

        self.setLayout(layout)