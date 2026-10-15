from fendimo import data
import os

REMOTE_REFS='refs/heads/'
LOCAL_REFS='refs/remote/'

##3. CLOGGED
def go_get(remote_dir):
    print(f"Going to the get the directory at: {remote_dir}")
    refs=_get_this_remote(remote_dir=remote_dir, prefix=REMOTE_REFS)
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