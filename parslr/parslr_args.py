import argparse
import os
import re


def file_path(string):
    if os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def file_dir_path(string):
    if os.path.isfile(string) or os.path.isdir(string):
        return string
    else:
        raise FileNotFoundError(string)


def dir_doesnt_exist(string):
    if os.path.isdir(string):
        raise FileExistsError(string)
    else:
        return string


def prepare_parser():
    """
    Parse common benchmark arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grammar",
                        help="Grammar file",
                        required=True,
                        type=file_path)
    parser.add_argument("-a", "--antlr",
                        help="ANTLR path",
                        required=True,
                        type=file_path)
    parser.add_argument("-r", "--rule",
                        help="Rule to start parsing with",
                        required=True)
    parser.add_argument("-i", "--input",
                        help="File or directory with files to parse",
                        required=True,
                        type=file_dir_path)
    parser.add_argument("-v", "--verbose",
                        help="Verbose mode",
                        action='store_true')
    parser.add_argument("-t", "--tmp_path",
                        help="Temporary folder",
                        type=dir_doesnt_exist,
                        default="tmp")
    return parser
