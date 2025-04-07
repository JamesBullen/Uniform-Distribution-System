from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QMessageBox, QErrorMessage, QFrame
from database import getValidtionTable, callProcedure
from table import Table

class OrdersTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Buttons
        tableButtons = QHBoxLayout()
        # New order
        #* select role, brings up all uniforms of that role, then select size and quantity
        # Available reissues
        # 

        # Table
        self.table = Table("call OrderInfo(%s)", 1)
        layout.addWidget(self.table)

        self.setLayout(layout)