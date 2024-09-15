import os
import subprocess
import platform


def create_virtualenv():
    print("Creating virtual environment...")
    subprocess.run(["python", "-m", "venv", "venv"], check=True)

def install_dependencies():
    print("Installing dependencies...")
    pip_path = os.path.join("venv", "Scripts", "pip") if platform.system() == "Windows" else os.path.join("venv", "bin", "pip")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)

def create_executable():
    print("Creating executable...")

    # Check the operating system and use the correct path for PyInstaller
    if platform.system() == "Windows":
        pyinstaller_path = os.path.join("venv", "Scripts", "pyinstaller.exe")
    else:
        pyinstaller_path = os.path.join("venv", "bin", "pyinstaller")

    # Check if resources directory exists and handle the packaging
    resources_dir = os.path.join("utils", "resources")
    if os.path.exists(resources_dir):
        print("Including resources in the executable.")
        subprocess.run([pyinstaller_path, "--onefile", "--windowed", "app.py", "--add-data", f"{resources_dir}{os.pathsep}utils/resources"], check=True)
    else:
        print("Warning: Resources folder not found. Proceeding without resources.")
        subprocess.run([pyinstaller_path, "--onefile", "--windowed", "app.py"], check=True)

if __name__ == "__main__":
    create_virtualenv()
    install_dependencies()
    create_executable()
    print("Setup complete. Executable can be found in the 'dist' folder.")
