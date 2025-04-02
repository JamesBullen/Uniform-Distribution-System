import sys
from PyQt6.QtWidgets import QApplication, QWidget

# Creates the application
app = QApplication([])

# Creates a window
window = QWidget()
window.show()

# Starts event loop
sys.exit(app.exec())