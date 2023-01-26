import os
import shutil
from sys import platform

if platform == "win32":
    os.system('pyinstaller --noconfirm --onedir --windowed --clean --add-data "data;data/" --add-data "img;img/" --add-data "txt;txt/" --name "SimulationChernobyl" "main.py"')
else:
    os.system('python -m PyInstaller --noconfirm --onedir --windowed --clean --add-data "data;data/" --add-data "img;img/" --add-data "txt;txt/" --name "SimulationChernobyl" "main.py"')

os.remove('SimulationChernobyl.spec')
shutil.rmtree('build')
shutil.rmtree('__pycache__')
shutil.copytree('dist/', './', dirs_exist_ok=True)
shutil.rmtree('dist')

# to fix: windows not accepting png
# --icon "img/icon.png"
