#!F:\RogerRelocated\Documents\newcombiner\venv\Scripts\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'mdv==1.7.4','console_scripts','mdv'
__requires__ = 'mdv==1.7.4'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('mdv==1.7.4', 'console_scripts', 'mdv')()
    )
