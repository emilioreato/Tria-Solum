import subprocess
import sys


class Installer:

    libraries = [  # libraries to install because are needed to run the program
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
    def install_single_package(package):  # a func that runs a comand that install the librarie passed as parameter
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

    @staticmethod
    def install_libraries_from_list(list_of_libraries, installation_status_path):  # a func that installs all the libraries in the list passed as parameter
        for librarie in list_of_libraries:
            try:
                __import__(librarie)
                print(f"'{librarie}' is already installed.")
            except ImportError:
                Installer.install_single_package(librarie)
            with open(installation_status_path, 'a') as file:  # path was necesary as a parameter because  it writes in a file all the libraries it installs  and the ones that are already installed so then it can check it
                file.write(librarie + " installed\n")

    @staticmethod
    def check_libraries_installation_status(installation_status_path):  # a func that checks if all the libraries are installed and returns a list with the ones that are not installed
        not_installed_libraries = []
        with open(installation_status_path, 'r') as file:
            content = file.read().lower()
            for librarie in Installer.libraries:
                if not librarie in content:
                    print(librarie, "is missing.")
                    not_installed_libraries.append(librarie)
        return not_installed_libraries
