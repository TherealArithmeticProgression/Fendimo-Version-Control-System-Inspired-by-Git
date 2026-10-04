import os

from fendimo import data

'''default directory is the root directory
Symbolic links are not permitted'''
def conifer(directory='.'):
    with os.scandir(directory) as this:
        for entry in this:
            full=f"{directory}/{entry.name}"
            if entry.is_file(follow_symlinks=False):
                print(full)
            elif entry.is_dir(follow_symlinks=False):
                