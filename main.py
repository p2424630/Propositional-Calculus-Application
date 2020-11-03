import sys
from pyqt5_material import apply_stylesheet
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QPushButton, QVBoxLayout

# # app = QApplication([])
# # create the application and the main window
# app = QApplication(sys.argv)
#
# label = QLabel('Hello World!')
# # label.show()
# window = QMainWindow(label)
#
# apply_stylesheet(app, theme='dark_teal.xml')
# window.show()
# app.exec_()


app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
apply_stylesheet(app, theme='dark_teal.xml')
window.setLayout(layout)
window.show()
app.exec_()
