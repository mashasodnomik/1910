import sys
from math import cos, pi, sin

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QInputDialog, QFileDialog

SCREEN_SIZE = [500, 500]


class Fractal:
    def __init__(self, filename):
        with open(filename, "r") as f:
            self.side = int(f.readline())
            self.angle = int(f.readline())
            self.init = f.readline().strip()
            self.exps = list(map(str.strip, f.readlines()))

    def calculate_epochs(self, n):
        parse_exps = []
        for exp in self.exps:
            parse_exps.append(exp.split("->"))
        result = self.init
        for _ in range(n):
            for exp in parse_exps:
                if exp[0] in result:
                    result = result.replace(exp[0], exp[1])
        return result








class DrawFractal(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fractal = Fractal(QFileDialog.getOpenFileName(self, "Выберите фрактал", "")[0])

        print(self.fractal.calculate_epochs(2))




    def initUI(self):
        self.setGeometry(300, 300, *SCREEN_SIZE)
        self.setWindowTitle('Рисуем звезду')

        self.btn = QPushButton("Рисуй", self)
        self.btn.clicked.connect(self.run)

        self.do_paint = False

    def run(self):
        self.do_paint = True
        self.repaint()
        self.do_paint = False

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.draw_fractal(qp)
            qp.end()

    def xs(self, x):
        return x + SCREEN_SIZE[0] // 2

    def ys(self, y):
        return SCREEN_SIZE[1] // 2 - y

    def draw_fractal(self, qp):
        current_x,current_y = 0, 0
        fractal = self.fractal.calculate_epochs(3)
        angle = 0
        for sym in fractal:
            if sym == "f" or sym == "F":
                new_x = current_x + self.fractal.side * cos(angle * pi / 180)
                new_y = current_y + self.fractal.side * sin(angle * pi / 180)
                if sym == "F":
                    qp.drawLine(self.xs(current_x), self.ys(current_y), self.xs(new_x), self.ys(new_y))
                current_x, current_y = new_x, new_y
            elif sym == "-":
                angle += self.fractal.angle
            elif sym == "+":
                angle -= self.fractal.angle





def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
sys.excepthook = except_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DrawFractal()
    ex.show()
    sys.exit(app.exec())

