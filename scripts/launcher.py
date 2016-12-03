#!/usr/bin/env python2.7


# Included modules
import os
import sys

# ZeroNet Modules
import zeronet

def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def setarg(arg,val):
    if arg not in sys.argv:
        sys.argv = [sys.argv[0]]+[arg,val]+sys.argv[1:]

def main():
    print("- Please report snap specific errors (e.g. Read-only file system) to: https://github.com/mkg20001/zeronet-snap/issues")
    print("- and ZeroNet specific errors to: https://github.com/HelloZeroNet/ZeroNet/issues")
    setarg("--data_dir",os.environ['SNAP_USER_COMMON']+"/data")
    setarg("--config_file", os.environ['SNAP_USER_COMMON']+"/zeronet.conf")
    setarg("--log_dir", os.environ['SNAP_USER_DATA']+"/log")
    mkdirp(os.environ['SNAP_USER_COMMON']+"/data")
    mkdirp(os.environ['SNAP_USER_DATA']+"/log")
    os.chdir(os.environ['SNAP'])
    sys.exit(zeronet.main())

if __name__ == '__main__':
    main()
