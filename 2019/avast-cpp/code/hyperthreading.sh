#!/usr/bin/env bash

STATE=$1
echo ${STATE} > /sys/devices/system/cpu/cpu4/online
echo ${STATE} > /sys/devices/system/cpu/cpu5/online
echo ${STATE} > /sys/devices/system/cpu/cpu6/online
echo ${STATE} > /sys/devices/system/cpu/cpu7/online
