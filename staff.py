from PyQt6.QtWidgets import QWidget, QGridLayout, QFormLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QMessageBox, QFrame
from PyQt6.QtGui import QIntValidator, QValidator, QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression
from database import getValidtionTable, callProcedure
from table import Table

class StaffTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.labelDict = {1: None, 2: None, 3: None, 4: None}
        self.inputDict = {1: None, 2: None, 3: None, 4: None}

        # Buttons
        tableButtons = QHBoxLayout()
        # Add new staffer
        self.newStaffButton = QPushButton('Add new staffer', self)
        self.newStaffButton.clicked.connect(self.openStaffForm)
        tableButtons.addWidget(self.newStaffButton)

        layout.addLayout(tableButtons)
        
        # Table
        self.table = Table("call StaffInfo(%s)", 1)
        layout.addWidget(self.table)

        # Staff input form
        self.staffLayout = QFormLayout()
        self.staffFrame = QFrame()
        # Name row
        self.nameInput = QLineEdit(self)
        regexValidator = QRegularExpressionValidator(QRegularExpression("[A-Z a-z '-]{0,40}"), self)
        self.nameInput.setValidator(regexValidator)
        self.staffLayout.addRow(self.tr('Full Name:'), self.nameInput)
        # Sex row
        self.sexInput = QComboBox(self)
        self.sexInput.addItems(['Male','Female'])
        self.sexInput.setCurrentIndex(-1)
        self.staffLayout.addRow(self.tr('Sex:'), self.sexInput)
        # Role row
        self.roleInput = QComboBox(self)
        roleResults = getValidtionTable('tbl_roles')
        self.roleInput.addItems([i[1] for i in roleResults])
        self.roleInput.setCurrentIndex(-1)
        self.staffLayout.addRow(self.tr('Role:'), self.roleInput)
        # Hours row
        self.hoursInput = QLineEdit(self)
        hoursValidation = QIntValidator(1, 80, self)
        self.hoursInput.setValidator(hoursValidation)
        self.staffLayout.addRow(self.tr('Hours:'), self.hoursInput)
        # Buttons
        self.nextButton = QPushButton('Next')
        self.nextButton.clicked.connect(self.nextAction)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelAction)
        self.staffLayout.addRow(self.nextButton, self.cancelButton)
        self.staffFrame.setLayout(self.staffLayout)

        # Size form
        self.uniformLayout = QFormLayout()
        self.uniformFrame = QFrame()
        self.sizesResults = getValidtionTable('tbl_sizes')
        # Button options
        self.finishButton = QPushButton('Finish')
        self.finishButton.clicked.connect(self.finishAction)
        self.backButton = QPushButton('Back')
        self.backButton.clicked.connect(self.backAction)
        # Add everything to layout
        self.uniformFrame.setLayout(self.uniformLayout)

        self.setLayout(layout)

    def openStaffForm(self):
        # Changes display
        self.staffFrame.show()
    
    def nextAction(self):
        uniformFields = [self.sexInput.currentText()[0], self.roleInput.currentIndex()+1, self.hoursInput.text()]
        self.uniformResult = callProcedure("call AllocatedUniform(%s, %s, %s)", uniformFields)
        self.staffFrame.hide()
        self.generateForm(self.uniformResult[0])
    
    def cancelAction(self):
        self.staffFrame.hide()
        self.clearStaffForm()

    def clearStaffForm(self):
        self.nameInput.clear()
        self.sexInput.setCurrentIndex(-1)
        self.roleInput.setCurrentIndex(-1)
        self.hoursInput.clear()

    def generateForm(self, uniforms):
        # Clears layout
        if self.labelDict[1]:
            for i in range(4):
                self.uniformLayout.removeRow(self.labelDict[i])
        
        # Resets for loop
        self.labelDict = {1: None, 2: None, 3: None, 4: None} # This still needed?
        self.inputDict = {1: None, 2: None, 3: None, 4: None}

        # Dynamically creates size fields for each uniform type
        for i in range(0, len(uniforms)):
            self.labelDict[i] = QLabel()
            self.labelDict[i].setText(uniforms[i][0])

            sizeOptions = self.sizesResults[uniforms[i][3]-1][1]

            self.inputDict[i] = QComboBox()
            self.inputDict[i].addItems(sizeOptions.split(','))
            self.uniformLayout.addRow(self.labelDict[i], self.inputDict[i])

        self.uniformLayout.addRow(self.finishButton, self.backButton)
        self.uniformFrame.show()

    def finishAction(self):
        # validation checks will go hear, will see about a switch case for different validation errors
        try:
            staffFields = [self.nameInput.text(), self.sexInput.currentText()[0], self.roleInput.currentIndex()+1, self.hoursInput.text()]
        except:
            QMessageBox.warning(self, 'Missing values', "All fields must be filled correctly")
            return
        
        callProcedure("call AddNewStaff(%s, %s, %s, %s)", staffFields)

        self.clearStaffForm()

        order = callProcedure("call NextOrderNumber", None)[0][0][0]
        staffID = callProcedure("call LastAddedStaff", None)[0][0][0]
        for i in self.inputDict:
            print(self.labelDict[i])
            if self.labelDict[i]:
                args = [order, staffID, self.uniformResult[0][i][1], self.uniformResult[0][i][2], self.inputDict[i].currentText(), self.uniformResult[0][i][4]]
                print(args)
                callProcedure("call PurchaseUniform(%s, %s, %s, %s, %s, %s, 0)", args)

        self.table.updateTable()
        self.uniformFrame.hide()


    def backAction(self):
        self.uniformFrame.hide()
        self.openStaffForm()