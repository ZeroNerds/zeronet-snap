#!/usr/bin/env python2.7


# Included modules
import os
import sys
import signal
from subprocess import PIPE, Popen
from threading  import Thread
from Queue import Queue, Empty
from multiprocessing import Pool

# ZeroNet Modules
import zeronet

def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

process=0

def signal_handler(signal, frame):
    global process
    print('- Exiting ZeroNet...')
    if process:
        if process.poll():
            process.terminate()
            process.wait()
    sys.exit(0)

def setarg(arg,val):
    if arg not in sys.argv:
        if len(val):
            sys.argv = [sys.argv[0]]+[arg,val]+sys.argv[1:]
        else:
            sys.argv = [sys.argv[0]]+[arg]+sys.argv[1:]

def main():
    print("- Please report snap specific errors (e.g. Read-only file system) to: https://github.com/mkg20001/zeronet-snap/issues")
    print("- and ZeroNet specific errors to: https://github.com/HelloZeroNet/ZeroNet/issues")
    print '[%s]' % ', '.join(map(str, sys.argv))
    setarg("--data_dir",os.environ['SNAP_USER_COMMON']+"/data")
    setarg("--config_file", os.environ['SNAP_USER_COMMON']+"/zeronet.conf")
    setarg("--log_dir", os.environ['SNAP_USER_DATA']+"/log")
    mkdirp(os.environ['SNAP_USER_COMMON']+"/data")
    mkdirp(os.environ['SNAP_USER_DATA']+"/log")
    os.chdir(os.environ['SNAP'])
    if "--enable-tor" in sys.argv:
        sys.argv.remove("--enable-tor")
        setarg("--tor","enable")
        argv=[os.environ["SNAP"]+"/launch.sh"]+sys.argv[1:]
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        global process
        process = Popen(argv)
        process.communicate()
    else:
        sys.exit(zeronet.main())

if __name__ == '__main__':
    main()
