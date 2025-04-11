from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QFormLayout, QPushButton, QHBoxLayout, QTableWidget, QLabel
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtGui import QTextDocument, QTextCursor, QTextTableFormat, QTextFrameFormat
from database import getValidtionTable, callProcedure
from table import Table
from PyQt6 import QtGui, QtCore

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        test = ReportRow('Staff')
        layout.addRow('Report:', test)

        self.setLayout(layout)

class ReportRow(QHBoxLayout):
    def __init__(self, label):
        super().__init__()

        reportLabel = QLabel(label)
        # Buttons
        viewBut = QPushButton('View')
        viewBut.clicked.connect(self.viewReport)
        printBut = QPushButton('Print')
        printBut.clicked.connect(self.printReport)

        self.addWidget(reportLabel)
        self.addWidget(viewBut)
        self.addWidget(printBut)

    def viewReport(self):
        dialog = QPrintPreviewDialog()
        dialog.paintRequested.connect(self.createDocument)
        dialog.exec()

    def printReport(self):
        dialog = QPrintDialog()
        
        if dialog.exec() == QPrintDialog.accepted:
            self.createDocument(dialog.printer())
    
    def createDocument(self, printer):
        # Document setup
        doc = QTextDocument()
        cursor = QTextCursor(doc)
        baseTable = Table('call StaffInfo(%s)', 1)

        # HTML
        html = ['<table><thead><tr>']
        # Headers
        for header in range(baseTable.columnCount()):
            html.append(f'<th>{baseTable.horizontalHeaderItem(header).text()}</th>')
        # Rows
        html.append('</tr></thead><tbody>')
        for row in range(baseTable.rowCount()):
            html.append('<tr>')
            for col in range(baseTable.columnCount()):
                print(row, col)
                html.append(f'<td>{baseTable.item(row, col).text()}</td>')
            html.append('</tr>')
        html.append('</tbody></table>')

        docTable = cursor.insertHtml(''.join(html))

        doc.print(printer)

# for header in range(baseTable.columnCount()):
#             cursor.insertText(baseTable.horizontalHeaderItem(header).text())
#             cursor.movePosition(QTextCursor.MoveOperation.NextCell)

#         for row in range(docTable.rows() -1):
#             for col in range(docTable.columns()):
#                 cursor.insertText(baseTable.item(row, col).text())
#                 cursor.movePosition(QTextCursor.MoveOperation.NextCell)