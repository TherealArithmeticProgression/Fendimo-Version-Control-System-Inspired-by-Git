import argparse
import os
import sys
import textwrap
from src.fendimo import data
from src.fendimo import base


def main():
    arg_parser=parse_args()
    arg_parser.func(arg_parser)

def parse_args():
    parser=argparse.ArgumentParser()
    required_commands=parser.add_subparsers(dest='required_commands')
    required_commands.required=True
    make_parser=required_commands.add_parser('make')
    make_parser.set_defaults(func=make)
    '''codesave is for producing the object's hash'''
    codesave_parser=required_commands.add_parser('codesave')
    codesave_parser.set_defaults(func=codesave)
    codesave_parser.add_argument('file')
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
    read_conifer_parser.add_argument('conifer')
    '''alter is the equivalent of a git commit for fendimo'''
    alter_parser=required_commands.add_parser('alter')
    alter_parser.set_defaults(func=alter)
    alter_parser.add_argument('-m', '--message', required=True)
    '''get_log to get the logs of the each of the alter in code'''
    get_log_parser=required_commands.add_parser('get_log')
    get_log_parser.set_defaults(func=get_log)

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

def get_log():
    base.get_log()

    