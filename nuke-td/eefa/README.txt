""""""""""""""""""""""""""""""""""""""""""""""""""""""
    __author__ = "Bardia Hassanzadeh"
    __copyright__ = "Copyright (C) 2024 EEFA VFX"
    __license__ = "Public Domain"
    __version__ = "1.0"
""""""""""""""""""""""""""""""""""""""""""""""""""""""
Setup EEFA Tools:

1. Place eefa directory in: <drive>:\Users\<user name>\.nuke\
2. Modify <drive>:\Users\<user name>\.nuke\menu.py:
If not already added, add the following lines

##Register EEFA Tools
from eefa.eefa_setup import setup_eefa_app
setup_eefa_app()

3. Run Nuke Studio
4. Scrips/Setup Nuke
5. EEFA Tools should now be added to the menu bar
