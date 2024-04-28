from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QColorDialog
from PyQt5.QtGui import QColor
import subprocess
import os

class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.logCurrentThemeCSSLocation()

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
        colorDialog.setOption(QColorDialog.ShowAlphaChannel, True)

        initial_color = QColor(255, 255, 255, 255)
        color = colorDialog.getColor(initial_color, self, options=QColorDialog.ShowAlphaChannel)

        if color.isValid():
            rgba_color = f"rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})"
            print(rgba_color)
            sender.setStyleSheet(f"background-color: {rgba_color}")

    def logCurrentThemeCSSLocation(self):
        try:
            theme_name = subprocess.check_output(
                ['gsettings', 'get', 'org.cinnamon.theme', 'name'],
                universal_newlines=True
            ).strip().strip("'")
            
            theme_path = f"/usr/share/themes/{theme_name}/cinnamon/cinnamon.css"
            if os.path.exists(theme_path):
                print(f"Current theme's cinnamon.css located at: {theme_path}")
            else:
                print(f"No cinnamon.css found for the theme '{theme_name}' at the expected location.")
        except Exception as e:
            print(f"Failed to determine current theme: {e}")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    picker = ColorPicker()
    picker.show()
    sys.exit(app.exec_())
