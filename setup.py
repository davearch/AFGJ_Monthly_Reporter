from cx_Freeze import setup, Executable
import os.path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages = ["monthly_reporter"],
    include_files =  [],
    excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('monthly_reporter.py', base=base)
]

setup(name='afgj-monthly-reporter',
      version = '1.0',
      description = 'in-house program to move our monthly reports',
      options = dict(build_exe = buildOptions),
      executables = executables)
