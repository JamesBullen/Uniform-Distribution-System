from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QFormLayout, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QMessageBox, QErrorMessage, QFrame, QCheckBox
from PyQt6.QtGui import QIntValidator
from database import getValidtionTable, callProcedure
from table import Table

class OrdersTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.labelDict = {1: None, 2: None, 3: None, 4: None}
        self.inputDict = {1: None, 2: None, 3: None, 4: None}

        # Table
        self.table = Table("call OrderInfo(%s)", 1)

        # Buttons
        tableButtons = QHBoxLayout()
        # New order
        #* select role, brings up all uniforms of that role, then select size and quantity
        self.newOrderButton = QPushButton('Place an order', self)
        self.newOrderButton.clicked.connect(self.showSelectionForm)
        tableButtons.addWidget(self.newOrderButton)
        # Available reissues
        # Refresh
        refreshBut = QPushButton('Refresh')
        refreshBut.clicked.connect(self.table.updateTable)
        tableButtons.addWidget(refreshBut)
        layout.addLayout(tableButtons)

        # Staff selection form
        self.selectionLayout = QFormLayout()
        self.selectionFrame = QFrame()
        self.staffInput = QComboBox() # Needs to be declared here due to role affecting it
        # Role search
        self.roleInput = QComboBox()
        roleResults = getValidtionTable('tbl_roles')
        self.roleInput.addItems([i[1] for i in roleResults])
        self.roleInput.setCurrentIndex(-1)
        self.roleInput.currentIndexChanged.connect(lambda: self.loadStaff(self.roleInput.currentIndex()+1))
        self.selectionLayout.addRow(self.tr('Role:'), self.roleInput)
        # Staff search
        self.selectionLayout.addRow(self.tr('Name:'), self.staffInput)
        # Buttons
        nextBut = QPushButton('Next')
        nextBut.clicked.connect(lambda: print('clicked'))
        cancBut = QPushButton('Cancel')
        cancBut.clicked.connect(lambda: self.selectionFrame.hide())
        self.selectionLayout.addRow(nextBut, cancBut)
        # Layout
        self.selectionFrame.setLayout(self.selectionLayout)

        # Uniform selection
        self.uniformLayout = QFormLayout()
        self.uniformFrame = QFrame()
        # test
        testy = QLineEdit()
        validator = QIntValidator(1, 99, self)
        testy.setValidator(validator)
        # Layout
        self.uniformFrame.setLayout(self.uniformLayout)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def showSelectionForm(self):
        self.roleInput.setCurrentIndex(-1)
        self.staffInput.clear()
        self.selectionFrame.show()
        return

    def loadStaff(self, role):
        staffResult = callProcedure('call FindStaff(%s)', role)[0]

        self.staffInput.clear()
        self.staffInput.addItems([f"{i[1]}, ID: {i[0]}" for i in staffResult])

        if len(staffResult) == 1:
            self.generateSelection()
            return
        
        self.staffInput.setCurrentIndex(-1)
        return
    
    def generateSelection(self):
        ...