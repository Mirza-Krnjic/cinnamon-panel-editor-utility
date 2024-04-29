from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QColorDialog, QMessageBox
from PyQt5.QtGui import QColor
import subprocess
import os
import re
import subprocess
from PyQt5.QtCore import QCoreApplication
import tempfile


class ColorPicker(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300, 200)
        self.initUI()

    def initUI(self):
        from PyQt5.QtGui import QIcon

        self.setWindowTitle('Cinnamon Panel Editor')
        self.setWindowIcon(QIcon('/cinnamon-panel-editor/usr/share/icons/cinnamon-panel-editor-icon.png')) 
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
        print("this is the text that the function gets: ", panel)
        print("refactored: ", 'panel-'+panel)

        css_path = self.get_current_theme_css_path()
        if css_path:
            try:
                with open(css_path, 'r') as file:
                    css_content = file.read()


                pattern = re.compile(
                    r'(\.' + re.escape('panel-'+panel) + r'\b\s*\{[^}]*\})',
                    re.DOTALL
                    )

                css_class_match = pattern.search(css_content)
                if css_class_match:
                    css_class = css_class_match.group(1)
                    
                    # Check if 'background-color' property exists
                    if 'background-color:' in css_class:
                        updated_css_class = re.sub(
                            r'background-color:\s*[^;]+;',
                            f'background-color: {color} !important;',
                            css_class
                        )
                    else:
                        # Append 'background-color' if it doesn't exist
                        updated_css_class = css_class.rstrip('}') + f'  background-color: {color} !important;\n}}'

                    updated_css_content = css_content.replace(css_class, updated_css_class)

                    # Create a temporary file with the updated CSS content
                    with tempfile.NamedTemporaryFile(delete=False, mode='w') as temp_file:
                        temp_file.write(updated_css_content)

                    # Use pkexec to move the temporary file to the original location
                    cmd = ['pkexec', 'mv', temp_file.name, css_path]
                    subprocess.run(cmd, check=True)

                    QMessageBox.information(self, "Restart Required", 
                        "Please restart your computer or switch themes to apply the new panel color. Click OK to dismiss this message.")
                else:
                    print(f"No CSS class found for {panel}")

            except Exception as e:
                print(f"Failed to update CSS file for {panel} panel: {e}")
                if 'temp_file' in locals():
                    os.remove(temp_file.name)  # Clean up the temporary file
            finally:
                # Ensure the temporary file is cleaned up if it exists
                if 'temp_file' in locals() and os.path.exists(temp_file.name):
                    os.remove(temp_file.name)



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    picker = ColorPicker()
    picker.show()
    app.exec_()
