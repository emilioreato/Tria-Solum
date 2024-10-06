import subprocess
import ctypes
import sys


class FirewallRules:

    def __init__(self) -> None:
        pass

    def get_admin_permitions():  # Restarts the script with administrator permissions so the firewall con be modified.

        def is_admin():  # Checks if the script is running with administrator permissions.
            try:
                return ctypes.windll.shell32.IsUserAnAdmin()
            except:
                return False

        if not is_admin():
            # If not admin, restart the script with admin permissions
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, ' '.join(sys.argv), None, 1)
            sys.exit()  # Exit after starting the new process

    def rule_exists(rule_name):
        # Check for both inbound and outbound rules
        inbound_rule_name = f"{rule_name}Inbound"
        outbound_rule_name = f"{rule_name}Outbound"

        try:
            # Check Inbound Rule
            command_inbound = f'Get-NetFirewallRule -DisplayName "{inbound_rule_name}"'
            result_inbound = subprocess.run(['powershell', '-Command', command_inbound], capture_output=True, text=True)

            if result_inbound.returncode == 0:
                return True

            # Check Outbound Rule
            command_outbound = f'Get-NetFirewallRule -DisplayName "{outbound_rule_name}"'
            result_outbound = subprocess.run(['powershell', '-Command', command_outbound], capture_output=True, text=True)

            if result_outbound.returncode == 0:
                return True

            # If both checks fail, the rule does not exist
            return False

        except subprocess.CalledProcessError as e:
            print("Error executing PowerShell command:", e)
            return False

    def add_firewall_rule(port, rule_name, direction):
        try:
            command = f'New-NetFirewallRule -DisplayName "{rule_name}" -Direction {direction} -Protocol TCP -LocalPort {port} -Action Allow'
            subprocess.run(['powershell', '-Command', command], check=True)
            print(f"Rule '{rule_name}' added to the firewall to allow port {port} in direction {direction}.")
        except subprocess.CalledProcessError as e:
            print("Error adding the rule to the firewall:", e)

    def check_firewall_installation_status(path, port):  # THIS METHOD IS MADE FOR THIS SPECIFIC GAME. but its useful anyway
        with open(path, 'r') as archivo:  # Small code that creates a firewall rule if it has not been created yet. the state of the creation is saved on rules.txt
            if not "yes" in archivo.read():
                print("creating")
                FirewallRules.get_admin_permitions()
                rule_name = "GambitGameRule"
                if not FirewallRules.rule_exists(rule_name):
                    FirewallRules.add_firewall_rule(port, rule_name + "Inbound", "Inbound")
                    FirewallRules.add_firewall_rule(port, rule_name + "Outbound", "Outbound")
                with open(path, 'w') as archivo:
                    archivo.write('yes')
            else:
                print("already")
