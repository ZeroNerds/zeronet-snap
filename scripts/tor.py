#!/usr/bin/env python2.7


# Included modules
import os
import sys
import signal
from shutil import copyfile
from subprocess import Popen, PIPE

#argv
argv=[os.environ['SNAP']+"/bin/tor"]+sys.argv[1:]

def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def setarg(arg,val):
    global argv
    if arg not in argv:
        if len(val):
            argv = [argv[0]]+[arg,val]+argv[1:]
        else:
            argv = [argv[0]]+[arg]+argv[1:]

process=0

def signal_handler(signal, frame):
    global process
    print('- Exiting Tor...')
    if process:
        if process.poll():
            process.terminate()
            process.wait()
    sys.exit(0)

def main():
    print("- Please report snap specific errors (e.g. Read-only file system) to: https://github.com/mkg20001/zeronet-snap/issues")
    print("- and Tor specific errors to: https://trac.torproject.org/projects/tor")
    os.chdir(os.environ['SNAP'])
    setarg("--defaults-torrc",os.environ["SNAP"]+"/torrc")
    torrc=os.environ["SNAP_USER_COMMON"]+"/torrc"
    setarg("-f",torrc)
    if not os.path.exists(torrc):
        print("- Creating "+torrc+"...")
        copyfile(os.environ['SNAP']+"/torrc",torrc)
    #setarg("--verify-config","")
    if "--debug" in sys.argv:
        print '[%s]' % ', '.join(map(str, sys.argv))
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    global process
    process = Popen(argv)
    process.communicate()

if __name__ == '__main__':
    main()
