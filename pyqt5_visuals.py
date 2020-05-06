from covid19_data_fetch import fetch_data
from PyQt5.QtWidgets import QApplication, QGridLayout, QSizePolicy, QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPalette, QColor
from PyQt5.QtCore import Qt
from sys import argv, exit

class GraphArea(QWidget):

    def __init__(self, hcds, maximum_value, omitted, parent):
        super().__init__()

        self.left = 75
        self.top = 30
        self.width = 200
        self.height = 950

        self.hcds = hcds
        self.y_max = maximum_value
        self.x_omitted = omitted
        self.parent = parent


        self.init_background()

    def init_background(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("darkGray"))
        self.setPalette(palette)

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setPen(Qt.gray)
        y = 50
        while y <= self.y_max:
            paint.drawLine(0, y, 2000, y)
            y += self.y_max // 50

        y_multiplier = 0.4
        y0 = 940
        y_interval = self.parent.height // len(self.hcds[21].infected_cumulative)
        for hcd in self.hcds:
            i = 1
            x = 15
            for infected in hcd.infected_cumulative[self.x_omitted:]:
                paint.setPen(Qt.gray)
                paint.drawLine(x, 950, x, 0)
                x1 = x - 64
                y1 = y0 - (hcd.infected_cumulative[i - 1] * y_multiplier)
                x2 = x
                y2 = y0 - (hcd.infected_cumulative[i] * y_multiplier)
                paint.setPen(Qt.red)
                paint.drawLine(x1, y1, x2, y2)
                paint.drawEllipse(x2 - 2.5, y2 - 2.5, 5, 5)
                i += 1
                x += 64
        paint.end()
        # self.setUpdatesEnabled(False)

class DataArea(QWidget):

    def __init__(self):
        super().__init__()

        self.left = 75
        self.top = 30
        self.width = 2000
        self.height = 1000

        self.hcds, self.dates, self.maximum_value = fetch_data()
        self.no_of_y_labels = self.maximum_value // 50
        self.y_interval = self.height // self.no_of_y_labels
        print(self.y_interval, self.maximum_value)
        self.range_of_days = 30
        self.omitted = len(self.dates) - self.range_of_days
        self.dates = self.dates[self.omitted:]

        self.initUI()

    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()
        graph_area = GraphArea(self.hcds, self.maximum_value, self.omitted)
        graph_area.setFixedHeight(graph_area.height)
        layout.addWidget(graph_area, 0, 1, 1, -1)

        i = 0
        x = 1
        for infected in self.hcds[21].infected_cumulative[self.omitted:]:
            date_label = QLabel(str(self.dates[i].strftime("%m/%d")), self)
            layout.addWidget(date_label, 1, x)
            i += 1
            x += 1

        y = 0
        i = 1
        y0 = 900
        y_labels = QWidget()
        for i in range(0, self.no_of_y_labels):
            y += 50
            label_text = str(y)
            y_value = QLabel(label_text, y_labels)
            y_value.move(0, y0-(self.y_interval*i))
            print(y_value.height())
        layout.addWidget(y_labels, 0, 0)

        self.setLayout((layout))

        self.show()


class GraphViewer(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("nCoV-2019 infections in Finland")
        self.left = 75
        self.top = 30
        self.width = 2500
        self.height = 1280
        self.setGeometry(self.left, self.top, self.width, self.height)

        layout = QGridLayout()

        graph_area = DataArea()
        graph_area.setFixedHeight(graph_area.height)
        graph_area.setFixedWidth(graph_area.width)
        layout.addWidget(graph_area)

        widget = QWidget()
        widget.setLayout((layout))
        self.setCentralWidget((widget))

        self.show()


if __name__ == '__main__':
    app = QApplication(argv)
    ex = GraphViewer()
    exit(app.exec_())