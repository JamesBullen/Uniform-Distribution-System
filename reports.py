from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QMessageBox, QErrorMessage, QFrame
from database import getValidtionTable, callProcedure

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.setLayout(layout)