#!/bin/bash

cd $SNAP
datadir=$SNAP_USER_DATA

#we currently can not open a browser or browser session
SCRIPT="$SNAP/zeronet/zeronet.py"
mkdir -p $datadir/data
mkdir -p $datadir/log
cd $SNAP/zeronet
$SNAP/zero/Python/python $SCRIPT --data_dir $datadir/data --log_dir $datadir/data "$@"
