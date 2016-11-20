#!/usr/bin/env python2.7


# Included modules
import os

# ZeroNet Modules
import zeronet

def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def main():
    mkdirp(os.environ['SNAP_USER_DATA']+"/data")
    mkdirp(os.environ['SNAP_USER_DATA']+"/log")
    os.chdir(os.environ['SNAP'])
    zeronet.main()

if __name__ == '__main__':
    main()
