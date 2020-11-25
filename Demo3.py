import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox, QApplication

def dialog():
    mbox = QMessageBox()

    mbox.setText("Your allegiance has been noted")
    mbox.setDetailedText("You are now a disciple and subject of the all-knowing Guru")
    mbox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            
    mbox.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    window = QWidget()
    window.resize(300, 300)
    window.setWindowTitle("DX First Demo")

    label = QLabel(window)
    label.setText("Behold the Guru, Guru99")
    label.move(100,130)
    label.show()

    btn = QPushButton(window)
    btn.setText('Beheld')
    btn.move(110,150)
    btn.show()
    btn.clicked.connect(dialog)

    window.show()
    sys.exit(app.exec_())


