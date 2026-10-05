import os
import pathlib as Path
from fendimo import data

'''default directory is the root directory
Symbolic links are not permitted'''
def conifer(directory='.'):
    for entry in Path(directory).iterdir():
        if entry.is_file() and not entry.is_symlink():
            print(entry)
        elif entry.is_dir() and not entry.is_symlink():
            conifer(entry)


                