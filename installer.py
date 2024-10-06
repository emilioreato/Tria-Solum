import subprocess
import sys

# libraries to install because are needed to run the program
libraries = [
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
    'pywin32',
    'string',
    'socket',
    'requests'
]


def install_package(package):
    print(f"Installing {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


for librarie in libraries:
    try:
        __import__(librarie)
        print(f"'{librarie}' is already installed.")
    except ImportError:
        install_package(librarie)
