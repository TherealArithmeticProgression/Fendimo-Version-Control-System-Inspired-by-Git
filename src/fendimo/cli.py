import argparse
import os
import subprocess
import sys
import textwrap

from fendimo import data, base, diff, remote


def main():
    arg_parser=parse_args()
    arg_parser.func(arg_parser)

def parse_args():
    parser=argparse.ArgumentParser()
    required_commands=parser.add_subparsers(dest='required_commands')
    required_commands.required=True
    o_id=base.get_oid
    make_parser=required_commands.add_parser('make')
    make_parser.set_defaults(func=make)
    
    '''codesave is for producing the object's hash'''
    codesave_parser=required_commands.add_parser('codesave')
    codesave_parser.set_defaults(func=codesave)
    codesave_parser.add_argument('file', type=o_id)
    '''show will display the info shared at an object's hash'''
    show_parser=required_commands.add_parser('show')
    show_parser.set_defaults(func=show)
    show_parser.add_argument('show')
    '''conifer implements the functionality of write-tree'''
    conifer_parser=required_commands.add_parser('conifer')
    conifer_parser.set_defaults(func=conifer)
    '''read_conifer reads from a provided conifer'''
    read_conifer_parser=required_commands.add_parser('read_conifer')
    read_conifer_parser.set_defaults(func=read_conifer)
    read_conifer_parser.add_argument('conifer', type=o_id)
    '''alter is the equivalent of a git commit for fendimo'''
    alter_parser=required_commands.add_parser('alter')
    alter_parser.set_defaults(func=alter)
    alter_parser.add_argument('-m', '--message', required=True)
    '''get_log to get the logs of the each of the alter in code'''
    get_log_parser=required_commands.add_parser('get_log')
    get_log_parser.set_defaults(func=get_log)
    get_log_parser.add_argument('o_id', nargs='?', type=o_id, default='@') #nargs is for expected number of arguments
    '''checkout to point head to a previous alt'''
    checkout_parser=required_commands.add_parser('checkout')
    checkout_parser.set_defaults(func=checkout)
    checkout_parser.add_argument('alt_id')
    '''nameit parser to name an alt instead of using the hash value'''
    nameit_parser=required_commands.add_parser('nameit')
    nameit_parser.set_defaults(func=nameit)
    nameit_parser.add_argument('alt_id', nargs='?', type=o_id, default='@')
    '''C parser to see the alt history, and chronological build-up of project, akin to how gitk works'''
    C_parser=required_commands.add_parser('C')
    C_parser.set_defaults(func=C)
    '''channel parser to switch between changes (offers the functionality of branching offered by git)'''
    channel_parser = required_commands.add_parser('channel')
    channel_parser.set_defaults(func=channel)
    channel_parser.add_argument('name', nargs='?') # name of channel/branch
    channel_parser.add_argument('start_point', default='@', type=o_id, nargs="?")
    ''' info parser prints pivotal information about the current working directory (related to the current channel)'''
    info_parser=required_commands.add_parser('info')
    info_parser.set_defaults(func=info)
    info_parser.add_argument('alt_id', type=o_id)
    '''reset parser to set master and head on the same alt (any prev alts)'''
    reset_parser=required_commands.add_parser('reset')
    reset_parser.set_defaults(func=reset)
    reset_parser.add_argument('alt', type=o_id)
    '''show-alt parser to show only the alt's attached message'''
    show_alt_parser=required_commands.add_parser('show-alt')
    show_alt_parser.set_defaults(func=show_alt)
    show_alt_parser.add_argument('alt_id', nargs='?', default='@', type=o_id)
    '''changed parser to show the difference between the repository of last commit and current working directory'''
    changed_parser=required_commands.add_parser('changed')
    changed_parser.set_defaults(func=_changed)
    changed_parser.add_argument('alt', nargs='?', default='@')
    '''merge parser to merge two or more channels together'''
    merge_parser=required_commands.add_parser('merge')
    merge_parser.set_defaults(func=merge)
    merge_parser.add_argument("alt_id", type=o_id)
    '''merge_base parser to find the first common ancestor of two distinct channels'''
    merge_base_parser=required_commands.add_parser('merge_base')
    merge_base_parser.set_defaults(func=merge_base)
    merge_base_parser.add_argument('alt1', type=o_id)
    merge_base_parser.add_argument('alt2', type=o_id)
    '''go_get parser to fetch a remote directory to implementing fetching functionalities'''
    go_get_parser=required_commands.add_parser('go-get')
    go_get_parser.set_defaults(func=go_get)
    go_get_parser.add_argument('remote_dir')
    '''add parser helps in adding staging functionalities to the vcs'''
    add_parser=required_commands.add_parser('add')
    add_parser.set_defaults(func=add)
    add_parser.add_argument('files', nargs='+')

    return parser.parse_args()

