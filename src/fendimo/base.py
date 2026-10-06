'''
Base file contains all vital components of fendimo (low-lying).
'''
'''NamedTuple can have elements accessed by using names instead of just indices.'''
import os
import pathlib as Path
import itertools
import operator
from collections import namedtuple
from src.fendimo import data
from src.fendimo.exceptions import UnrecognizedArgumentError, IncorrectInputError, FendimoError

'''default directory is the root directory
Symbolic links are not permitted'''
alt=namedtuple('alt', ['conifer', 'ancestor', 'message'])

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

'''commits in git are connected and linked, the head points to the current commit. 
A similar structure would be implemented on fendimo.'''
'''
Alt carries link to previous head (ancestor alter)'''
def alt(message):
    commit+=f"Conifer {get_conifer()}\n"
    commit+=f"Head Alt {data.get_ha()}\n" #this is the object id of the head pointer
    commit+='\n'
    commit+=f"{message}\n"
    o_id= data.hash_obj(commit.encode(), 'alt=')
    data.set_HEAD(o_id)
    return o_id
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


def get_alt(o_id):
    ancestor=None
    alt=data.get_obj(o_id, 'alt').decode()
    lines=iter(alt.splitlines())
    for line in itertools.takewhile(operator.truth, lines):
        key, value = line.split(' ', 1)
        if key=='conifer':
            conifer=value
        elif key=='ancestor':
            ancestor=value
        else:
            assert UnrecognizedArgumentError(f"Unknown field {key}")
    message='\n'.join(lines)
    return alt(conifer=conifer, ancestor=ancestor, message=message) #update to get new values

def get_conifer(o_id, base_path=""):
    result={}
    for type_,oid,name in iter_conifer(o_id):
        if '/' in name or name in ('..','.'):
            raise IncorrectInputError(f"Incorrect name of file {name}")
        path=base_path+name 
        if type_=='blubber':
            result[path]=oid
        elif type_=='conifer':
            result.update(get_conifer(oid, base_path=f"{path}"))
        else:
            raise (f"Object of type {type_} not recognized.")
    return result

def read_conifer(conifer_oid):
    _empty_current_directory()
    for path, o_oid in get_conifer(o_id=conifer_oid, base_path='./').items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(data.get_obj(o_oid))

def _empty_current_directory():
    current_dir=Path.cwd()
    for path in sorted(current_dir.rglob("*"), key=lambda p:len(p.parts), reverse=True):
        try:
            relativePath=path.relative_to(current_dir)
        except ValueError:
            continue
        if is_ignored(str(relativePath)):
            continue
        try:
            os.rmdir(path)
        except(FileNotFoundError, OSError):
            pass