from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFormLayout, QPushButton, QHBoxLayout, QTableWidget
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtGui import QTextDocument, QTextCursor
from database import getValidtionTable, callProcedure
from table import Table

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        test = ReportRow()
        layout.addRow('test', test)
        self.setLayout(layout)

class ReportRow(QHBoxLayout):
    def __init__(self):
        super().__init__()

        # Buttons
        viewBut = QPushButton('View')
        viewBut.clicked.connect(self.viewReport)
        printBut = QPushButton('Print')
        printBut.clicked.connect(self.printReport)

        self.addWidget(viewBut)
        self.addWidget(printBut)

    def viewReport(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.createDocument)
        dialog.exec()

    def printReport(self):
        dialog = QPrintDialog()
        
        if dialog.exec() == QPrintDialog.accepted:
            self.test.print(self.createDocument)
    
    def createDocument(self, printer):
        doc = QTextDocument()
        cursor = QTextCursor(doc)
        baseTable = Table('call StaffInfo(%s)', 1)
        docTable = cursor.insertTable(baseTable.rowCount(), baseTable.columnCount())

        for row in range(docTable.rows()):
            for col in range(docTable.columns()):
                cursor.insertText(baseTable.item(row, col).text())
                cursor.movePosition(QTextCursor.MoveOperation.NextCell)

        doc.print(printer)