#!/usr/bin/env python2.7


# Included modules
import os
import sys

# ZeroNet Modules
import imp

zeronet = imp.load_source('zeronet', os.environ['SNAP']+'/zeronet.py')

def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    sys.argv = [sys.argv[0]]+["--data_dir", os.environ['SNAP_USER_COMMON']+"/data", "--log_dir", os.environ['SNAP_USER_DATA']+"/log"]+sys.argv[1:]
    mkdirp(os.environ['SNAP_USER_COMMON']+"/data")
    mkdirp(os.environ['SNAP_USER_DATA']+"/log")
    os.chdir(os.environ['SNAP'])
    zeronet.main()

if __name__ == '__main__':
    main()
