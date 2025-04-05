from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox, QMessageBox, QErrorMessage, QFrame
from database import extractTable
from mysql.connector import connect, pooling, Error

class Tables(QWidget):
    def __init__(self, headers):
        super().__init__()
        layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        layout.addWidget(self.table)
        self.setLayout(layout)

class StaffTab(QWidget):
    def __init__(self, pool):
        super().__init__()
        self.pool = pool
        layout = QVBoxLayout()

        # Buttons
        tableButtons = QHBoxLayout()
        # Add new staffer
        self.newStaffButton = QPushButton('Add new Staffer', self)
        self.newStaffButton.clicked.connect(self.openStaffForm)
        tableButtons.addWidget(self.newStaffButton)

        layout.addLayout(tableButtons)
        
        # Table
        results = extractTable(self.pool, 'tbl_staff') # will use different function later
        self.table = Tables(results[1])
        layout.addWidget(self.table)

        #* Staff input form
        self.staffLayout = QGridLayout()
        self.staffFrame = QFrame()
        labelCol = QVBoxLayout()
        inputCol = QVBoxLayout()
        staffButtons = QHBoxLayout()
        # Name row
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Fullname')
        self.nameInput = QLineEdit(self)
        labelCol.addWidget(self.nameLabel)
        inputCol.addWidget(self.nameInput)
        # Sex row
        self.sexLabel = QLabel(self)
        self.sexLabel.setText('Sex')
        self.sexInput = QComboBox(self)
        self.sexInput.addItems(['Male','Female'])
        self.sexInput.setCurrentIndex(-1)
        labelCol.addWidget(self.sexLabel)
        inputCol.addWidget(self.sexInput)
        # Role row
        self.roleLabel = QLabel(self)
        self.roleLabel.setText('Role')
        self.roleInput = QComboBox(self)
        roleResults = extractTable(self.pool, 'tbl_roles')[0]
        self.roleInput.addItems([i[1] for i in roleResults])
        self.roleInput.setCurrentIndex(-1)
        labelCol.addWidget(self.roleLabel)
        inputCol.addWidget(self.roleInput)
        # Hours row
        self.hoursLabel = QLabel(self)
        self.hoursLabel.setText('Hours')
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
        self.sizesResults = extractTable(self.pool, 'tbl_sizes')[0]
        # Button options
        self.finishButton = QPushButton('Finish')
        self.finishButton.clicked.connect(lambda: print('test'))
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
        # validation checks will go hear, will see about a switch case for different validation errors
        try:
            staffFields = [self.nameInput.text(), self.sexInput.currentText()[0], self.roleInput.currentIndex()+1, self.hoursInput.text()]
        except:
            QMessageBox.warning(self, 'Missing values', "All fields must be filled correctly")
            return

        try:
            # Connect to pool
            connection = self.pool.get_connection()
            # Open cursor and runs fetch query
            cursor = connection.cursor()
            query = "call AddNewStaff(%s, %s, %s, %s)"
            cursor.execute(query, staffFields)
            result = cursor.fetchall()

            # Close cursor and return connection to pool
            cursor.close()
            connection.close()
        except Error as e:
            print(f"Error: {e}")
            errorMessage = QErrorMessage()
            errorMessage.showMessage(f"Error: {e}")
            return
        
        self.staffFrame.hide()
        self.generateUniformForm(result)
    
    def cancelAction(self):
        self.staffFrame.hide()
        self.clearStaffForm()

    def clearStaffForm(self):
        self.nameInput.clear()
        self.sexInput.setCurrentIndex(-1)
        self.roleInput.setCurrentIndex(-1)
        self.hoursInput.clear()

    def generateUniformForm(self, uniforms):
        if self.uniformCol.children():
            print('has children')
        else:
            print('no children')
        
        # Setup for loop
        labelDict = {1:None, 2:None, 3:None, 4:None}
        inputDict = {1:None, 2:None, 3:None, 4:None}

        # Dynamically creates size fields for each uniform type
        for i in range(0, len(uniforms)):
            labelDict[i] = QLabel()
            labelDict[i].setText(uniforms[i][0])
            self.uniformCol.addWidget(labelDict[i])

            sizeOptions = self.sizesResults[uniforms[i][3]][1]
            print(sizeOptions)

            inputDict[i] = QComboBox()
            inputDict[i].addItems(sizeOptions.split(','))
            self.sizeCol.addWidget(inputDict[i])

        self.uniformFrame.show()

    def finishAction(self):
        self.clearStaffForm()

    def backAction(self):
        self.uniformFrame.hide()
        self.openStaffForm()
    
    def updateTable(self):
        ...

class OrdersTab(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel(f"<h1>{text}</h1>")
        layout.addWidget(self.label)

        self.setLayout(layout)

class ReportsTab(QWidget):
    def __init__(self, text):
        super().__init__()
        layout = QVBoxLayout()

        self.label = QLabel(f"<h1>{text}</h1>")
        layout.addWidget(self.label)

        self.setLayout(layout)