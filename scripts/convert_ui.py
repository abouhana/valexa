#!/usr/bin/env python

import os
from subprocess import call


def convert_all_ui_files():
    gui_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../valexa/gui/")

    for filename in os.listdir(gui_dir):
        if is_ui_file(filename):
            input_path = os.path.join(gui_dir, filename)
            output_path = os.path.join(gui_dir, filename.replace(".ui", ".py"))
            call(["pyuic5", input_path, "-o", output_path])


def is_ui_file(filename: str) -> bool:
    try:
        return filename.split('.')[1] == "ui"
    except IndexError:
        return False

if __name__ == '__main__':
    convert_all_ui_files()
