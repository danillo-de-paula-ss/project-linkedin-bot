import os
import sys
from cx_Freeze import setup, Executable

path = os.path.dirname(__file__) + os.sep
# O que deve ser incluído na pasta final
FILES = []
INCLUDES = ['threading', 'os', 'sys', 'time', 'argparse', 'pyperclip', 'random', 'pickle', 'traceback', 'unicodedata']
PACKAGES = ['webdriver_manager', 'selenium', 'PySimpleGUI', 'cryptography', 'pyperclip', 'utilities']
EXCLUDES = []

base = None
# if (sys.platform == "win32"):
#     base = "Win32GUI"    # Tells the build script to hide the console.

# Saída de arquivos
config = Executable(
    script=path + 'bot_linkedin.py',
    base=base
)

# Configurar o cx-freeze (detalhes do programa)
setup(
    name='bot_linkedin',
    version='1.1.0',
    description='Bot para Linkedin',
    author='DanilloDePaulaSS',
    options={'build_exe': {'include_files': FILES,
                           'packages': PACKAGES,
                           'includes': INCLUDES,
                           'excludes': EXCLUDES}},
    executables=[config]
)
