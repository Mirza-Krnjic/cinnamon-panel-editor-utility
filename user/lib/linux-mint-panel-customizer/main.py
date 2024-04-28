from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QColorDialog
from PyQt5.QtGui import QColor
import subprocess
import os
import re

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
            self.update_css_file(sender.text().split(' ')[0].lower(), rgba_color)  # update CSS file based on button

    def get_current_theme_css_path(self):
        try:
            theme_name = subprocess.check_output(
                ['gsettings', 'get', 'org.cinnamon.theme', 'name'],
                universal_newlines=True
            ).strip().strip("'")
            
            theme_path = f"/usr/share/themes/{theme_name}/cinnamon/cinnamon.css"
            if os.path.exists(theme_path):
                return theme_path
            else:
                print(f"No cinnamon.css found for the theme '{theme_name}' at the expected location.")
                return None
        except Exception as e:
            print(f"Failed to determine current theme: {e}")
            return None

    def update_css_file(self, panel, color):
        css_path = self.get_current_theme_css_path()
        if css_path:
            try:
                with open(css_path, 'r+') as file:
                    css_content = file.read()
                    pattern = re.compile(r'(\.' + re.escape(panel) + r'\s*\{\s*[^}]*\})')
                    css_class = pattern.search(css_content).group(1)
                    updated_css_class = re.sub(r'(background-color:.*?;)', '', css_class)
                    updated_css_class += f'  background-color: {color} !important;'
                    updated_css_content = pattern.sub(updated_css_class, css_content)
                    file.seek(0)
                    file.write(updated_css_content)
                    file.truncate()
            except Exception as e:
                print(f"Failed to update CSS file for {panel} panel: {e}")

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    picker = ColorPicker()
    picker.show()
    sys.exit(app.exec_())
