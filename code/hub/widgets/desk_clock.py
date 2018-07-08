from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout


class DeskClock(QWidget):

    class Time(QLabel):
        def __init__(self, parent: QWidget):
            super().__init__(parent)
            self.setText('--:--')
            self.setAlignment(Qt.AlignVCenter)
            self.setObjectName('desk_clock_time')

    class Date(QWidget):

        def __init__(self, parent: QWidget):
            super().__init__(parent)
            layout = QVBoxLayout(self)

            self.today_day = QLabel('--', self)
            self.today_day.setObjectName('desk_clock_month')

            self.today_date = QLabel('--', self)
            self.today_date.setObjectName('desk_clock_date')

            layout.addWidget(self.today_day, alignment=Qt.AlignHCenter)
            layout.addWidget(self.today_date, alignment=Qt.AlignHCenter)

            self.setLayout(layout)

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.date_display = DeskClock.Date(self)
        self.time_display = DeskClock.Time(self)

        self.update_time()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        layout = QHBoxLayout(self)
        layout.setObjectName('desk_clock')

        layout.addWidget(self.date_display)
        layout.addWidget(self.time_display)

        self.setLayout(layout)

    def update_time(self):
        from time import strftime
        self.time_display.setText(strftime("%H:%M"))
        self.date_display.today_day.setText(strftime("%A"))
        self.date_display.today_date.setText(strftime("%B %-d %Y"))
