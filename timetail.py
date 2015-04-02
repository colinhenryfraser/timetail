#!/usr/bin/python

import sys
import argparse
import pprint
import select
import datetime
import re
import collections

def datefregex(date_format):
	regex=''
	i=0
	for j in range(0, len(date_format)):
		if i >= len(date_format):
			return regex
		if date_format[i] == '%':
			i+=1
			if date_format[i] == 'a':
				regex += '(?:Sun|Mon|Tue|Wed|Thu|Fri|Sat)'
			elif date_format[i] == 'A':
				regex = regex + '(?:Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday)'
			elif date_format[i] == 'w':
				regex = regex + '\d[0-6]'
			elif date_format[i] == 'D':
				regex += ' \d{1}|\d{2}'
                        elif date_format[i] == 'd':
				regex += '\d{2}'
                        elif date_format[i] == 'b':
				regex += '(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
                        elif date_format[i] == 'B':
				regex = regex + '(?:January|Febuary|March|April|May|June|July|August|September|October|November|December)'
                        elif date_format[i] == 'm':
				regex = regex + '\d[0-3][0-9]'
                        elif date_format[i] == 'y':
				regex = regex + '\d{2}'
                        elif date_format[i] == 'Y':
				regex = regex + '\d{4}'
                        elif date_format[i] == 'H':
				regex = regex + '\d[0-2][0-9]'
                        elif date_format[i] == 'I':
				regex = regex + '\d[0-1][0-9]'
                        elif date_format[i] == 'p':
				regex = regex + '(?:PM|AM)'
                        elif date_format[i] == 'M':
				regex = regex + '\d[0-6][0-9]'
                        elif date_format[i] == 'S':
				regex = regex + '\d[0-6][0-9]'
                        elif date_format[i] == 'f':
				regex = regex + '\d{6}'
                        elif date_format[i] == 'z':
				regex = regex + '(?:\+HHMM|-HHMM)'
                        elif date_format[i] == 'Z':
				regex = regex + ''
                        elif date_format[i] == 'j':
				regex = regex + '\d[0-3][0-5][0-9]'
                        elif date_format[i] == 'U':
				regex = regex + '\d[0-5][0-9]'
                        elif date_format[i] == 'W':
				regex = regex + '\d[0-5][0-9]'
			elif date_format[i] == 'c':
                                regex = regex + ''
                        elif date_format[i] == 'x':
                                regex = regex + '\d[0-1][0-9]/\d[0-3][0-9]/\d[0-9][0-9]'
                        elif date_format[i] == 'X':
                                regex += '\d{2}:\d{2}:\d{2}'
			i+=1
			
		else:	
			regex += str(date_format[i])
			i+=1
	return regex
	
# process text
#
def process_line(line, time_period, input_format, epoch):
	#
	# epoch date now
	now_epoch_date = datetime.datetime.now().strftime('%s')

	#
	# Get the regular expression from the date format entered
	date_regex = datefregex(input_format)

	#
	# set the date format
	#
	try:
		#
		# Find the date in the line
		match = re.search(date_regex, line)
		#
		# Add the year if it doesn't exist
		found_date = match.group() + datetime.datetime.strftime(datetime.datetime.now(), '%Y')
		line_epoch_date = datetime.datetime.strptime(found_date, input_format+"%Y").strftime('%s')
		if int(line_epoch_date) >= int(now_epoch_date)-int(time_period):
			if epoch == True:
				return {line_epoch_date: re.sub(date_regex, line_epoch_date, line)}
			else:
				return {line_epoch_date: line}
	except:
		return 1

#
# Set the arguments 
#
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', default=60, help='Time period in seconds for which to display data from log')
parser.add_argument('-i', '--input', metavar='DATE FORMAT', default='%b %d %X', help='Time and date format of the input file')
parser.add_argument('-e', '--epoch', help='Display date in UNIX epoch time format', action='store_true')
parser.add_argument('-o', '--oldest', help='Display oldest records first', action='store_true')
parser.add_argument('infile', metavar='FILE', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Read data from FILE. With no FILE, read standard input.')
args = parser.parse_args()

#
# output is empty dict
output = {}

if args.infile:
	if args.infile.name == '<stdin>':
	#
	# input from stdin
	#
		while sys.stdin in select.select([args.infile], [], [], 0)[0]:
			line = args.infile.readline()
			if line:
				test_result = process_line(line.rstrip('\n').replace("  ", " 0"), args.time, args.input, args.epoch)
				if test_result != None:
					output.update(test_result)
			else:
				break
	else:
	#
	# Input from a file
	#
		for line in iter(args.infile):
			test_result = process_line(line.rstrip('\n').replace("  ", " 0"), args.time, args.input, args.epoch)
			if test_result != None:
				output.update(test_result)

#
# Print in order
if args.oldest:
	pprint.pprint(collections.OrderedDict(sorted(output.items(), reverse=True)).items())
else:
	pprint.pprint(collections.OrderedDict(sorted(output.items())).items())
