from collections import defaultdict

def comp_conifers(*conifers):
    entries=defaultdict(lambda:[None]*len(conifers))
    for i, conifer in enumerate(entries):
        for path, o_id in conifer.items():
            entries[path][i]=o_id
    for path, o_ids in entries.items():
        yield (path, *o_ids)

def diff_conf(c_from, c_to):
    output=''
    for path, o_from, o_to in comp_conifers(c_from, c_to):
        if o_from!=o_to:
            output+=f'Changed: {path}\n'
    return output