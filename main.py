import os
import subprocess

# Paths
ui_file = "form.ui"
generated_ui_file = "ui_form.py"
widget_file = "widget.py"

# Check if the UI file has been updated
def is_ui_file_updated():
    if not os.path.exists(generated_ui_file):
        return True
    ui_file_mtime = os.path.getmtime(ui_file)
    generated_ui_file_mtime = os.path.getmtime(generated_ui_file)
    return ui_file_mtime > generated_ui_file_mtime

# Generate the Python file from the UI file if needed
if is_ui_file_updated():
    print(f"Generating {generated_ui_file} from {ui_file}...")
    try:
        subprocess.run(["pyside6-uic", ui_file, "-o", generated_ui_file], check=True)
        print(f"{generated_ui_file} has been successfully generated.")
    except subprocess.CalledProcessError as e:
        print(f"Error while generating {generated_ui_file}: {e}")
        exit(1)

# Run the widget.py file
print(f"Running {widget_file}...")
try:
    subprocess.run(["python", widget_file], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error while running {widget_file}: {e}")
    exit(1)