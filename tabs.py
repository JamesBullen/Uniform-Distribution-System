from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTabWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QCheckBox, QMessageBox
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
        layout = QVBoxLayout()

        # Table
        self.table = Tables(extractTable(pool, 'tbl_staff')[1])
        layout.addWidget(self.table)

        self.setLayout(layout)

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