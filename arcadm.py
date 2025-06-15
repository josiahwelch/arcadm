#!/usr/local/bin/python3
import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDesktopWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QMenu, QAction, QDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor

class ArcaDM(QMainWindow):
    def __init__(self):
        super().__init__()

        #initialization of variables
        self.desktop = QApplication(sys.argv)
        self.setWindowTitle("Arca Desktop Manager")
        button = QPushButton("Press this")

        #final stuff prior to bootup
        self.setCentralWidget(button)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = ArcaDM()

    desktop.show()
    app.exec()
