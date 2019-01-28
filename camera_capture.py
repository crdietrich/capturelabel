"""Camera recording methods
Colin Dietrich 2019
"""

import os
import time
import atexit
import cv2
import numpy as np

from datetime import datetime

def _struct_time():
    t = datetime.now()
    return (t.year, t.month, t.day, t.hour,
            t.minute, t.second, t.microsecond)


def std_time_ms(str_format='{:02d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:06}'):
    """Get time in stardard format '%Y-%m-%d %H:%M:%S.%f' and accurate
    to the millisecond
    """
    t = _struct_time()
    st = str_format
    return st.format(t[0], t[1], t[2], t[3], t[4], t[5], t[6])


def file_time():
    """Get time in a format compatible with filenames,
    '%Y_%m_%d_%H_%M_%S_%f' and accurate to the second
    """
    t = _struct_time()
    st = '{:02d}_{:02d}_{:02d}_{:02d}_{:02d}_{:02d}_{:06}'
    return st.format(t[0], t[1], t[2], t[3], t[4], t[5], t[6])


class CAM:
    """Camera capture to file with timestamp"""

    def __init__(self, cam_id=0, description='default_cam'):
        """Initialize attributes

        Parameters
        ----------
        cam_id : int, camera id on computer
        descript : str, description of camera for file names
        """
        self.dev = cv2.VideoCapture(cam_id)
        self.description = description
        self.save_directory = ""

        self.quit = False
        self.sample_rate = 0

        self.out = None

        atexit.register(self.close)

    def set(self, n, value):
        """Passthrough to opencv.VideoCapture.set"""
        self.dev.set(n, value)

    def read_camera(self, verbose=False):
        """Read one image from the camera"""
        ret, frame = self.dev.read()
        if verbose:
            print(ret, frame)
        return ret, frame

    def write_image_file(self, label=None, verbose=False):
        """Write image to file with timestamp and description"""
        ret, frame = self.read_camera()
        ft = file_time()
        if label:
            img_name = "{}_{}_{}.png".format(label, self.description, ft)
        else:
            img_name = "{}_{}.png".format(self.description, ft)
        img_path = os.path.normpath(self.save_directory + img_name)
        if verbose:
            print("Saving to: {}".format(img_path))
        cv2.imwrite(img_path, frame)

    def stream_image_files(self, n=0, delay=0, stats=False):
        """Continuously write images to individual files

        Parameters
        ----------
        n : int, number of samples to take - 0 == infinite
        delay : int, delay in seconds between samples
        stats : bool, calculate frame rate
        """

        if delay == 0:
            def delayer():
                pass
        else:
            def delayer(delay):
                time.sleep(delay)
        m = 0
        t0 = 0
        if stats:
            t0 = time.time()
        while self.quit is False:
            self.write_image_file()
            delayer()
            m += 1
            if m == n:
                break
        if stats:
            self.sample_rate = n / (time.time()-t0)

    def record_video(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        ft = file_time()
        vid_name = "{}_{}.avi".format(self.description, ft)
        self.out = cv2.VideoWriter(vid_name, fourcc, 20.0, (640, 480))

        while self.dev.isOpened():
            ret, frame = self.dev.read()
            if ret:
                frame = cv2.flip(frame, 0)

                # write the flipped frame
                self.out.write(frame)

                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break

    def close(self):
        """Close connection to camera"""
        self.dev.release()
        try:
            self.out.release()
        except:
            pass
