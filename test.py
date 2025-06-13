import sys
import time
import os
import logging
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QDesktopWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QMenu, QAction, QDialog, QGridLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPalette, QColor

# Set up logging
logging.basicConfig(filename='desktop_env.log', level=logging.DEBUG, 
                    format='%(asctime)s %(levelname)s: %(message)s')

class DesktopEnvironment(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_wayland = self.check_display_server()
        try:
            self.initUI()
        except Exception as e:
            logging.error(f"Failed to initialize UI: {str(e)}")
            raise

    def check_display_server(self):
        # Check if running on Wayland or Xorg
        display_type = os.environ.get("XDG_SESSION_TYPE", "unknown").lower()
        logging.info(f"Detected display server: {display_type}")
        return display_type == "wayland"

    def initUI(self):
        # Set window to full screen
        self.setWindowTitle("PyQt Desktop Environment")
        try:
            self.showFullScreen()
        except Exception as e:
            logging.error(f"Failed to set full screen: {str(e)}")
            return

        # Center the window
        self.center()

        # Set desktop background (solid color)
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

        # Start button
        start_button = QPushButton("Start", self)
        start_button.setFixedWidth(100)
        start_button.setStyleSheet("background-color: #555; color: white;")
        start_button.clicked.connect(self.show_start_menu)
        taskbar_layout.addWidget(start_button)

        # Spacer for taskbar
        taskbar_layout.addStretch()

        # Clock
        self.clock_label = QLabel(self)
        self.clock_label.setStyleSheet("color: white;")
        taskbar_layout.addWidget(self.clock_label)

        # Update clock every second
        try:
            timer = QTimer(self)
            timer.timeout.connect(self.update_clock)
            timer.start(1000)
            self.update_clock()
        except Exception as e:
            logging.error(f"Failed to initialize clock timer: {str(e)}")

        main_layout.addWidget(taskbar)

        # Create start menu
        try:
            self.start_menu = QMenu(self)
            self.start_menu.setStyleSheet("background-color: #444; color: white;")
            calculator_action = QAction("Calculator", self)
            calculator_action.triggered.connect(self.open_calculator)
            self.start_menu.addAction(calculator_action)
            quit_action = QAction("Quit", self)
            quit_action.triggered.connect(self.close)
            self.start_menu.addAction(quit_action)
        except Exception as e:
            logging.error(f"Failed to initialize start menu: {str(e)}")

    def center(self):
        # Center the window on the screen
        try:
            screen = QDesktopWidget().screenGeometry()
            self.setGeometry(0, 0, screen.width(), screen.height())
        except Exception as e:
            logging.error(f"Failed to center window: {str(e)}")

    def update_clock(self):
        # Update clock display
        try:
            current_time = time.strftime("%H:%M:%S")
            self.clock_label.setText(current_time)
        except Exception as e:
            logging.error(f"Failed to update clock: {str(e)}")

    def show_start_menu(self):
        # Show start menu at start button position
        try:
            start_button = self.sender()
            pos = start_button.mapToGlobal(start_button.rect().bottomLeft())
            self.start_menu.popup(pos)  # Safe for both Wayland and Xorg
        except Exception as e:
            logging.error(f"Failed to show start menu: {str(e)}")

    def open_calculator(self):
        # Open a sample calculator dialog
        try:
            calc_dialog = CalculatorDialog(self, self.is_wayland)
            calc_dialog.show()
            if not self.is_wayland:
                calc_dialog.activateWindow()
        except Exception as e:
            logging.error(f"Failed to open calculator: {str(e)}")

class CalculatorDialog(QDialog):
    def __init__(self, parent=None, is_wayland=False):
        super().__init__(parent)
        self.is_wayland = is_wayland
        self.setWindowTitle("Calculator")
        self.setFixedSize(300, 400)
        try:
            self.initUI()
        except Exception as e:
            logging.error(f"Failed to initialize calculator UI: {str(e)}")

    def initUI(self):
        layout = QVBoxLayout(self)
        self.display = QLabel("0", self)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 24px; background-color: white; padding: 10px;")
        layout.addWidget(self.display)

        # Use QGridLayout for buttons
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        buttons = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('/', 0, 3),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('*', 1, 3),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3),
            ('0', 3, 0), ('.', 3, 1), ('=', 3, 2), ('+', 3, 3)
        ]

        for btn_text, row, col in buttons:
            button = QPushButton(btn_text, self)
            button.setFixedSize(60, 60)
            button.clicked.connect(self.button_clicked)
            grid_layout.addWidget(button, row, col)

        self.current_input = ""
        self.operation = None
        self.first_operand = None

    def button_clicked(self):
        try:
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
        except Exception as e:
            logging.error(f"Calculator button error: {str(e)}")

    def calculate(self, a, b, op):
        try:
            if op == '+': return a + b
            if op == '-': return a - b
            if op == '*': return a * b
            if op == '/': return a / b if b != 0 else "Error"
        except Exception as e:
            logging.error(f"Calculation error: {str(e)}")
            return "Error"

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        desktop = DesktopEnvironment()
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Application crashed: {str(e)}")
        raise