import main_module
from main_module import *
import importlib

def reload_module():
	importlib.reload(main_module)
	exec("from main_module import *", globals())
