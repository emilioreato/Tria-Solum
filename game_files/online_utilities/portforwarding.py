import subprocess
import os
import time


"""
COMANDS BEING EXECUTED. 

start the app
upnpc-static.exe -s

shows stats:
upnpc-static.exe -l

open port:
upnpc-static.exe -a {your local ip} {port} {port} TCP

close opened port:
upnpc-static.exe -d {port} TCP
"""


class Portforwarding:

    upnpc_tool = "upnpc\\upnpc-static.exe"
    upnpc_tool_absolute_path = os.path.dirname(os.path.abspath(__file__))+"\\"+upnpc_tool
    # print(upnpc_tool_absolute_path)

    def __init__(self) -> None:
        pass

    @staticmethod
    def execute_command(comand):
        try:
            result = subprocess.run(comand, shell=True, capture_output=True, text=True)
            if result.stderr:
                print(f"Error executing comand '{comand}': {result.stderr}")
            return result.stdout
        except Exception as e:
            print(f"An error ocurred executing comand '{comand}': {str(e)}")
            return None

    @staticmethod
    def initialize():
        Portforwarding.execute_command(f"{Portforwarding.upnpc_tool_absolute_path} -s")

    @staticmethod
    def open_port(local_ip, local_port, external_port, protocol):  # Opens a port using miniupnpc compiled exe
        print("Opening port...")
        result = Portforwarding.execute_command(f'"{Portforwarding.upnpc_tool_absolute_path}" -a {local_ip} {local_port} {external_port} {protocol}')
        if result:
            print(result)
        time.sleep(1.5)  # wait to make sure the port gets opened correctly

    @staticmethod
    def check_ports(port):
        print("Cheking open ports...")
        result = Portforwarding.execute_command(f"{Portforwarding.upnpc_tool_absolute_path} -l")
        if str(port) in result:
            print("The specified port is already opened")
            return True
        print("The port specified is not opened.")
        return False  # this means the port has not be opened yet

    @staticmethod
    def close_port(port):
        print("closing specified port...")
        Portforwarding.execute_command(f"{Portforwarding.upnpc_tool_absolute_path} -d {port} TCP")
