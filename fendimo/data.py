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

'''
Helps you read the file/object stored at a hash value.
Don't run with python -o -m pytest otherwise this won't work as expected.
'''
def get_obj(o_id, expected='blubber'):
    with open(f"{DIRECTORY}/objects/{o_id}", "rb") as file:
        obj=file.read()

    type_,_,content=obj.partition(b"\x00")
    type_=type_.decode()
    if expected is not None:
        assert type_==expected, f"Expected {expected}, got {type_} instead"
    return content
