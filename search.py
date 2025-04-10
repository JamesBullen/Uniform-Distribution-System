from PyQt6.QtWidgets import  QWidget, QFormLayout, QPushButton, QComboBox
from PyQt6.QtGui import QIcon
from database import callProcedure, getValidtionTable

# search widget class go here
class Search(QWidget):
    def __init__(self):
        super().__init__()

class StaffSearch(QFormLayout):
    def __init__(self, finish, cancel):
        super().__init__()

        self.staffInput = QComboBox() # Needs to be declared here due to role affecting it
        # Role search
        self.roleInput = QComboBox()
        roleResults = getValidtionTable('tbl_roles')
        self.roleInput.addItems([i[1] for i in roleResults])
        self.roleInput.setCurrentIndex(-1)
        self.roleInput.currentIndexChanged.connect(lambda: self.loadStaff(self.roleInput.currentIndex()+1))
        self.addRow(self.tr('Role:'), self.roleInput)
        # Staff search
        self.addRow(self.tr('Name:'), self.staffInput)
        # Buttons
        nextBut = QPushButton('Next')
        nextBut.clicked.connect(finish)
        cancBut = QPushButton('Cancel')
        cancBut.clicked.connect(cancel)
        self.addRow(nextBut, cancBut)

    def loadStaff(self, role):
        self.staffResult = callProcedure('call FindStaff(%s)', role)[0]

        self.staffInput.clear()
        self.staffInput.addItems([f"{i[1]}, ID: {i[0]}" for i in self.staffResult])

        if len(self.staffResult) == 1:
            return
        
        self.staffInput.setCurrentIndex(-1)

    def roleSelection(self):
        return self.roleInput.currentIndex()
    
    def staffSelection(self):
        return self.staffInput.currentIndex()
    
    def getStaffData(self):
        return self.staffResult