import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTabWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QCheckBox, QMessageBox
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon
from database import openConnection, createPool, extractTable
from tabs import StaffTab

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

        # Staff tab
        self.staffTab = StaffTab()
        layout.addWidget(self.staffTab)

        # Orders tab
        # Reports tab

        # Adds tabs together
        tabs = QTabWidget()
        tabs.addTab(self.staffTab,"Staff")
        layout.addWidget(tabs)

        self.show()

class TabsTest(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel(f"<h1>{text}</h1>")
        layout.addWidget(self.label)

        self.setLayout(layout)

# Creates connection pool
connectionPool = createPool()
# Tests connection to database
if not connectionPool:
    # Close program if can't connect
    sys.exit(1)

def getConnection():
    return connectionPool.get_connection()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
#! No code after here