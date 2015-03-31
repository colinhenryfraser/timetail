#!/usr/bin/python

import sys
import argparse
import pprint
import select


#
# Set the arguments 
#
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--period', help='Period of time for which to display data from log')
parser.add_argument('-i', '--input', help='Time and date format of the input file')
parser.add_argument('-e', '--epoch', help='Output is displayed in UNIX epoch time format', action='store_true')
parser.add_argument('-o', '--oldest', help='Display records oldest first', action='store_true')
parser.add_argument('infile', metavar='FILE', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
args = parser.parse_args()

#
# Input from file
#
if 

#
# input from stdin
#
while sys.stdin in select.select([args.infile], [], [], 0)[0]:
	line = args.infile.readline()
	if line:
		print line
	else:
		exit()

