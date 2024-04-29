#!/bin/bash
# Usage: ./modify_cinnamon_css.sh "new_css_content"

# Get the current theme name
theme_name=$(gsettings get org.cinnamon.theme name | tr -d "'")

# Construct the path to the cinnamon.css file for the current theme
css_file_path="/usr/share/themes/${theme_name}/cinnamon/cinnamon.css"

# Check if the file exists
if [ -f "$css_file_path" ]; then
    # If the file exists, overwrite it with the new content
    echo "$1" > "$css_file_path"
else
    # If the file doesn't exist, print an error message
    echo "Error: No such file $css_file_path"
fi