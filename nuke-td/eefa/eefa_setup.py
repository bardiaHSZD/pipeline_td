import importlib.util
import nuke
import os
import sys

script_directory = os.path.dirname(os.path.realpath(__file__))
app_path = os.path.join(script_directory, 'eefa_tools.py')

def run_app():
    spec = importlib.util.spec_from_file_location("app", app_path)
    app = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app)
    print("Entered")
    app.initiate()

def setup_eefa_app():    
    nuke.menu("Nuke").addCommand("Scripts/Setup EEFA", run_app, 'alt+l')
