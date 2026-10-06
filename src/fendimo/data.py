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

def hash_obj(data, type_='blubber'):
    obj=type_.encode()+b'\x00'+data
    o_id=hashlib.sha256(obj).hexdigest()
    with open(f"{DIRECTORY}/objects/{o_id}", "wb") as out:
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

def set_ref(ref, alt_id):
    ref_path=f"{DIRECTORY}/{ref}"
    os.makedirs(os.path.dirname(ref_path), exist_ok=False) 
    with open(ref_path, "w") as file:
        file.write(alt_id)

# .strip() will make sure there are no lingering white spaces/ tab spaces
def get_ref(ref):
    ref_path=f"{DIRECTORY}/{ref}"
    if os.path.isfile(ref_path):
        with open(ref_path) as file:
            file.read().strip() #default: ref_path opens in read text mode


