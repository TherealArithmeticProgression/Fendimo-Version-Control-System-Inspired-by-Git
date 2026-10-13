import subprocess
from collections import defaultdict
from tempfile import NamedTemporaryFile as temp
from fendimo import data

def comp_conifers(*conifers):
    entries=defaultdict(lambda:[None]*len(conifers))
    for i, conifer in enumerate(entries):
        for path, o_id in conifer.items():
            entries[path][i]=o_id
    for path, o_ids in entries.items():
        yield (path, *o_ids)

##2.
def iter_changed_files(c_from, c_to):
    for path, o_from, o_to in comp_conifers(c_from, c_to):
        if o_from!=o_to:
            action=('New file' if not o_from else
                    'Deleted' if not o_to else
                    'Modified')
        yield path, action        

def diff_conf(c_from, c_to):
    output=b''
    for path, o_from, o_to in comp_conifers(c_from, c_to):
        if o_from!=o_to:
            output+=diff_blubber(o_from, o_to, path)
    return output


def diff_blubber(o_from, o_to, path='blubber'):
    with temp() as f_from, temp() as f_to:
        for o_id, f in ((o_from, f_from),(o_to,f_to)):
            if o_id:
                f.write(o_id)
                f.flush()
        # function will stop executing until the process communicates the required output
        # to the function, then the function will return
        # the output obtained.
        # without "unified" mode the +/- signs won't be visible
        # and you can get the clunky coordinates instead
        # user will see the {path} instead of a temporary file when you do a/path / b/path
        # with PIPE python catches the output
        with subprocess.Popen(['diff','--unified','--show-c-function',
                               '--label', f'a/{path}', f_from.name,
                               '--label', f'b/{path}', f_to.name],stdout=subprocess.PIPE) as proc:
            output,_=proc.communicate()
        # this stays _, because it is responsible for catching stderrors, 
        # which will be empty unless we write stderr=subprocess.PIPE as well.
    return output

# MERGE TYPE FUNCTIONS

##2.
def merge_conifs(c_head, c_other):
    merged={}
    for path, o_head, o_ther in comp_conifers(c_head, c_other):
        merged[path]=merge_blubbers(o_head=o_head, o_ther=o_ther)
    return merged

def merge_blubbers(o_base, o_head, o_ther):
    with temp() as f_base, temp() as f_head, temp() as f_ther:
        for o_id, f in ((o_base, f_base),(o_head,f_head) (o_ther, f_ther)):
            if o_id:
                f.write(data.get_obj(o_id))
                f.flush()

    # diff3 can give th return codes 0/1/2/... 0=merge with no conflicts, 1=merge with conflicts
    # code=2... ->some bad error happened. we need to avoid this output.
    with subprocess.Popen(['diff3', '-m',"-L",'HEAD',f_head.name, '-L','BASE', f_base.name, '-L', 'MERGE_HEAD', f_ther.name], stdout=subprocess.PIPE) as proc:
        output, _ = proc.communicate()
        if proc.returncode not in (0,1):
            raise SystemError
        

    return output

