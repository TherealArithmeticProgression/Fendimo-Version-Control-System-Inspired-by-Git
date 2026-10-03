import argparse
import os
import sys
from fendimo import data


def main():
    arg_parser=parse_args()
    arg_parser.func(arg_parser)

def parse_args():
    parser=argparse.ArgumentParser()
    required_commands=parser.add_subparsers(dest='required_commands')
    required_commands.required=True
    make_parser=required_commands.add_parser('make')
    make_parser.set_defaults(func=make)

    codesave_parser=required_commands.add_parser('codesave')
    codesave_parser.set_defaults(func=codesave)
    codesave_parser.add_argument('file')

    show_parser=required_commands.add_parser('show')
    show_parser.set_defaults(func=show)
    show_parser.add_argument('show')
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



    