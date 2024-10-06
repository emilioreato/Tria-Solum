import subprocess
import sys


class Installer:

    modules = [  # modules to install because are needed to run the program
        'copy',
        'pygame',
        'time',
        'numpy',
        'pygame_gui',
        'os',
        'pyautogui',
        'ctypes',
        'math',
        'random',
        'threading',
        'wave',
        'pyaudio',
        'media',
        'pywin32',  # for win32con and win32api
        'string',
        'socket',
        'requests'
    ]

    @staticmethod
    def install_single_package(package):  # a func that runs a comand that install the module passed as parameter
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    @staticmethod
    def install_modules_from_list(list_of_modules, installation_status_path):  # a func that installs all the modules in the list passed as parameter
        for module in list_of_modules:
            try:
                __import__(module)
                print(f"'{module}' is already installed.")
            except ImportError:
                Installer.install_single_package(module)
            with open(installation_status_path, 'a') as file:  # path was necesary as a parameter because  it writes in a file all the modules it installs  and the ones that are already installed so then it can check it
                file.write(module + " installed\n")

    @staticmethod
    def check_modules_installation_status(installation_status_path):  # a func that checks if all the modules are installed and returns a list with the ones that are not installed
        not_installed_modules = []
        with open(installation_status_path, 'r') as file:
            content = file.read().lower()
            for module in Installer.modules:
                if not module in content:
                    print(module, "is missing.")
                    not_installed_modules.append(module)
        return not_installed_modules
