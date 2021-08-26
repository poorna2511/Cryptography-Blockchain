# Imported below Libs for GUI
from PyQt5.QtWidgets import *

# Import UI for main window
import UI     

import sys

 # MAIN()
App = QApplication(sys.argv)
ui = UI.MainWindow()

status = App.exec_()
sys.exit(status)
