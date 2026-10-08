"""
Module-level doc string
This file (data.py) will initialize a folder 
in the repository titled .fend, mimicking git's .git creation.
"""
import hashlib
import os
from collections import namedtuple

DIRECTORY=".fend"
'''create a typedef struct in Python called ref_val which has the attributes symbolic/value.'''
ref_val=namedtuple('Ref_Value',['symbolic','value'])

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

def set_ref(ref, alt_id, deref=True):
    if alt_id.symbolic:
        raise ValueError
    ref=_get_ref_internal(ref, deref)[0]
    ref_path=f"{DIRECTORY}/{ref}"
    os.makedirs(os.path.dirname(ref_path), exist_ok=False) 
    with open(ref_path, "w") as file:
        file.write(alt_id.value)

# .strip() will make sure there are no lingering white spaces/ tab spaces

def get_ref(ref):
    return _get_ref_internal(ref, deref)[1]
    
def _get_ref_internal(ref, deref):
    ref_path=f"{DIRECTORY}/{ref}"
    value=None
    if os.path.isfile(ref_path):
        with open(ref_path) as file:
            value= file.read().strip() #default: ref_path opens in read text mode
    symbolic=bool(value) and value.startswith('ref:')
    if symbolic:
        value=value.split(':', 1)[1].strip()
        if deref:
            return _get_ref_internal(value, deref=True)
    return ref, ref_val(symbolic=symbolic, value=value)


def iter_refs(deref=True):
    refs=['@']
    for root, _, filenames in os.walk(f'{DIRECTORY}/refs/'):
        root=os.path.relpath(root, DIRECTORY)
        refs.extend(f"{root}/{name}" for name in filenames)

    for refname in refs:
        yield refname, get_ref(refname, deref=deref)

