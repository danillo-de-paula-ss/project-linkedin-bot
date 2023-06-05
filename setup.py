import os
from cx_Freeze import setup, Executable

path = os.path.dirname(__file__) + os.sep
# O que deve ser incluído na pasta final
FILES = [path + 'settings.txt']
INCLUDES = ['threading', 'os', 'sys', 'time', 'driver_settings']
PACKAGES = ['selenium']
EXCLUDES = ['tkinter']

# Saída de arquivos
config = Executable(
    script=path + 'main.py'
)

# Configurar o cx-freeze (detalhes do programa)
setup(
    name='Linkedin Bot',
    version='1.0.0',
    description='Bot para Linkedin',
    author='DanilloDePaula',
    options={'build_exe': {'include_files': FILES,
                           'packages': PACKAGES,
                           'includes': INCLUDES,
                           'excludes': EXCLUDES}},
    executables=[config]
)
