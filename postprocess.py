"""Post processing for labeled image collections
Colin Dietrich 2019
"""

import os
import cv2
import pandas as pd


def inventory_files(source_filepath, verbose=False):
    """Inventory all files recursively in one directory"""
    filepath = []
    filename = []
    for (directory, dnames, fnames) in os.walk(source_filepath):
        for f in fnames:
            filepath.append(os.path.join(directory, f))
            filename.append(f)
    df = pd.DataFrame({'source_filepath': filepath,
                       'filename': filename})
    return df

def class_id(filename, class_list):
    """Create list of class ids from filenames,
    assumes a class id is present in the filename string.
    """

    for i in class_list:
        if i in filename:
            return i
    return 'undefined'

def inventory_flow(source_filepath, class_list, verbose=False):
    """Prepare a directory for Keras ImageDataGenerator.flow_from_dataframe
    """
    df = inventory_files(source_filepath, verbose=verbose)
    df['class_id'] = df.filename.apply(lambda x: class_id(x, class_list))
    return df

def crop_resize(source_filepath, destination_filepath,
                x1=0, x2=-1, y1=0, y2=-1,
                h=224, w=224,
                verbose=False):
    """Crop and resize pictures and save to a new directory

    Parameters
    ----------
    scr : source folder
    dst : destination folder
    n0 : int, index of first image in dir
    n1 : int, index of last image in dir
    h : int, new height
    w : int, new width
    """
    if verbose:
        print(source_filepath)
    img = cv2.imread(source_filepath)
    img_cropped = img[y1:y2, x1:x2]
    img_resized = cv2.resize(img_cropped, (h, w))
    cv2.imwrite(destination_filepath, img_resized)

def crop_resize_flow(source_directory, destination_directory, class_list,
                     x1=0, x2=-1, y1=0, y2=-1,
                     h=224, w=224,
                     save=False,
                     verbose=False):
    """Crop and resize pictures, save to a new directory and
    generate a Pandas Dataframe of labels for
    Keras ImageDataGenerator.flow_from_dataframe method.

    Parameters
    ----------
    source_filepath : source folder
    destination_filepath : destination folder
    x1 : int lower x index to crop to
    x2 : int upper x index to crop to
    y1 : int lower y index to crop to
    y2 : int upper y index to crop to
    h : int, new height in pixels
    w : int, new width in pixels
    """

    if not os.path.isabs(destination_directory):
        destination_directory = os.path.abspath(destination_directory)

    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    df = inventory_flow(source_directory, class_list, verbose=verbose)
    df['destination_filepath'] = destination_directory + os.path.sep + df.filename
    _ = df.apply(lambda x: crop_resize(x.source_filepath,
                                   x.destination_filepath,
                                   x1=x1, x2=x2, y1=y1, y2=y2,
                                   h=h, w=w, verbose=verbose),
                                   axis=1)
    if save:
        df.to_pickle(path=destination_directory + os.path.sep + "flow_dataframe.pkl")
    return df
