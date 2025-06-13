import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDesktopWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QMenu, QAction, QDialog)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor

class ArcaDM(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window to full screen
        self.setWindowTitle("PyQt Desktop Environment")
        self.showFullScreen()

        # Center the window
        self.center()

        # Set desktop background (solid color for simplicity)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 128, 255))  # Blue background
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # Create central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Add spacer to push taskbar to bottom
        main_layout.addStretch()

        # Create taskbar
        taskbar = QWidget(self)
        taskbar.setFixedHeight(40)
        taskbar.setStyleSheet("background-color: #333; color: white;")
        taskbar_layout = QHBoxLayout(taskbar)
        taskbar_layout.setContentsMargins(5, 0, 5, 0)

        # M.A.T. button
        mat_button = QPushButton("M.A.T.", self)
        mat_button.setFixedWidth(100)
        mat_button.setStyleSheet("background-color: #555; color: white;")
        mat_button.clicked.connect(self.show_mat_menu)
        taskbar_layout.addWidget(mat_button)

        # Spacer for taskbar
        taskbar_layout.addStretch()

        # Clock
        self.clock_label = QLabel(self)
        self.clock_label.setStyleSheet("color: white;")
        taskbar_layout.addWidget(self.clock_label)

        # Update clock every second
        timer = QTimer(self)
        timer.timeout.connect(self.update_clock)
        timer.start(1000)
        self.update_clock()

        main_layout.addWidget(taskbar)

        # Create start menu (initially hidden)
        self.start_menu = QMenu(self)
        self.start_menu.setStyleSheet("background-color: #444; color: white;")

        # Add sample actions to start menu
        calculator_action = QAction("Calculator", self)
        calculator_action.triggered.connect(self.open_calculator)
        self.start_menu.addAction(calculator_action)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.close)
        self.start_menu.addAction(quit_action)

    def center(self):
        # Center the window on the screen
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(0, 0, screen.width(), screen.height())

    def update_clock(self):
        # Update clock display
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.setText(current_time)

    def show_mat_menu(self):
        # Show start menu at start button position
        mat_button = self.sender()
        pos = mat_button.mapToGlobal(mat_button.rect().bottomLeft())
        self.start_menu.popup(pos)

    def open_calculator(self):
        # Open a sample calculator dialog
        calc_dialog = CalculatorDialog(self)
        calc_dialog.show()


class CalculatorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calculator")
        self.setFixedSize(300, 400)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        self.display = QLabel("0", self)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 24px; background-color: white; padding: 10px;")
        layout.addWidget(self.display)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        grid_layout = QHBoxLayout()
        layout.addLayout(grid_layout)
        for btn_text in buttons:
            button = QPushButton(btn_text, self)
            button.setFixedSize(60, 60)
            button.clicked.connect(self.button_clicked)
            layout.addWidget(button)

        self.current_input = ""
        self.operation = None
        self.first_operand = None

    def button_clicked(self):
        sender = self.sender()
        text = sender.text()

        if text in '0123456789.':
            self.current_input += text
            self.display.setText(self.current_input)
        elif text in '+-*/':
            self.first_operand = float(self.current_input) if self.current_input else 0
            self.operation = text
            self.current_input = ""
        elif text == '=' and self.operation and self.current_input:
            second_operand = float(self.current_input)
            result = self.calculate(self.first_operand, second_operand, self.operation)
            self.display.setText(str(result))
            self.current_input = str(result)
            self.operation = None

    def calculate(self, a, b, op):
        if op == '+': return a + b
        if op == '-': return a - b
        if op == '*': return a * b
        if op == '/': return a / b if b != 0 else "Error"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = ArcaDM()
    sys.exit(app.exec_())