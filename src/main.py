from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QColorDialog
from PyQt5.QtGui import QColor

class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Color Picker')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.buttons = {
            "top": QPushButton('Top Panel Color'),
            "bottom": QPushButton('Bottom Panel Color'),
            "left": QPushButton('Left Panel Color'),
            "right": QPushButton('Right Panel Color'),
        }

        for button in self.buttons.values():
            button.clicked.connect(self.openColorDialog)
            self.layout.addWidget(button)

    def openColorDialog(self):
        color = QColorDialog.getColor()

        if color.isValid():
            print(color.name())

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    picker = ColorPicker()
    picker.show()

    sys.exit(app.exec_())