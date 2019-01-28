"""Main script for running camera controlled labeling
Colin Dietrich 2019
"""
import sys
from PyQt5.QtWidgets import QApplication

import config
import gui


app = QApplication(sys.argv)
window = gui.Window(config.buttons)
window.show()
sys.exit(app.exec_())
