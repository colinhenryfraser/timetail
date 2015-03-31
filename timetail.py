#!/usr/bin/python

import sys
import argparse
import pprint
import select

#
# process text
#
def process_line(line, time_period, input_format, epoch, oldest):
	print line


#
# Set the arguments 
#
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', default=60, help='Time period in seconds for which to display data from log')
parser.add_argument('-i', '--input', metavar='DATE FORMAT', default='%m %D %h:%m:%s', help='Time and date format of the input file')
parser.add_argument('-e', '--epoch', help='Display date in UNIX epoch time format', action='store_true')
parser.add_argument('-o', '--oldest', help='Display oldest records first', action='store_true')
parser.add_argument('infile', metavar='FILE', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Read data from FILE. With no FILE, read standard input.')
args = parser.parse_args()


#
# Get the Input
#
if args.infile:
	if args.infile.name == '<stdin>':
	#
	# input from stdin
	#
		while sys.stdin in select.select([args.infile], [], [], 0)[0]:
			line = args.infile.readline()
			if line:
				process_line(line.rstrip('\n'), args.time, args.input, args.epoch, args.oldest)
			else:
				exit()
	else:
	#
	# Input from a file
	#
		for line in iter(args.infile):
			process_line(line.rstrip('\n'), args.time, args.input, args.epoch, args.oldest)
