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
        self.newStaffButton.clicked.connect(self.addStaff)
        tableButtons.addWidget(self.newStaffButton)

        layout.addLayout(tableButtons)
        
        # Table
        results = extractTable(self.pool, 'tbl_staff') # will use different function later
        self.table = Tables(results[1])
        layout.addWidget(self.table)

        # Staff input form
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
        self.staffOkButton = QPushButton('Ok')
        self.staffOkButton.clicked.connect(self.staffOk)
        self.staffCancelButton = QPushButton('Cancel')
        self.staffCancelButton.clicked.connect(self.staffCancel)
        staffButtons.addWidget(self.staffOkButton)
        staffButtons.addWidget(self.staffCancelButton)

        self.staffLayout.addLayout(labelCol, 0, 0)
        self.staffLayout.addLayout(inputCol, 0, 1)
        self.staffLayout.addLayout(staffButtons, 1, 0, 1, 2)
        self.staffFrame.setLayout(self.staffLayout)
        #layout.addWidget(self.staffFrame)

        self.setLayout(layout)

    def addStaff(self):
        # Clears form
        self.nameInput.clear()
        self.sexInput.setCurrentIndex(-1)
        self.roleInput.setCurrentIndex(-1)
        self.hoursInput.clear()

        # Changes display
        self.staffFrame.show()
    
    def staffOk(self):
        # validation checks will go hear, will see about a switch case for different validation errors
        try:
            staffFields = [self.nameInput.text(), self.sexInput.currentText()[0], self.roleInput.currentIndex()+1, self.hoursInput.text()]
        except:
            QMessageBox.warning(self, 'Validtion', "All fields must be filled correctly")
            return

        try:
            # Connect to pool
            connection = self.pool.get_connection()
            # Open cursor and runs fetch query
            cursor = connection.cursor()
            query = "call AddNewStaff(%s, %s, %s, %s)"
            cursor.execute(query, staffFields)
            result = cursor.fetchall()
        except Error as e:
            print(f"Error: {e}")
            errorMessage = QErrorMessage()
            errorMessage.showMessage(f"Error: {e}")
            return
        
        self.staffFrame.hide()
        self.generateUniformForm()
    
    def staffCancel(self):
        self.staffFrame.hide()

    def generateUniformForm():
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