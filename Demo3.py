import sys
# from PyQt5.QtWidgets import QApplication, QLabel, QToolBar, QAction, QStatusBar, QCheckBox, QMainWindow
# from PyQt5.QtCore import Qt, QSize
# from PyQt5.QtGui import QIcon

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")


        layout = QVBoxLayout()
        widgets = [QCheckBox,
            QComboBox,
            QDateEdit,
            QDateTimeEdit,
            QDial,
            QDoubleSpinBox,
            QFontComboBox,
            QLCDNumber,
            QLabel,
            QLineEdit,
            QProgressBar,
            QPushButton,
            QRadioButton,
            QSlider,
            QSpinBox,
            QTimeEdit]

        for w in widgets:
            layout.addWidget(w())


        widget = QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()