from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QMessageBox, QFrame
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

        #* Staff input form
        self.staffLayout = QGridLayout()
        self.staffFrame = QFrame()
        labelCol = QVBoxLayout()
        inputCol = QVBoxLayout()
        staffButtons = QHBoxLayout()
        # Name row
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Full Name:')
        self.nameInput = QLineEdit(self)
        labelCol.addWidget(self.nameLabel)
        inputCol.addWidget(self.nameInput)
        # Sex row
        self.sexLabel = QLabel(self)
        self.sexLabel.setText('Sex:')
        self.sexInput = QComboBox(self)
        self.sexInput.addItems(['Male','Female'])
        self.sexInput.setCurrentIndex(-1)
        labelCol.addWidget(self.sexLabel)
        inputCol.addWidget(self.sexInput)
        # Role row
        self.roleLabel = QLabel(self)
        self.roleLabel.setText('Role:')
        self.roleInput = QComboBox(self)
        roleResults = getValidtionTable('tbl_roles')
        self.roleInput.addItems([i[1] for i in roleResults])
        self.roleInput.setCurrentIndex(-1)
        labelCol.addWidget(self.roleLabel)
        inputCol.addWidget(self.roleInput)
        # Hours row
        self.hoursLabel = QLabel(self)
        self.hoursLabel.setText('Hours:')
        self.hoursInput = QLineEdit(self)
        labelCol.addWidget(self.hoursLabel)
        inputCol.addWidget(self.hoursInput)
        # Buttons
        self.nextButton = QPushButton('Next')
        self.nextButton.clicked.connect(self.nextAction)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelAction)
        staffButtons.addWidget(self.nextButton)
        staffButtons.addWidget(self.cancelButton)

        #* Size form
        self.uniformLayout = QGridLayout()
        self.uniformFrame = QFrame()
        self.uniformCol = QVBoxLayout()
        self.sizeCol = QVBoxLayout()
        self.uniformButtons = QHBoxLayout()
        self.sizesResults = getValidtionTable('tbl_sizes')
        # Button options
        self.finishButton = QPushButton('Finish')
        self.finishButton.clicked.connect(self.finishAction)
        self.backButton = QPushButton('Back')
        self.backButton.clicked.connect(self.backAction)
        self.uniformButtons.addWidget(self.finishButton)
        self.uniformButtons.addWidget(self.backButton)
        # Add everything to layout
        self.uniformLayout.addLayout(self.uniformCol, 0, 0)
        self.uniformLayout.addLayout(self.sizeCol, 0, 1)
        self.uniformLayout.addLayout(self.uniformButtons, 1, 0, 1, 2)
        self.uniformFrame.setLayout(self.uniformLayout)

        self.staffLayout.addLayout(labelCol, 0, 0)
        self.staffLayout.addLayout(inputCol, 0, 1)
        self.staffLayout.addLayout(staffButtons, 1, 0, 1, 2)
        self.staffFrame.setLayout(self.staffLayout)

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
        for i in self.labelDict:
            if self.labelDict[i]:
                self.uniformCol.removeWidget(self.labelDict[i])
                self.sizeCol.removeWidget(self.inputDict[i])
        
        # Resets for loop
        self.labelDict = {1: None, 2: None, 3: None, 4: None}
        self.inputDict = {1: None, 2: None, 3: None, 4: None}

        # Dynamically creates size fields for each uniform type
        for i in range(0, len(uniforms)):
            self.labelDict[i] = QLabel()
            self.labelDict[i].setText(uniforms[i][0])
            self.uniformCol.addWidget(self.labelDict[i])

            sizeOptions = self.sizesResults[uniforms[i][3]-1][1]

            self.inputDict[i] = QComboBox()
            self.inputDict[i].addItems(sizeOptions.split(','))
            self.sizeCol.addWidget(self.inputDict[i])

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