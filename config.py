"""Configuration settings for camera functions
Colin Dietrich 2019
"""
from sys import platform

# ===== File Saving Location =====
if platform == "linux" or platform == "linux2":
    data_dir = "/home/user/labeled_images/"
    stream_dir = "/home/colin/data/stream_images/"
elif platform == "darwin": # OS X
	pass
elif platform == "win32":
    data_dir = "C:\\Users\\user\\labeled_images\\"
    stream_dir = "C:\\Users\\user\\stream_images\\"

# ===== File Save Naming =====
# this will be included in the file name so keep it short
description = "label"

# ===== GUI CSS =====
default_button_css = ("font: bold;"+
			   "font-size: 45px;" +
			   "height: 48px;" +
			   "width: 120px;"
			   )
# ===== Button Names for Class Labels =====
buttons = {"joint": default_button_css,
           "clear_concrete": default_button_css,
           "clear_asphalt": default_button_css,
           "horizontal_crack": default_button_css,
           "uplift": default_button_css,
		   "settling": default_button_css,
		   "vault_lid": default_button_css,
		   "vertical_crack": default_button_css,
		   "alligator_crack": default_button_css,
           "brick/cobble": default_button_css,
		   "other": default_button_css
		   }
		   #"background-image: url('81x100_rabbit.png');"+default_css}

# ===== Camera =====
# Select camera to access,
# this depends on computer and number of cameras installed.
# If there is only a USB camera, camera_id = 0
camera_id = 1
