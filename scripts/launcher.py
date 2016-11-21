#!/usr/bin/env python2.7


# Included modules
import os
import sys

# ZeroNet Modules
import imp

zeronet = imp.load_source('zeronet', os.environ['SNAP']+'/zeronet.py') #todo: fix snapcraft.yml and change back to "import zeronet"

def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    print("- Please report snap specific errors (e.g. Read-only file system) to: https://github.com/mkg20001/zeronet-snap/issues")
    sys.argv = [sys.argv[0]]+["--data_dir", os.environ['SNAP_USER_COMMON']+"/data", "--config_file", os.environ['SNAP_USER_COMMON']+"/zeronet.conf", "--log_dir", os.environ['SNAP_USER_DATA']+"/log"]+sys.argv[1:]
    mkdirp(os.environ['SNAP_USER_COMMON']+"/data")
    mkdirp(os.environ['SNAP_USER_DATA']+"/log")
    os.chdir(os.environ['SNAP'])
    zeronet.main()

if __name__ == '__main__':
    main()
