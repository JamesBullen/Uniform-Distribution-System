from PyQt6.QtWidgets import QWidget, QFormLayout, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtPrintSupport import QPrintDialog, QPrintPreviewDialog
from PyQt6.QtGui import QTextDocument, QTextCursor
from database import getValidtionTable, callProcedure
from table import Table

class ReportsTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QFormLayout()

        mostOrderedItem = ReportRow('Most ordered uniforms', 'call MostOrdered()')
        layout.addRow('Report:', mostOrderedItem)

        staffStatistics = ReportRow('Staff employed', 'call StaffStatistics()')
        layout.addRow('Report:', staffStatistics)

        uniformAllocation = ReportRow('Uniform allocation', 'call AllocationTable()')
        layout.addRow('Info:', uniformAllocation)

        supplierInfo = ReportRow('Supplier detials', 'call SupplierInfo()')
        layout.addRow('Info:', supplierInfo)

        self.setLayout(layout)

class ReportRow(QHBoxLayout):
    def __init__(self, label, procedure, args=None, exclude=0):
        super().__init__()
        self.procedure = procedure
        self.args = args
        self.exclude = exclude

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
        baseTable = Table(self.procedure, self.args, self.exclude)

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
                html.append(f'<td>{baseTable.item(row, col).text()}</td>')
            html.append('</tr>')
        html.append('</tbody></table>')

        docTable = cursor.insertHtml(''.join(html))
        doc.print(printer)