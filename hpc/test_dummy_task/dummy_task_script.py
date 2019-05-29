from __future__ import print_function

import itertools
import argparse
import sys 
import os
from time import sleep
import random
import stat
import copy 
parser = argparse.ArgumentParser()

parser.add_argument('--input1',required=True,type=int)
parser.add_argument('--input2',required=True,type=str)
parser.add_argument('--input3',required=True,type=str)

args = parser.parse_args(sys.argv[1:])

print('Hello!. You ran this job with following params: {} , {} , {}'.format(args.input1, args.input2, args.input3))



