import argparse

def main():
    argparser=parse_args()
    argparser.func(parse_args)

def parse_args():
    parser=argparse.ArgumentParser()
    required_commands=parser.add_subparsers(dest='required_commands')
    required_commands.required=True
    make_parser=required_commands.add_parser('make')
    make_parser.set_defaults(func='make')
    return parser.parse_args()

def make(args):
    print("Hello, there!")
