import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTabWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QCheckBox, QMessageBox
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from database import open_connection

# Sets up the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/favicon.png"))
        self.setWindowTitle("Uniform Distribution System")
        mainWidget = QWidget()
        layout = QVBoxLayout(mainWidget)
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

        self.testtab = TabsTest('one')
        layout.addWidget(self.testtab)
        self.testtab2 = TabsTest('two')
        layout.addWidget(self.testtab2)

        tabs = QTabWidget()
        tabs.addTab(self.testtab,"Test Tab")
        tabs.addTab(self.testtab2,"Test Tab 2")
        layout.addWidget(tabs)

        self.show()

class TabsTest(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel(f"<h1>{text}</h1>")
        layout.addWidget(self.label)

        self.setLayout(layout)

# Tries to connect to database
if not open_connection():
    # Close program if can't connect
    sys.exit(1)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())