def make(args):
    base.start()
    print(f"Initialized a fendimo directory at {os.getcwd()}/{data.DIRECTORY}")

def codesave(args):
    with open(args.file, 'rb') as f:
        print(data.hash_obj(f.read()))
        
def show(args):
    sys.stdout.flush()
    sys.stdout.buffer.write(data.get_obj(args.object, expected=None))

'''
Store current working directory to object database '''
def conifer(args):
    base.conifer()

def read_conifer(args):
    base.read_conifer(args.conifer)

def alter(args):
    print(base.alter(args.message))

##2.
def get_log(args):
    refs={}
    for ref_name, ref in data.iter_refs():
        refs.setdefault(ref.value, []).append(ref_name)
    for o_id in base.iter_alts_and_ancestors({args.o_id}): #retrieve only the relevant argument (o_id) from the argumentspace
        alt=base.get_alter(o_id=o_id)      

def checkout(args):
    base.checkout(args.alt_id)

def nameit(args):
    base.nameit(args.name, args.o_id)

##3.
def channel(args):
    if not args.name:
        current=base.get_channel_name()
        for channel in base.iter_channels():
            prefix="*" if channel==current else " "
            print(f"{prefix} {channel}")
    else:
        base.make_channel(args.name, args.start_point)
        print(f"A channel {args.name} was created starting at the alt {args.start_point[:10]}")

def merge(args):
    base.merge(args.alt_id)

def merge_base(args):
    print(base.merge_base(args.alt1, args.alt2))

def reset(args):
    base.reset(args.alt)

def C(args):
    dot='digraph alters{\n'
    o_ids=set()
    for ref_name, ref in data.iter_refs(deref=False):
        dot+=f'"{ref_name}" [shape=note]\n'
        dot+=f'"{ref_name}"->"{ref.value}"\n'
        if not ref.symbolic:
            o_ids.add(ref.value)

    for o_id in base.iter_alts_and_ancestors(o_ids):
        alt=base.get_alt(o_id)
        dot+=f'"{o_id}" [shape=box style=filled label="{o_id[:10]}"]\n'
        if alt.ancestors:
            for ancestor in alt.ancestors:
                dot+=f'"{o_id}"->"{ancestor}"\n'
    dot+='}'
    print(dot)

    with subprocess.Popen(
            ['dot', '-Tgtk', '/dev/stdin'],
            stdin=subprocess.PIPE) as proc:
        proc.communicate(dot.encode())

##3.
def info(args):
    if not args.alt_id:
        return
    alt=base.get_alt(args.alt_id)
    ancestor=None
    if alt.ancestors:
        ancestor=base.get_alt(alt.ancestors[0]).conifer
    show_alt(args.alt_id, alt)
    result=diff.diff_conf(base.get_conifer(ancestor), base.get_conifer(alt.conifer))
    sys.stdout.flush()
    sys.stdout.write(result)

def show_alt(args):
    HEAD=base.get_oid('@')
    channel=base.get_channel_name()
    if channel:
        print(f"On channel {channel}")
    else:
        print(f"Head detached at {HEAD[:10]}")
    MERGE_HEAD=base.get_alt('HEAD').value
    if MERGE_HEAD:
        print(f"Merging with {MERGE_HEAD[:10]}")
    print('\n Changes to be committed:\n')
    HEAD_tree=HEAD and base.get_alt(HEAD).name
    for path, action in diff.iter_changed_files(base.get_tree(HEAD_tree), base.get_pwc()):
        print(f"{action:>12}:{path}")

def _changed(args):
    conifer=args.alt and base.get_alt(args.alt).conifer
    result=diff.diff_conf(base.get_conifer(conifer), base.get_pwc())
    sys.stdout.flush()
    sys.stdout.write(result)

def _alt_printer(o_id, alt, refs=None):  #defaults to None to maintain compatibility with show_alt function                     
    refs_str=f'({", ".join(refs[o_id])})' if o_id in refs else ''
    print(f"Alt {o_id} {refs_str}\n")
    print(textwrap.indent(alt.message, "    ")) #four spaces for indents
    print('')                     

def go_get(args):
    remote.go_get(args.remote_dir)

def add(args):
    base.add(args.files)