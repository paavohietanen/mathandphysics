from math import sin, cos, sqrt, log, pi
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from random import random as rand
from sys import argv, exit
from probability_functions import mean, variance, standard_deviation, find_min_and_max, fx_gaussian_psd,\
     distribution_around_center


def box_muller():
    u1 = rand()
    u2 = rand()
    z0 = sqrt(-2*log(u1))*cos(2*pi*u2)
    z1 = sqrt(-2*log(u1))*sin(2*pi*u2)
    return z0, z1


def generate_gaussian_data(n):
    data = []
    for i in range(1, n):
        x1, x2 = box_muller()
        data.append(x1)
    return data


def generate_pseudo_random_data(n):
    data = []
    biggest = 0
    smallest = 100000
    for i in range(1, n):
        a, b, c, d = rand(), rand(), rand(), rand()
        if rand() > 0.1:
            a *= -1
        if rand() > 0.1:
            b *= -1
        if rand() > 0.5:
            c *= -1
        if rand() > 0.9999:
            d *= -1
        x1 = (a+b+c+d)
        if x1 < smallest:
            smallest = x1
        if x1 > biggest:
            biggest = x1
        data.append(x1)
    print("SMALLEST ", smallest, "BIGGEST ", biggest)
    return data

class App(QWidget):

    def __init__(self):
        super().__init__()

        self.title = "Curve from function using Python's PRNG"
        self.left = 75
        self.top = 30
        self.width = 600
        self.height = 400
        self.initUI()

        # Initiating general painting tools
        self.x0 = (self.width / 2)
        self.y0 = (self.height / 2) + 100
        self.scale_multiplier_x = 40
        self.scale_multiplier_y = -400

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)
        paint.setPen(Qt.red)

        # Generate 10000 random Gaussian[?] values
        gaussian_data_points = generate_pseudo_random_data(100000)#generate_gaussian_data(10000)#mu, sigma, 10000)

        # Calculate "standard deviation"
        sigma = standard_deviation(gaussian_data_points, sample=True)
        print("Sigma is ", sigma)

        # Calculate "mean"
        mu = mean(gaussian_data_points)
        print("Mu is ", mu)

        # Find minimum and maximum as well as number of data points less and more than mu
        minimum, maximum = find_min_and_max(gaussian_data_points)
        lt_mu, gt_mu = distribution_around_center(gaussian_data_points, mu)
        print("Minimum: ", minimum, " Maximum: ", maximum)

        # Map to Gaussian PSD
        self.draw_gaussian_psd(paint, gaussian_data_points, mu, sigma)

        # Draw some key indicators to PSD
        self.draw_key_points(paint, minimum, maximum, mu, lt_mu, gt_mu)
        paint.end()

    def draw_gaussian_psd(self, paint, gaussian_data_points, mu, sigma):
        for value in gaussian_data_points:
            x = value
            fx = fx_gaussian_psd(x, mu, sigma)
            x_scaled = x * self.scale_multiplier_x + self.x0
            y_scaled = fx * self.scale_multiplier_y + self.y0
            paint.drawPoint(x_scaled, y_scaled)


    def draw_key_points(self, paint, minimum, maximum, mu, lt_mu, gt_mu):
        key_value_marker = QPen(Qt.black, 1, Qt.SolidLine)
        key_value_marker.setStyle(Qt.CustomDashLine)
        key_value_marker.setDashPattern([1, 4, 5, 4])
        paint.setPen(key_value_marker)

        x_mu = mu * self.scale_multiplier_x + self.x0
        x_min = minimum * self.scale_multiplier_x + self.x0
        x_max = maximum * self.scale_multiplier_x + self.x0
        y1 = self.y0 - 200


        paint.drawLine(x_mu, self.y0, x_mu, y1)
        paint.drawLine(x_min, self.y0, x_min, y1)
        paint.drawLine(x_max, self.y0, x_max, y1)
        print("GREATER THAN MEAN: ", len(gt_mu)/100000, ", SMALLER THAN MEAN: ", len(lt_mu)/100000)


if __name__ == '__main__':
    app = QApplication(argv)
    ex = App()
    exit(app.exec_())