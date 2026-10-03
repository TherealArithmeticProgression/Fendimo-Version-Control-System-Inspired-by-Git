"""
Module-level doc string
This file (data.py) will initialize a folder 
in the repository titled .fend, mimicking git's .git creation.
"""
import os

DIRECTORY=".fend"

def init():
    os.makedirs(DIRECTORY)