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
from fendimo import diff
from fendimo.exceptions import UnrecognizedArgumentError, IncorrectInputError, FendimoError

'''default directory is the root directory
Symbolic links are not permitted'''

alt=namedtuple('alt', ['conifer', 'ancestors', 'message'])

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

##3.
def read_merged_conifers(c_base, c_head, c_other):
    _empty_current_directory()
    for path, blubber in diff.merge_conifs(get_conifer(c_base), get_conifer(c_head), get_conifer(c_other)).items():
        os.makedirs(f"{os.path.dirname(path)}", exist_ok=True)
        with open(path, "wb") as f:
            f.write(blubber)

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
    
    ALT+=f"Conifer {get_conifer()}\n"
    HEAD=data.get_ref('HEAD').value
    if HEAD:
        ALT+=f"Head Alt {HEAD}\n" #this is the object id of the head pointer
    MERGE_HEAD=data.get_ref('MERGE_HEAD').value
    if MERGE_HEAD:
        ALT+=f'ancestor {MERGE_HEAD}\n'
    ALT+='\n'
    ALT+=f"{message}\n"
    o_id= data.hash_obj(ALT.encode(), 'alt=')
    data.set_ref('HEAD', data.refValue(symbolic=False, value=o_id))
    return o_id

def get_alt(o_id):
    ancestors=[]
    alt=data.get_obj(o_id, 'alt').decode()
    lines=iter(alt.splitlines())
    for line in itertools.takewhile(operator.truth, lines):
        key, value = line.split(' ', 1)
        if key=='conifer':
            conifer=value
        elif key=='ancestor':
            ancestors.append(value)
        else:
            assert UnrecognizedArgumentError(f"Unknown field {key}")
    message='\n'.join(lines)
    return alt(conifer=conifer, ancestors=ancestors, message=message) #update to get new values

##2.
def get_pwc():
    result={}
    for root,_, filenames in os.walk("."):
        for filename in filenames:
            path=os.path.relpath(f"{root}/{filename}")
            if not os.path.isfile(path) or is_ignored(path):
                continue
            with open(path, "rb") as file:
                result[path]=data.hash_obj(file.read())
    return result 

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
        o_ids.extendleft(alt.ancestors[:1])
        o_ids.extend(alt.ancestors[1:])

##5.
def merge(other_id):
    HEAD=data.get_ref('HEAD').value
    if not HEAD:
        raise ValueError
    merge_base=merge_base(other_id, HEAD)
    a_other=get_alt(other_id)
    if not a_other:
        raise IncorrectInputError(f"No alt with the ID {other_id[:10]}... recognized.")
    if merge_base==HEAD:
        read_conifer(a_other.conifer)
        data.set_ref('MERGE_HEAD', data.ref_val(symbolic=False, value=other_id))
        print("Fast-forward merge occured.")
        return 
    data.set_ref('MERGE_HEAD', data.ref_val(symbolic=False, value=other_id))
    a_base=get_alt(merge_base)
    a_head=get_alt(HEAD)
    read_conifer(a_head.conifer, a_other.conifer)
    print("Merged to present working conifer \n Make an alt to proceed safely.")

# chronology lost in set, but retained in generator-type output of
# iter_alts_and_ancestors({alt_id2}) 
# and it makes sure the first common ancestor is returned
##2.
def merge_base(alt_id1, alt_id2):
    ancestors1=set(iter_alts_and_ancestors({alt_id1}))
    for o_id in iter_alts_and_ancestors({alt_id2}):
        if o_id in ancestors1:
            return o_id


def add(file_names):
    '''
    ## add file and corresponding object id in the index

    Accepts a parameter ```filenames``` to be added in the index.

    '''
    def add_file(file_name):
        with data.get_idx() as idx:
                file=os.path.relpath(file_name)
                with open(file, 'w') as f:
                    # $$ 
                    idx[file_name]=data.hash_obj(f.read())
    def add_dir(dir_name):
        for root, _, file_names in os.walk(dir_name):
            for file_name in file_names:
                path=os.path.relpath(file_name)
                if is_ignored(path) or not os.path.isfile(path):
                    continue
                add_file(path)

    with data.get_idx() as idx:
        for entity_name in file_names:
            if os.path.isfile(entity_name):
                add_file(entity_name)
            elif os.path.isdir(entity_name):
                add_dir(entity_name)


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

def is_related_to(alt, ref):
    return ref in iter_alts_and_ancestors({alt})

'''accessibility functions - END'''