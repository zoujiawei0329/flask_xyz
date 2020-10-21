#!/usr/bin/env bash
mkdir $PWD/log
fname=$PWD/log/$(date +%Y%m%d)log.txt
echo ${fname}
nohup python start.py>>${fname} &
