"""
Module-level doc string
This file (data.py) will initialize a folder 
in the repository titled .fend, mimicking git's .git creation.
"""
import hashlib
import os

DIRECTORY=".fend"

def init():
    os.makedirs(DIRECTORY)
    os.makedirs(f"{DIRECTORY}/objects")

def hash_obj(data):
    o_id=hashlib.sha256(data).hexdigest()
    with open(f"{DIRECTORY}/objects/{o_id}", "wb+") as out:
        out.write(data)
    return o_id
