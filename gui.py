"""Qt windows for camera controlled labeling
Colin Dietrich 2019
"""

from functools import partial
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QWidget, QApplication
# import everything, since it's hard to remember what class does what
from PyQt5.QtWidgets import QMainWindow,\
    QApplication, QLabel, QLineEdit, QPushButton,\
    QHBoxLayout, QVBoxLayout, QGroupBox, QFrame, QGridLayout, QAction

import config
from camera_capture import CAM


cam = CAM(cam_id=config.camera_id, description=config.description)
cam.save_directory = config.data_dir

class Window(QWidget):
    def __init__(self, mapping):
        QWidget.__init__(self)
        layout = QVBoxLayout(self)
        self.buttons = []
        for key, value in mapping.items():
            #text_label, image = value[0], value[1]
            q_push_button = QPushButton(key, self)
            #q_push_button.setStyleSheet("background-image: url({});".format(value))
            q_push_button.setStyleSheet(value)
            self.buttons.append(q_push_button)
            self.buttons[-1].clicked.connect(partial(handleButton, data=key))
            layout.addWidget(self.buttons[-1])

def handleButton(self, data="\n"):
    cam.write_image_file(data, verbose=True)
    print(data)
