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

    def exec(self):
        self.show()
        self.desktop.exec()

if __name__ == '__main__':
    desktop = ArcaDM()
    desktop.exec()
