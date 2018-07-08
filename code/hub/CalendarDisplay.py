from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QSizePolicy, QSpacerItem, QGridLayout, QLayout, \
    QCalendarWidget, QMainWindow


class CalendarDisplay(QWidget):

    def __init__(self, parent: QMainWindow, object_name = "tab_calendar"):
        super().__init__(parent)
        self.setObjectName(object_name)

        self.setAutoFillBackground(True)

        layout = QGridLayout()
        layout.setSizeConstraint(QLayout.SetDefaultConstraint)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 0, 0)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 0)
        layout.addWidget(self.get_calendar_widget(), 1, 1)
        layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 1, 2)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding), 2, 1)

        self.setLayout(layout)

    def get_calendar_widget(self):
        calendar = QCalendarWidget()
        calendar.setEnabled(True)
        calendar.setFirstDayOfWeek(Qt.Monday)
        calendar.setDateEditEnabled(True)

        return calendar
