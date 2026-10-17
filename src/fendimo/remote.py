from fendimo import data
from fendimo import base
import os

REMOTE_REFS='refs/heads/'
LOCAL_REFS='refs/remote/'

##4.
def go_get(remote_dir):
    print(f"Going to the get the directory at: {remote_dir}")
    refs=_get_this_remote(remote_dir=remote_dir, prefix=REMOTE_REFS)
    for o_id in base.iter_alts_and_ancestors(refs.values()):
        data.fetch_obj_if_missing(o_id, remote_dir=remote_dir)
    for refname, value in refs.items():
        refname=os.path.relpath(remote_dir, REMOTE_REFS)
        data.set_ref(f"{LOCAL_REFS}/{refname}", data.set_ref(symbolic=False, value=value))

##3.
def _get_this_remote(remote_dir, prefix=''):
    '''
        Input - A remote directory path, and a prefix path present 
                inside the remote directory path.
        Output - (Dict) Iters through files in remote dir, under the given prefix.
    '''
    with data.change_fend_dir(remote_dir):
        return {refname:ref.value for refname, ref in data.iter_refs(prefix)}

##2.
def put(remote_path, ref_name):
    '''
    ## fendimo put is a good alternative to git push
    
    you can pass two parameters to the put function: 
    
    - ```remote_path``` contains path to be checked in remote directory
    - ```ref_name``` is the name of reference in consideration
    
    the reference name will be checked at remote and local sources. If the reference
    name is present, the local reference and remote reference should be related to each other.
    Or, at least the remote reference should be missing (a new alt/commit in the repository).
    
    XXX relies on shutil so compatibility with Mac is curtailed.
    '''
    remote_refs=_get_this_remote(remote_dir=remote_path)
    remote_ref=remote_refs.get(ref_name) #get the value corresponding to refname from remote references
    local_ref=data.get_ref(ref_name).value
    assert local_ref
    assert not remote_ref or base.is_related_to(local_ref, remote_ref) 
    known_remote_refs=filter(data.obj_exists, remote_refs.values())
    # filter() = if it says no, remove the object
    remote_objs=set(base.iter_alts_and_ancestors({known_remote_refs}))
    local_objs=set(base.iter_alts_and_ancestors({local_ref}))
    objs_to_put=local_objs-remote_objs
    for o_id in objs_to_put:
        data.put_obj(o_id, remote_path)
    with data.change_fend_dir(remote_path):
        data.set_ref(ref_name, data.ref_val(symbolic=False, value=local_ref))
    


