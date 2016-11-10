
import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("echo")
    args = parser.parse_args()
    print(args.echo)

if __name__ == '__main__':
        main()