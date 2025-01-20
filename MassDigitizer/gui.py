from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton

class CustomDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Dialog")

        layout = QVBoxLayout()
        label = QLabel("This is a custom dialog")
        layout.addWidget(label)

        button = QPushButton("Close")
        button.clicked.connect(self.close)
        layout.addWidget(button)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication([])
    dialog = CustomDialog()
    dialog.exec()
