# This Python file uses the following encoding: utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget

from openvpn_service import OpenVPNService

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py
from ui_form import Ui_Widget

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.vpn = OpenVPNService()
        self.sessions_list: list[str] = []
        self.active_session_name: str = None
        self.disable_controls()
        self.ui.session_list_combo_box.currentIndexChanged.connect(self.on_session_list_combo_box_change)
        self.ui.session_on_push_button.clicked.connect(self.on_start_button_clicked)
        self.ui.session_off_push_button.clicked.connect(self.on_stop_button_clicked)
        self.initialize_sessions_list()

    def disable_controls(self):
        """Disable controls until a session is selected."""
        self.ui.session_off_push_button.setEnabled(False)
        self.ui.session_on_push_button.setEnabled(False)
        self.ui.status_switch_horizontal_slider.setEnabled(False)
        self.ui.session_list_combo_box.setEnabled(False)
        self.ui.session_logs.clear()
        self.ui.session_logs.setReadOnly(True)

    def update_session_controls(self):
        """Update session controls based on the selected session."""
        if (self.vpn.is_session_running(self.active_session_name)):
            self.ui.session_off_push_button.setEnabled(True)
            self.ui.status_switch_horizontal_slider.setEnabled(True)
            self.ui.status_switch_horizontal_slider.setValue(1)
            self.ui.session_logs.appendPlainText(f"Session '{self.active_session_name}' is running.")
        else:
            self.ui.session_on_push_button.setEnabled(True)
            self.ui.status_switch_horizontal_slider.setEnabled(True)
            self.ui.status_switch_horizontal_slider.setValue(0)
            self.ui.session_logs.appendPlainText(f"Session '{self.active_session_name}' is not running.")

    def initialize_sessions_list(self):
        """Initialize the sessions list."""
        sessions_list = self.vpn.get_session_configuration()
        if sessions_list:
            for session_path, session_data in dict(sessions_list).items():
                self.sessions_list.append(session_data["name"])

            self.ui.session_list_combo_box.addItems(self.sessions_list)
            self.ui.session_list_combo_box.setEnabled(True)
        else:
            print("No active sessions found.")

    def on_session_list_combo_box_change(self, index):
        """Handle session selection change."""
        if index == -1:
            return

        selected_session = self.sessions_list[index]
        self.active_session_name = selected_session
        self.ui.session_logs.clear()
        self.ui.session_logs.appendPlainText(f"Selected session: {selected_session}")
        self.update_session_controls()

    def on_start_button_clicked(self):
        self.vpn.start_session(self.active_session_name)
        self.update_session_controls()


    def on_stop_button_clicked(self):
        self.vpn.stop_session(self.active_session_name)
        self.update_session_controls()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
