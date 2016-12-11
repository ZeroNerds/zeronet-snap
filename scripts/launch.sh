#!/bin/bash
tmp="$SNAP_USER_DATA/.pidfile"
runlock="$SNAP_USER_DATA/.runlock"
rm -f $tmp
touch $tmp
echo "$$" > $runlock
add_pid() {
  echo " $1" >> $tmp
}
start_cmd() {
  $*
  stop_pids
}
start_pid() {
  if ! [ -f $runlock ]; then
    echo "Something (probably Tor) has failed to start..."
    exit 2
  fi
  start_cmd $* & add_pid $!
}
stop_pids() {
  if [ -f $runlock ]; then
    rm $runlock
  fi
  for p in $(cat $tmp); do
    kill $p 2> /dev/null
  done
  rm $tmp
}

start_pid $SNAP/tor.py
sleep 1s
start_pid $SNAP/zeronet.py $*

sleep infinity

stop_pids #stop all after Ctrl+C
