from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt6.QtCore import Qt
from database import callProcedure

class Table(QTableWidget):
    def __init__(self, procedure, args, exclude=0, checks=False):
        super().__init__()
        self.procedure = procedure
        self.args = args
        self.exclude = exclude
        self.checks = checks

        self.data = self.getData(args)
        self.setColumnCount(len(self.data[1])-exclude if checks == False else len(self.data[1])-exclude+1)

        self.setTable()
    
    def getData(self, args):
        results =  callProcedure(self.procedure, args)
        return results
    
    def setTable(self, rows=None):
        if self.checks:
            checkHeaders = list(self.data[1][self.exclude:])
            checkHeaders.append('Select')
        self.setHorizontalHeaderLabels(self.data[1][self.exclude:] if self.checks == False else checkHeaders)
        
        if not rows:
            rows = [i[self.exclude:] for i in self.data[0]]

        # O(n^2), find better solution in future
        for r in rows:
            rowPos = self.rowCount()
            self.insertRow(rowPos)

            for i in range(0, len(r)):
                self.setItem(rowPos, i, QTableWidgetItem(str(r[i])))
            
            if self.checks:
                checkbox = QTableWidgetItem()
                checkbox.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
                checkbox.setCheckState(Qt.CheckState.Unchecked)
                self.setItem(rowPos, len(r), checkbox)
    
    def updateTable(self):
        rows = self.getData(self.rowCount() +1)[0]
        newRows = [r for r in rows if r not in self.data[0]]
        
        self.setTable(newRows)
    
    def refreshTable(self):
        self.setRowCount(0)

        self.data = self.getData(self.args)
        self.setTable()

    def getSelectedRows(self):
        if not self.checks:
            return
        
        results = []
        for row in range(self.rowCount()):
            if self.item(row, self.columnCount()-1).checkState() == Qt.CheckState.Checked:              
                results.append(row)

        # Returns indexes of selected rows
        return results
    
    def getRawData(self, indexes=None):
        if indexes:
            results = []
            for index in indexes:
                results.append(self.data[0][index])
            
            return results
        
        return self.data[0]
    
    def getRowCount(self):
        return self.rowCount()
    
    def clearTable(self):
        self.setRowCount(0)