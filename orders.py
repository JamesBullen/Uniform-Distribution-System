from PyQt6.QtWidgets import QWidget, QFormLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox, QFrame, QCheckBox
from PyQt6.QtGui import QIcon, QIntValidator
from database import getValidtionTable, callProcedure
from table import Table
from search import StaffSearch

class OrdersTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.varDict = {1: None, 2: None, 3: None, 4: None}

        # Table
        self.table = Table("call OrderInfo(%s)", 1)

        # Buttons
        tableButtons = QHBoxLayout()
        # New order
        #* select role, brings up all uniforms of that role, then select size and quantity
        self.newOrderButton = QPushButton('Place Order', self)
        self.newOrderButton.clicked.connect(self.showSelectionForm)
        tableButtons.addWidget(self.newOrderButton)
        # Available reissues
        self.availReissueBut = QPushButton('Available Reissues')
        self.availReissueBut.clicked.connect(self.showReissues)
        tableButtons.addWidget(self.availReissueBut)
        # Refresh
        refreshBut = QPushButton('Refresh')
        refreshBut.clicked.connect(self.table.refreshTable)
        tableButtons.addWidget(refreshBut)
        layout.addLayout(tableButtons)

        # Staff selection form
        self.selectionForm = StaffSearch('Next', 'Cancel')
        self.selectionForm.setFinBut(self.nextAction)
        self.selectionForm.setCancBut(lambda: self.selectionFrame.hide())
        self.selectionFrame = QFrame()
        self.selectionFrame.setWindowIcon(QIcon("assets/favicon.png"))
        self.selectionFrame.setWindowTitle('Staff Select')
        self.selectionFrame.setLayout(self.selectionForm)

        # Uniform selection
        self.uniformLayout = QVBoxLayout()
        self.uniformForm = QFormLayout()
        self.uniformFrame = QFrame()
        self.uniformFrame.setWindowIcon(QIcon("assets/favicon.png"))
        self.uniformFrame.setWindowTitle('Uniform Select')
        uniformButs = QHBoxLayout()
        # Buttons
        self.finBut = QPushButton('Finish')
        self.finBut.clicked.connect(self.finAction)
        self.backBut = QPushButton('Back')
        self.backBut.clicked.connect(self.showSelectionForm)
        uniformButs.addWidget(self.finBut)
        uniformButs.addWidget(self.backBut)
        # Layout
        self.uniformLayout.addLayout(self.uniformForm)
        self.uniformLayout.addLayout(uniformButs)
        self.uniformFrame.setLayout(self.uniformLayout)

        # Reissuing selection
        self.reissueLayout = QVBoxLayout()
        self.reissueForm = QFormLayout()
        self.reissueFrame = QFrame()
        self.reissueFrame.setWindowIcon(QIcon("assets/favicon.png"))
        self.reissueFrame.setWindowTitle('Available Reissues')
        self.reissueTable = Table('call AvailableReissues()', None, 3, True)
        # Buttons
        reissueSelecBut = QPushButton('Reissue Selected')
        reissueSelecBut.clicked.connect(self.reissueUniform)
        reissueAllBut = QPushButton('Reissue All')
        reissueAllBut.clicked.connect(lambda: self.reissueUniform(True))
        cancReissueBut = QPushButton('Cancel')
        cancReissueBut.clicked.connect(lambda: self.reissueFrame.hide())
        self.reissueButs = QHBoxLayout()
        self.reissueButs.addWidget(reissueSelecBut)
        self.reissueButs.addWidget(reissueAllBut)
        self.reissueButs.addWidget(cancReissueBut)
        # Layout
        self.reissueLayout.addWidget(self.reissueTable)
        self.reissueLayout.addLayout(self.reissueButs)
        self.reissueFrame.setLayout(self.reissueLayout)

        layout.addWidget(self.table)
        self.setLayout(layout)

    def showSelectionForm(self):
        self.uniformFrame.hide()
        self.selectionFrame.show()
    
    def nextAction(self):
        args = [self.selectionForm.getStaffData()[self.selectionForm.staffSelection()][2], self.selectionForm.roleSelection()+1, self.selectionForm.getStaffData()[self.selectionForm.roleSelection()][3]]
        self.uniformResult = callProcedure('call AllocatedUniform(%s, %s, %s)', args)
        
        self.generateSelection(self.uniformResult)

    # Displays all uniform that specific staff is allowed to order
    def generateSelection(self, uniforms):
        # Clears layout
        if self.varDict[1]:
            for i in range(4):
                row = self.varDict[i]
                if row:
                    self.uniformForm.removeRow(row)
        
        sizesTable = getValidtionTable('tbl_sizes')
        for i in range(0, len(uniforms[0])):
            # Available sizes
            sizes= QComboBox()
            sizes.addItems(sizesTable[uniforms[0][i][3]][1].split(','))

            # Quantity wanted
            quantity = QLineEdit()
            quantiyValidation = QIntValidator(1, 99, self)
            quantity.setValidator(quantiyValidation)

            # Checkbox
            selected = QCheckBox()

            # Input fields
            fields = QHBoxLayout()
            fields.addWidget(sizes)
            fields.addWidget(quantity)
            fields.addWidget(selected)
            fields.widget
            
            self.varDict[i] = fields
            self.uniformForm.addRow(self.tr(f'{uniforms[0][i][0]}:'), fields)
        
        self.selectionFrame.hide()
        self.uniformFrame.show()
    
    def finAction(self):
        self.uniformFrame.hide()

        orderNum = callProcedure('call NextOrderNumber()')
        for i in self.varDict:
            if not self.varDict[i]:
                continue
            if self.varDict[i].itemAt(2).widget().isChecked():
                details = self.uniformResult[0][i]
                args = [orderNum[0][0][0], self.selectionFrame.getStaffData()[self.staffInput.currentIndex()][0], details[1], details[2], self.varDict[i].itemAt(0).widget().currentText(), details[3]]
                callProcedure('call PurchaseUniform(%s, %s, %s, %s, %s, %s, 1, 0)', args)
        
        self.table.refreshTable()
    
    def showReissues(self):
        self.reissueTable.refreshTable()
        
        self.reissueFrame.show()

    def reissueUniform(self, all=False):
        if all:
            uniforms = self.reissueTable.getRowCount()
            data = self.reissueTable.getRawData()
        else:
            uniforms = self.reissueTable.getSelectedRows()
            indexes = self.reissueTable.getSelectedRows()
            data = self.reissueTable.getRawData(indexes)
        
        colours = dict(getValidtionTable('tbl_colours'))
        orderNum = callProcedure('call NextOrderNumber()')[0][0][0]

        for i in range(uniforms if all == True else len(uniforms)):
            args = [orderNum if orderNum == True else 1, data[i][1], data[i][2], list(colours.keys())[list(colours.values()).index(data[i][6])], data[i][7], data[i][8], data[i][0]]
            callProcedure('call PurchaseUniform(%s, %s, %s, %s, %s, %s, 0, %s)', args)
        
        self.reissueFrame.hide()