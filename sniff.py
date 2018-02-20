#! /usr/bin/python
# -*- coding: utf-8 -*-
from os import system
from termcolor import colored
from time import sleep
from flask import Flask


close_process='airmon-ng check kill'
system(close_process)
monitor='airmon-ng start wlx14cc202576fb'
system(monitor)
sniff='airodump-ng wlan0mon'
system(sniff)



