from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QCheckBox
from database import callProcedure

class Table(QWidget):
    def __init__(self, procedure, args, exclude=0, checks=False):
        super().__init__()
        layout = QVBoxLayout()
        self.procedure = procedure
        self.checks = checks

        self.data = self.getData(args)
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.data[1])-exclude if checks == False else len(self.data[1])-exclude+1)
        self.table.setHorizontalHeaderLabels(self.data[1][exclude:])
        self.setTable(self.data[0][exclude:])

        layout.addWidget(self.table)
        self.setLayout(layout)
    
    def getData(self, args):
        results =  callProcedure(self.procedure, args)
        return results
    
    def setTable(self, rows):
        # O(n^2), find better solution in future
        for r in rows:
            rowPos = self.table.rowCount()
            self.table.insertRow(rowPos)

            for i in range(0, len(r)):
                self.table.setItem(rowPos, i, QTableWidgetItem(str(r[i])))
            
            if self.checks:
                self.table.setItem(rowPos, len(r)+1, QCheckBox())
    
    def updateTable(self):
        rows = self.getData(self.table.rowCount() +1)[0]
        newRows = [r for r in rows if r not in self.data[0]]
        
        self.setTable(newRows)