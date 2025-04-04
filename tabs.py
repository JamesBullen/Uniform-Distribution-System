from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QComboBox
from database import extractTable

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

        # Table view
        tableView = QVBoxLayout()
        tableButtons = QHBoxLayout()

        # Add new staffer
        self.newStaffButton = QPushButton('Add new Staffer', self)
        self.newStaffButton.clicked.connect(self.addStaff)
        tableButtons.addWidget(self.newStaffButton)
        
        # Table
        results = extractTable(self.pool, 'tbl_staff') # will use different function later
        self.table = Tables(results[1])
        tableView.addWidget(self.table)

        # Staff input form
        self.staffForm = QVBoxLayout()
        nameRow = QHBoxLayout()
        sexRow = QHBoxLayout()
        roleRow = QHBoxLayout()
        hoursRow = QHBoxLayout()
        staffButtons = QHBoxLayout()
        # Name row
        self.nameLabel = QLabel(self)
        self.nameLabel.setText('Fullname')
        self.nameInput = QLineEdit(self)
        nameRow.addWidget(self.nameLabel)
        nameRow.addWidget(self.nameInput)
        # Sex row
        self.sexLabel = QLabel(self)
        self.sexLabel.setText('Sex')
        self.sexInput = QComboBox(self)
        self.sexInput.addItems(['Male','Female'])
        sexRow.addWidget(self.sexLabel)
        sexRow.addWidget(self.sexInput)
        # Role row
        self.roleLabel = QLabel(self)
        self.roleLabel.setText('Role')
        self.roleInput = QLineEdit(self)
        roleRow.addWidget(self.roleLabel)
        roleRow.addWidget(self.roleInput)
        # Hours row
        self.hoursLabel = QLabel(self)
        self.hoursLabel.setText('Hours')
        self.hoursInput = QLineEdit(self)
        hoursRow.addWidget(self.hoursLabel)
        hoursRow.addWidget(self.hoursInput)
        # Buttons
        self.staffOkButton = QPushButton('Ok')
        self.staffOkButton.clicked.connect(self.staffOk)
        self.staffCancelButton = QPushButton('Cancel')
        self.staffCancelButton.clicked.connect(self.staffCancel)
        staffButtons.addWidget(self.staffOkButton)
        staffButtons.addWidget(self.staffCancelButton)

        self.staffForm.addLayout(nameRow)
        self.staffForm.addLayout(sexRow)
        self.staffForm.addLayout(roleRow)
        self.staffForm.addLayout(hoursRow)
        self.staffForm.addLayout(staffButtons)

        layout.addLayout(self.staffForm)

        self.setLayout(layout)

    def addStaff(self):
        # Clears form
        staffFields = [self.nameInput, self.sexInput, self.roleInput, self.hoursInput]
        for i in staffFields:
            i.clear()

        # Changes display
        self.table.hide()
        self.staffForm.show()
    
    def staffOk(self):
        ...
    
    def staffCancel(self):
        self.staffForm.hide()
        self.table.show()

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