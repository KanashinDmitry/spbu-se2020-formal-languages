from src.antlr_parse import TreeAST
from antlr4 import FileStream
import argparse

def main():
    parser = argparse.ArgumentParser(description='The script visualize input Database script in DOT format')
    parser.add_argument(
        '-s', dest="script_file", required=True, type=str,
        help='path to script file'
    )
    parser.add_argument(
        '-o', dest="output_file", required=True, type=str,
        help='path to output DOT file'
    )
    args = parser.parse_args()

    tree_wrapper = TreeAST(FileStream(args.script_file))
    tree_wrapper.visualize_tree(args.output_file)


if __name__ == "__main__":
    main()