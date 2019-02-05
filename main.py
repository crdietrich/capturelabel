"""Main script for running camera controlled labeling
Colin Dietrich 2019
"""
import sys
from PyQt5.QtWidgets import QApplication

import config


if sys.argv[1] == 's':
    from camera_capture import CAM
    cam = CAM(cam_id=config.camera_id, description=config.description)
    cam.save_directory = config.stream_dir
    cam.stream_image_files(n=0, delay=0, stats=False)
else:
    import gui
    app = QApplication(sys.argv)
    window = gui.Window(config.buttons)
    window.show()
    sys.exit(app.exec_())
