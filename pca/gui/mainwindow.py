from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Propositional Calculus Application')
        self.setLayout(QtWidgets.QVBoxLayout())
        self.setGeometry(200, 200, 300, 300)
        self.teach()
        self.show()

    def teach(self):
        cont = QtWidgets.QWidget()
        cont.setLayout(QtWidgets.QGridLayout())
    # label = QtWidgets.QLabel(win)
    # label.setText(' Section 1')
    #
    # win.show()
    # sys.exit((app.exec()))


app = QApplication([])
win = MainWindow()
app.setStyle(QtWidgets.QStyleFactory.create('Fusion'))
app.exec()
