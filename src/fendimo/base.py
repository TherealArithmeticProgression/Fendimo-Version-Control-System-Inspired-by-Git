'''
Base file contains all vital components of fendimo (low-lying).
'''
'''NamedTuple can have elements accessed by using names instead of just indices.'''
import os
import pathlib as Path
import itertools
import operator
from collections import namedtuple, deque
import string
from fendimo import data
from fendimo.exceptions import UnrecognizedArgumentError, IncorrectInputError, FendimoError

'''default directory is the root directory
Symbolic links are not permitted'''

alt=namedtuple('alt', ['conifer', 'ancestor', 'message'])

def start():
    data.start()
    data.set_ref('HEAD', data.ref_val(symbolic=False, value='refs/heads/master'))

def make_channel(name, start_point):
    data.set_ref(f"refs/heads/{name}", data.ref_val(symbolic=False, value=start_point))

def get_channel_name():
    HEAD=data.get_ref('HEAD', deref=False)
    if not HEAD.symbolic:
        return None
    if not HEAD.startswith('refs/heads'):
        raise IncorrectInputError
    return os.path.relpath(HEAD, 'refs/heads')

##2.
def is_channel(name):
    return data.get_ref(f'refs/heads/{name}').value is not None

def iter_channels():
    for ref_name in data.iter_refs('refs/heads'):
        yield os.path.relpath(ref_name, 'refs/heads/')

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

def iter_conifer(o_id):
    if not o_id:
        return
    conifer=data.get_obj(o_id, 'tree')
    for entry in conifer.decode().splitlines():
        type_,o_id, name=entry.split('',2)
        yield type_, o_id, name

'''commits in git are connected and linked, the head points to the current commit. 
A similar structure would be implemented on fendimo.'''
'''
Alt carries link to previous head (ancestor alter)'''
def alt(message):
    
    commit+=f"Conifer {get_conifer()}\n"
    ancestor=data.get_ref('HEAD').value
    if ancestor:
        commit+=f"Head Alt {ancestor}\n" #this is the object id of the head pointer
    commit+='\n'
    commit+=f"{message}\n"
    o_id= data.hash_obj(commit.encode(), 'alt=')
    data.set_ref('HEAD', data.refValue(symbolic=False, value=o_id))
    return o_id

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



def checkout(name):
    alt_id=get_oid(name)
    alt=get_alt(alt_id)
    get_conifer(alt.conifer)
    if is_channel(name):
        HEAD=data.ref_val(symbolic=True, value=f"refs/heads/{name}")
    else:
        HEAD=data.ref_val(symbolic=False, value=alt_id)
    data.set_ref('HEAD', HEAD, deref=False)

def reset(o_id):
    data.set_ref('HEAD', data.ref_val(symbolic=False, value=o_id))

def nameit(name, alt_id):
    data.set_ref(f'refs/tags/{name}', data.ref_val(symbolic=False, value=alt_id))

def iter_alts_and_ancestors(o_ids):
    o_ids=deque(o_ids)
    visited=set()
    while o_ids:
        o_id=o_ids.popleft()
        if not o_id or o_id in visited:
            continue
        visited.add(o_id)
        yield o_id
        alt=get_alt(o_id)
        o_ids.appendleft(alt.ancestor)


'''accessibility functions - START'''   
# if .fend is in the path, then we don't show it in the output (don't show all contents of the central .fend folder)
def is_ignored(path):
    return ".fend" in path.split('/')
# get object ID from the passed down name 

def get_oid(name):
    if name=='@' : name='HEAD'
    
    try_these=[f"{name}",
                 f"refs/{name}",
                 f"refs/heads/{name}",
                 f"refs/tags/{name}"]
    
    for try_this in try_these:
        if data.get_ref(try_this, deref=False).value:
            return data.get_ref(try_this).value

    is_hex=all(c in string.hexdigits for c in name)
    if len(name)==64 and is_hex:
        return name #case when we have an o_id in our hands already, then that o_id doesn't have an o_id, and we return it as-is.
    else:
        assert IncorrectInputError(f"Name {name} encountered is unknown.")

def _empty_current_directory():
    current_dir=Path.cwd()
    for path in sorted(current_dir.rglob("*"), key=lambda p:len(p.parts), reverse=True):
        try:
            relativePath=Path.relative_to(current_dir)
        except ValueError:
            continue
        if is_ignored(str(relativePath)):
            continue
        try:
            os.rmdir(path)
        except(FileNotFoundError, OSError):
            pass

'''accessibility functions - END'''