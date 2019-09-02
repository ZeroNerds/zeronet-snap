#!/usr/bin/env python3


import errno
# Included modules
import os
import signal
import sys
import threading
from subprocess import PIPE, Popen
from time import sleep


def mkdirp(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


processes = []
threads = []


def signal_handler(signal, frame):
    print('- Exiting ZeroNet...')
    global processes, threads
    for process in processes:
        try:
            process.terminate()
        except OSError as err:
            if err.errno != errno.ESRCH:
                print("- Error while killing the process: " + err.errno)
        process.wait()
    for thread in threads:
        thread.join()


def setarg(arg, val):
    if arg not in sys.argv:
        if len(val):
            sys.argv = [sys.argv[0]] + [arg, val] + sys.argv[1:]
        else:
            sys.argv = [sys.argv[0]] + [arg] + sys.argv[1:]


class pipeThread (threading.Thread):
    def __init__(self, threadID, name, counter, args):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.args = args

    def run(self):
        # print "Starting "+self.name
        self.args.communicate()
        print(self.name + " has exited")


def start_tor(args):
    argv = [os.environ['SNAP'] + "/command-tor.wrapper"] + args[0:]
    global threads, process
    process = Popen(argv)
    tor_thread = pipeThread(1, "Tor", 1, process)
    tor_thread.start()
    threads.append(tor_thread)
    processes.append(process)


def start_zero(args):
    global threads, processes
    process = Popen(args)
    zero_thread = pipeThread(2, "ZeroNet", 2, process)
    zero_thread.start()
    threads.append(zero_thread)
    processes.append(process)


def zero_plugins():
    #print("- Fixing plugins")
    plugin_realsrc = os.environ['SNAP'] + "/plugins"
    plugin_src = "/snap/zeronet/current/plugins"
    plugin_dest = os.environ['SNAP_USER_COMMON'] + "/plugins"
    print("- Linking plugins...")

    all_plugins = os.listdir(plugin_src)
    notfound = os.listdir(plugin_src)
    mkdirp(plugin_dest)
    current = os.listdir(plugin_dest)
    for pl in current:  # check if that plugin exists, and remove it from notfound
        plp = plugin_dest + "/" + pl
        if os.path.islink(plp):
            pld = os.path.realpath(plp)
            # print "Real of "+plp+" is "+pld
            if pld.startswith(plugin_realsrc + "/"):
                if not os.path.exists(pld):
                    if pl == "BigFile" or pl == "Mute":
                        os.unlink(plp)
                    else:
                        raise Exception("Path " + pld + " does not exist")
                # print '[nf: %s]' % ', '.join(map(str, notfound))
                pln = pld.replace(plugin_realsrc + "/",
                                  "").replace("disabled-", "")
                if pln in notfound:
                    notfound.remove(pln)
                if "disabled-" + pln in notfound:
                    notfound.remove("disabled-" + pln)

    for pl in notfound:  # create that plugin link
        pld = plugin_dest + "/" + pl
        pls = plugin_src + "/" + pl
        if os.path.exists(pld):
            raise Exception(
                "Path " + pld + " could not be linked to " + pls + ": Already exists")
        # print "Linked "+pls+" to "+pld
        os.symlink(pls, pld)


def link(src_):
    src = "/snap/zeronet/current/" + src_
    dst = os.environ['SNAP_USER_COMMON'] + "/" + src_
    if not os.path.exists(dst):
        os.symlink(src, dst)


def zero_link():
    for p in ["update.py", "src", "zeronet.py"]:
        link(p)


def zero_start():
    print("- Please report snap specific errors (e.g. Read-only file system) to: https://github.com/mkg20001/zeronet-snap/issues")
    print("- and ZeroNet specific errors to: https://github.com/HelloZeroNet/ZeroNet/issues")
    if "--debug" in sys.argv:
        print('[%s]' % ', '.join(map(str, sys.argv)))
    setarg("--data_dir", os.environ['SNAP_USER_COMMON'] + "/data")
    setarg("--config_file", os.environ['SNAP_USER_COMMON'] + "/zeronet.conf")
    setarg("--log_dir", os.environ['SNAP_USER_COMMON'] + "/log")
    mkdirp(os.environ['SNAP_USER_COMMON'] + "/data")
    mkdirp(os.environ['SNAP_USER_COMMON'] + "/log")
    zero_plugins()
    zero_link()
    os.chdir(os.environ['SNAP_USER_COMMON'])
    sys.path.remove(os.environ["SNAP"])
    sys.path.append(os.environ['SNAP_USER_COMMON'])
    import zeronet
    sys.exit(zeronet.main())


def main():
    if "--enable-tor" in sys.argv:
        sys.argv.remove("--enable-tor")
        setarg("--tor", "enable")
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        start_tor([])
        start_zero(sys.argv)
        # This makes kill work, but only for 1 year TODO: fix this
        sleep(365 * 24 * 60 * 60 * 1000)
    else:
        zero_start()


if __name__ == '__main__':
    main()
