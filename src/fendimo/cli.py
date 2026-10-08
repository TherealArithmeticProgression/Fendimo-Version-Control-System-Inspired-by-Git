import argparse
import os
import subprocess
import sys
import textwrap

from fendimo import data
from fendimo import base


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
    channel_parser.add_argument('name') # name of channel/branch
    channel_parser.add_argument('start_point', default='@', type=o_id, nargs="?")

    return parser.parse_args()

def make(args):
    data.init()
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

def get_log(args):

    for o_id in base.iter_alts_and_ancestors({args.o_id}) #retrieve only the relevant argument (o_id) from the argumentspace
        alt=base.get_alter(o_id=o_id)
        print(f"Alt {o_id}")
        print(textwrap.indent(alt.message, "    ")) #four spaces for indents
        print('')

def checkout(args):
    base.checkout(args.alt_id)

def nameit(args):
    base.nameit(args.name, args.o_id)

def channel(args):
    base.make_channel(args.name, args.start_point)
    print(f"Channel: {args.name} made at {args.start_point[:10]}") #no point in depicting the entire hash of 64 characters, only 10 first characters will be kept
 
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
        if alt.ancestor:
            dot+=f'"{o_id}"->"{alt.ancestor}"\n'
    dot+='}'
    print(dot)

    with subprocess.Popen(
            ['dot', '-Tgtk', '/dev/stdin'],
            stdin=subprocess.PIPE) as proc:
        proc.communicate(dot.encode())

                         
                          
    