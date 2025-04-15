import subprocess
import json
import webbrowser
# import threading

class OpenVPNService:
    def __init__(self):
        self.openvpn_cmd = "openvpn3"
        # self.stop_logging = threading.Event()

    def get_session_configuration(self):
        """Retrieve the list of active OpenVPN configurations."""
        try:
            result = subprocess.run(
                [self.openvpn_cmd, "configs-list", "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving sessions: \n{e.stderr}")
            return None

    def is_session_running(self, config_name):
        """Check if a specific OpenVPN session is running."""
        try:
            result = subprocess.run(
                [self.openvpn_cmd, "sessions-list"],
                capture_output=True,
                text=True,
                check=True
            )
            # Parse the output to find the session with the matching config name
            sessions = result.stdout.split("-----------------------------------------------------------------------------\n")
            for session in sessions:
                if f"Config name: {config_name}" in session and "Status: Connection, Client connected" in session:
                    return True
            return False
        except subprocess.CalledProcessError as e:
            print(f"Error checking session status: \n{e.stderr}")
            return False
    
    def start_session(self, config_name):
        """Start a new OpenVPN session using the given configuration name."""
        try:
            result = subprocess.run(
                [self.openvpn_cmd, "session-start", "--config", config_name, "--background"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Session started successfully: \n{result.stdout}")

            auth_result = subprocess.run(
                [self.openvpn_cmd, "session-auth"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Authentication status: \n{auth_result.stdout}")

            # Extract the authentication URL from the output
            auth_output = auth_result.stdout.splitlines()
            auth_url = None
            for line in auth_output:
                if "Authentication URL:" in line:
                    auth_url = line.split(":")[1].strip()
                    break
            
            if auth_url:
                print(f"Opening authentication URL: {auth_url}")
                webbrowser.open(auth_url)
            else:
                print("No authentication URL found in the session start output.")

        except subprocess.CalledProcessError as e:
            print(f"Error starting session: \n{e.stderr}")

    def stop_session(self, config_name):
        """Stop an active OpenVPN session by the given configuration name."""
        try:
            result = subprocess.run(
                [self.openvpn_cmd, "session-manage", "--config", config_name, "-D"],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"Session stopped successfully: \n{result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Error stopping session: {e.stderr}")

    def get_session_stats(self, config_name):
        """Retrieve statistics for a specific OpenVPN Configuration name.."""
        try:
            result = subprocess.run(
                [self.openvpn_cmd, "session-stats", "--config", config_name, "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving session logs: \n{e.stderr}")
            return None
        
    def get_session_logs(self, config_name):
        """Retrieve logs for a specific OpenVPN Configuration name.."""
        try:
            result = subprocess.run(
                [self.openvpn_cmd, "session-log", "--config", config_name, "--log-level", "1"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving session logs: \n{e.stderr}")
            return None