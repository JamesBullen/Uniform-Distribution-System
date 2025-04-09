from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from database import callProcedure

class Table(QWidget):
    def __init__(self, procedure, args):
        super().__init__()
        layout = QVBoxLayout()
        self.procedure = procedure

        self.data = self.getData(args)
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.data[1]))
        self.table.setHorizontalHeaderLabels(self.data[1])
        self.setTable(self.data[0])

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
        rows = self.getData(self.table.rowCount() +1)[0]
        newRows = [r for r in rows if r not in self.data[0]]
        
        self.setTable(newRows)