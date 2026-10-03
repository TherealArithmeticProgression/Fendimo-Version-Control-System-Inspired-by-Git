import argparse
import os
from fendimo import data
def main():
    arg_parser=parse_args()
    argparser.func(parse_args)

def parse_args():
    parser=argparse.ArgumentParser()
    required_commands=parser.add_subparsers('required_commands')
    required_commands.required=True
    make_parser=required_commands.add_parser(dest='make')
    make_parser.set_default(func='make')

    codesave_parser=required_commands.add_parser(dest='codesave')
    codesave_parser.set_default(func='codesave')
    return parser.parse_args()

def make(args):
    data.init()
    print(f"Initialized a fendimo directory at {os.getcwd()}/{data.DIRECTORY}")

def codesave(args):
    with open(args.file, 'rb') as f:
        data.codesave(f.read())
        