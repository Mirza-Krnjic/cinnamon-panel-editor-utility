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

        for name, button in self.buttons.items():
            button.clicked.connect(self.openColorDialog)
            self.layout.addWidget(button)

    def openColorDialog(self):
        sender = self.sender()
        colorDialog = QColorDialog(self)
        colorDialog.setOption(QColorDialog.ShowAlphaChannel, True)  # Enable alpha channel in the dialog

        initial_color = QColor(255, 255, 255, 255)  # default white and fully opaque
        color = colorDialog.getColor(initial_color, self, options=QColorDialog.ShowAlphaChannel)

        if color.isValid():
            rgba_color = f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})"
            print(rgba_color)  # Print the color with alpha value
            sender.setStyleSheet(f"background-color: {rgba_color}")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    picker = ColorPicker()
    picker.show()
    sys.exit(app.exec_())
