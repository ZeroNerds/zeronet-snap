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
    echo "Something (propably Tor) has failed to start..."
    exit 2
  fi
  start_cmd $* & add_pid $!
}
stop_pids() {
  rm $runlock
  for p in $(cat $tmp); do
    kill $p
  done
}

start_pid $SNAP/tor.py
sleep 1s
start_pid $SNAP/zeronet.py $*

sleep infinity

stop_pids #stop all after Ctrl+C
