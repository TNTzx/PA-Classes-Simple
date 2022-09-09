"""Contains disk utilities."""


import os
import subprocess

import base64


ENCODING = "UTF-8"


def override_file(folder_path: str, filename: str, data: str | bytes, binary: bool = False):
    """Creates or overwrites the file in the path with the data."""
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    full_path = os.path.join(folder_path, filename)

    if not binary:
        with open(full_path, "wt", encoding = ENCODING) as file:
            file.write(data)
    else:
        with open(full_path, "wb") as file:
            file.write(data)


def make_folder_path(path: str):
    """Makes a folder path."""
    os.mkdir(path)


def read_file(file_path: str, binary: bool = False):
    """Returns the file contents."""
    if not binary:
        with open(file_path, "r", encoding = ENCODING) as file:
            return file.read()
    else:
        with open(file_path, "rb") as file:
            return file.read()

def path_exists(file_path: str):
    """Returns `True` if the file or folder exists, `False` otherwise."""
    return os.path.exists(file_path)


def get_all_file_paths_in_folder(folder: str, recursive: bool = False):
    """Returns a list of file paths of every file in a folder."""
    paths = [os.path.join(folder, name) for name in os.listdir(folder)]

    file_paths = []
    folder_paths = []

    for path in paths:
        if os.path.isfile(path):
            file_paths.append(path)
        else:
            folder_paths.append(path)

    paths = file_paths
    if recursive:
        if len(folder_paths) == 0:
            return paths

        inside_folder_paths = [get_all_file_paths_in_folder(folder_path, recursive) for folder_path in folder_paths]
        inside_folder_paths_combined = []
        for inside_folder_path in inside_folder_paths:
            inside_folder_paths_combined += inside_folder_path

        paths = paths + inside_folder_paths_combined

    return paths


FILE_BROWSER_PATH = os.path.join(os.getenv("WINDIR"), "explorer.exe")

def open_folder_in_explorer(folder_path: str):
    """Opens the folder in explorer."""
    folder_path = os.path.normpath(folder_path)
    subprocess.run([FILE_BROWSER_PATH, folder_path], check = False)

def open_file_in_explorer(file_path: str):
    """Opens the file in explorer."""
    file_path = os.path.normpath(file_path)
    subprocess.run([FILE_BROWSER_PATH, "/select", file_path], check = False)


def bytes_to_base64(bytes_data: bytes):
    """Returns the base64 representation of bytes."""
    return base64.b64encode(bytes_data).decode(ENCODING)

def base64_to_bytes(base64_data: str):
    """Returns the bytes representation of a base64 string."""
    return base64.b64decode(base64_data.encode(ENCODING))
