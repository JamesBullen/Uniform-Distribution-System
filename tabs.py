from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTabWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QCheckBox, QMessageBox, QDialog
from database import extractTable

class Tables(QWidget):
    def __init__(self, headers):
        super().__init__()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        layout.addWidget(self.table)
        self.setLayout(layout)

class StaffTab(QWidget):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool
        layout = QVBoxLayout()

        self.newStaffButton = QPushButton('Add new Staffer', self)
        self.newStaffButton.clicked.connect(self.addStaff)
        layout.addWidget(self.newStaffButton)

        # will use different function later
        results = extractTable(self.pool, 'tbl_staff')
        # Table
        self.table = Tables(results[1])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def addStaff(self):
        self.table.hide()

class OrdersTab(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel(f"<h1>{text}</h1>")
        layout.addWidget(self.label)

        self.setLayout(layout)

class ReportsTab(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel(f"<h1>{text}</h1>")
        layout.addWidget(self.label)

        self.setLayout(layout)