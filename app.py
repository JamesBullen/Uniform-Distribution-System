import sys
import staff, orders, reports
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTabWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QCheckBox, QMessageBox
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QIntValidator
from database import createPool, loadValidtionTables

# Sets up the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/favicon.png"))
        self.setWindowTitle("Uniform Distribution")
        mainWidget = QWidget()
        layout = QVBoxLayout(mainWidget)
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

        # Loads validation tables from database
        loadValidtionTables()

        # Staff tab
        self.staffTab = staff.StaffTab()
        layout.addWidget(self.staffTab)

        # Orders tab
        self.ordersTab = orders.OrdersTab()
        layout.addWidget(self.ordersTab)

        # Reports tab
        self.reportsTab = reports.ReportsTab()
        layout.addWidget(self.reportsTab)

        # Adds tabs together
        tabs = QTabWidget()
        tabs.addTab(self.staffTab,"Staff")
        tabs.addTab(self.ordersTab,"Orders")
        tabs.addTab(self.reportsTab,"Reports")
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

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    sys.exit(app.exec())
#! No code after here