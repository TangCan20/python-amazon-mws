#!/bin/bash

cur_dir=$(cd `dirname $0`; pwd)
echo $cur_dir
export PYTHONPATH=$cur_dir/../
export ETCD_SERVICE_SERVICE_HOST=192.168.0.203
export ETCD_SERVICE_SERVICE_PORT=22379
cd $cur_dir/../
python3 commander.py

