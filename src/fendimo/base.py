'''
Base file contains all vital components of fendimo (low-lying).
'''

import os
import pathlib as Path
from src.fendimo import data
from src.fendimo.exceptions import FendimoError, IncorrectInputError

'''default directory is the root directory
Symbolic links are not permitted'''
 
def make_conifer(directory='.'):
    entries=[]
    for entry in Path(directory).iterdir():
        if is_ignored(entry):
            continue
        if entry.is_file() and not entry.is_symlink():
            type_='blubber'
            with open(entry, "rb") as file:
                o_id=data.hash_obj(file.read())
        elif entry.is_dir() and not entry.is_symlink():
            type_='conifer'
            oid=make_conifer(entry)
        entries.append((type, o_id, entry.name))
    tree=''.join((f"{type_} {o_id} {entry.name}") for type_, o_id, entry in sorted(entries))
    return data.hash_obj(tree.encode(), 'tree')

# if .fend is in the path, then we don't show it in the output (don't show all contents of the central .fend folder)
def is_ignored(path):
    return ".fend" in path.split('/')

def iter_conifer(o_id):
    if not o_id:
        return
    conifer=data.get_obj(o_id, 'tree')
    for entry in conifer.decode().splitlines():
        type_,o_id, name=entry.split('',2)
        yield type_, o_id, name

def get_conifer(o_id, base_path=""):
    result={}
    for type_,name,o_id in iter_conifer(o_id):
        if '/' in name or name in ("..", "."):
            raise IncorrectInputError(f"The name of file '{name}' appears incorrect.")
        path=base_path+name
        if type_=='blubber':
            result[path]=o_id
        elif type_=='conifer':
            result.update(get_conifer(o_id, base_path=f"{path}/"))
        else:
            raise IncorrectInputError(f"The type {type_} is not recognized.")
    return result




def get_conifer(o_id, base_path=""):
    result={}
    for type_,oid,name in iter_conifer(o_id):
        if '/' in name or name in ('..','.'):
            raise IncorrectInputError(f"Incorrect name of file {name}")
        
        











def get_conifer(o_id, base_path=''):
    result={}
    for type_, o_id, name in get_conifer(o_id):
        if '/' in name or name in ("..", "."):
            raise IncorrectInputError("File name: '{name}' is incorrect.")
        path=base_path+name
        if type_=='blubber':
            result[path]=o_id
        elif type_=='conifer':
            result.update(get_conifer(o_id, f"{path}/"))
        else:
            assert False, f"Unknown entry of type {type_}"
        return result


                