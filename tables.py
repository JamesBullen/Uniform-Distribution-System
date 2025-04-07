from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from database import callProcedure

class Tables(QWidget):
    def __init__(self, procedure, args):
        super().__init__()
        layout = QVBoxLayout()
        self.procedure = procedure

        results = self.getData(args)
        self.table = QTableWidget()
        self.table.setColumnCount(len(results[1]))
        self.table.setHorizontalHeaderLabels(results[1])
        self.setTable(results[0])

        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def getData(self, args):
        results =  callProcedure(self.procedure, args)
        return results
    
    def setTable(self, rows):
        # O(n^2), find better solution in future
        for r in rows:
            rowPosition = self.table.rowCount()
            self.table.insertRow(rowPosition)

            for i in range(0, len(r)):
                self.table.setItem(rowPosition, i, QTableWidgetItem(str(r[i])))
    
    def updateTable(self):
        newRows = self.getData(self.table.rowCount() +1)[0]
        self.setTable(newRows)