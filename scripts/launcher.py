#!/usr/bin/env python2.7


# Included modules
import os
import sys
import signal
import errno

from subprocess import PIPE, Popen
from time import sleep
import threading

# ZeroNet Modules
import zeronet

def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

processes=[]
threads=[]

def signal_handler(signal, frame):
    print('- Exiting ZeroNet...')
    global processes, threads
    for process in processes:
        try:
            process.terminate()
        except OSError, err:
            if err.errno != errno.ESRCH:
                print "- Error while killing the process: "+err.errno
        process.wait()
    for thread in threads:
        thread.join()

def setarg(arg,val):
    if arg not in sys.argv:
        if len(val):
            sys.argv = [sys.argv[0]]+[arg,val]+sys.argv[1:]
        else:
            sys.argv = [sys.argv[0]]+[arg]+sys.argv[1:]

class pipeThread (threading.Thread):
    def __init__(self, threadID, name, counter, args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.args = args
    def run(self):
        #print "Starting "+self.name
        self.args.communicate()
        print self.name+" has exited"

def start_tor(args):
    argv=[os.environ['SNAP']+"/command-tor.wrapper"]+args[0:]
    global threads, process
    process = Popen(argv)
    tor_thread=pipeThread(1,"Tor",1,process)
    tor_thread.start()
    threads.append(tor_thread)
    processes.append(process)

def start_zero(args):
    global threads, processes
    process = Popen(args)
    zero_thread=pipeThread(2,"ZeroNet",2,process)
    zero_thread.start()
    threads.append(zero_thread)
    processes.append(process)

def zero_start():
    print("- Please report snap specific errors (e.g. Read-only file system) to: https://github.com/mkg20001/zeronet-snap/issues")
    print("- and ZeroNet specific errors to: https://github.com/HelloZeroNet/ZeroNet/issues")
    if "--debug" in sys.argv:
        print '[%s]' % ', '.join(map(str, sys.argv))
    setarg("--data_dir",os.environ['SNAP_USER_COMMON']+"/data")
    setarg("--config_file", os.environ['SNAP_USER_COMMON']+"/zeronet.conf")
    setarg("--log_dir", os.environ['SNAP_USER_DATA']+"/log")
    mkdirp(os.environ['SNAP_USER_COMMON']+"/data")
    mkdirp(os.environ['SNAP_USER_DATA']+"/log")
    os.chdir(os.environ['SNAP'])
    sys.exit(zeronet.main())

def main():
    if "--enable-tor" in sys.argv:
        sys.argv.remove("--enable-tor")
        setarg("--tor","enable")
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        start_tor([])
        start_zero(sys.argv)
        sleep(365*24*60*60*1000) #This makes kill work, but only for 1 year TODO: fix this
    else:
        zero_start()

if __name__ == '__main__':
    main()
