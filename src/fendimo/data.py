"""
Module-level doc string
This file (data.py) will initialize a folder 
in the repository titled .fend, mimicking git's .git creation.

"""
from contextlib import contextmanager
import hashlib
import os
import json 
import shutil #shutil is used for directory management tasks, such as moving/deleting/copying
from collections import namedtuple

DIRECTORY=None
@contextmanager
def change_fend_dir(new_dir):
    # __enter___
    global DIRECTORY # mandatory to declare it as global if we're assigning it a new value inside the function
                    # otherwise, python will think DIRECTORY is a local variable.
    old_dir=DIRECTORY
    DIRECTORY=f'{new_dir}/.fend'
    yield
    # __exit___ (cause you saw yield, now leave)
    DIRECTORY=old_dir
'''create a typedef struct in Python called ref_val which has the attributes symbolic/value.'''
ref_val=namedtuple('Ref_Value',['symbolic','value'])

def start():
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

def put_obj(o_id, remote_path):
    '''
    ## underlying code for pushing objects from local to remote source.
    
    Inputs:

    - ```o_id``` is the object ID, to be pushed onto the remote source.
    - ```remote_path``` is the path at which the output is directed to.

    XXX Curtailed compatibility for Mac Device. 
    '''
    remote_path+='/.fend'
    shutil.copy(f"{DIRECTORY}/objects/{o_id}", f"{remote_path}/objects/{o_id}")


def set_ref(ref, alt_id, deref=True):
    
    ref=_get_ref_internal(ref, deref)[0]
    if not deref.value:
        assert ValueError
    if deref.symbolic:
        value=f'ref: {deref.value}'
    else:
        value=deref.value
    ref_path=f"{DIRECTORY}/{ref}"
    os.makedirs(os.path.dirname(ref_path), exist_ok=False) 
    with open(ref_path, "w") as file:
        file.write(value)

# .strip() will make sure there are no lingering white spaces/ tab spaces

def get_ref(ref, deref=True):
    return _get_ref_internal(ref, deref)[1]

##3.
def delete_ref(ref, deref=True):
    ref=_get_ref_internal(ref, deref)[0]
    os.remove(f"{DIRECTORY}/{ref}")

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

##3.
def iter_refs(prefix="",deref=True):
    refs=['@']
    for root, _, filenames in os.walk(f'{DIRECTORY}/refs/'):
        root=os.path.relpath(root, DIRECTORY)
        refs.extend(f"{root}/{name}" for name in filenames)

    for refname in refs:
        if not refname.startswith(prefix):
            continue
        yield refname, get_ref(refname, deref=deref)

def obj_exists(o_id):
    return os.path.isfile(f"{DIRECTORY}/objects/{o_id}")

def fetch_obj_if_missing(o_id, remote_dir):
    if obj_exists(o_id=o_id):
        return 
    remote_dir+='/.fend'
    shutil.copy(f"{remote_dir}/objects/{o_id}", f"{DIRECTORY}/objects/{o_id}")

##2.
@contextmanager
def get_idx():
    idx={}
    idx_f=f'{DIRECTORY}/idx'
    if os.path.isfile(idx_f):
        with open(idx_f) as f:
            idx=json.load(f)

    yield idx

    with open(idx_f, 'w') as f:
        json.dump(idx, f)

