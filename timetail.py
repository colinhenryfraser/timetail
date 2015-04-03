#!/usr/bin/python
###################
#
# Name: 	timetail
# Description: 	Output the contents of a log file based
#		on the timesptamps of the log entries.
# Author:	Colin Fraser <colinhenryfraser@me.com>
# Date:		1st April 2015
##

import sys
import argparse
import select
import datetime
import re

#####
# METHODS

#
# Helper function to test string for int
def is_int(string):
	try: 
        	int(sting)
        	return True
    	except:
        	return False

#
# Convert strings like '1w' (1 week), '1d' (1 day), etc to seconds as an int
def get_seconds(time_string):
	#
	# get the last char of the string to test
	switch = time_string[-1:]

	if switch == 'w':
		# weeks
		return int(time_string[:-1])*604800
	elif switch == 'd':
		# days
		return int(time_string[:-1])*86400
	elif switch == 'h':
		# hours
		return int(time_string[:-1])*3600
	elif switch == 'm':
		# minutes
		return int(time_string[:-1])*60
	else:
		return int(time_string)
			
#
# Covert a date format string like '%Y %B %d %h:%m:s' into a regex
def date2regex(date_format):
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
                        elif date_format[i] == 'x':
                                regex = regex + '\d[0-1][0-9]/\d[0-3][0-9]/\d[0-9][0-9]'
                        elif date_format[i] == 'X':
                                regex += '\d{2}:\d{2}:\d{2}'
			elif date_format[i] == '%':
				regex += '%'
			i+=1
		elif re.match("\\\\|\{|\}|\(|\)|\||\[|\]|\^|\*|\$|\.|\?|\+|", date_format[i]):
			regex += "\\" + date_format[i]
			i+=1
		else:	
			regex += str(date_format[i])
			i+=1
	return regex

#
# Receive a log entry and check if is within the range required
def process_line(line, time_period, input_format, epoch):
	#
	# epoch date now
	now_epoch_date = datetime.datetime.now().strftime('%s')

	#
	# Get the regular expression from the date format entered
	date_regex = date2regex(input_format)

	#
	# Test the string is within the time period
	try:
		#
		# Find the date in the line
		match = re.search(date_regex, line.replace("  ", " 0"))
		#
		# Add the year if it doesn't exist - strptime will set it to 1900 if it isn't in the string
		found_date = match.group() + datetime.datetime.strftime(datetime.datetime.now(), '%Y')
		line_epoch_date = datetime.datetime.strptime(found_date, input_format+"%Y").strftime('%s')
		if int(line_epoch_date) >= int(now_epoch_date)-int(time_period):
			#
			# It's good so return the string
			return re.sub(date_regex, line_epoch_date, line.replace("  ", " 0"))
	except:
		#
		# It's not within the time period
		return None

######
# Main
#

#
# Set the arguments 
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', default="3600", help='Time period to display data from log. Append ')
parser.add_argument('-d', '--date', metavar='DATE FORMAT', default="%b %d %X", help="Time and date format of the input file")
parser.add_argument('-e', '--epoch', help='Display date in UNIX epoch time format', action='store_true')
parser.add_argument('-o', '--oldest', help='Display oldest records last (reverse output).', action='store_true')
parser.add_argument('infile', metavar='FILE', nargs='?', type=argparse.FileType('r'), default=sys.stdin, help='Read data from FILE. With no FILE, read standard input.')
args = parser.parse_args()

#
# Check the inputs
if re.match("^[0-9]*[w|d|h|m|0-9]$", args.time) == None:
	parser.print_usage()
	exit()

#
# output is empty dict
output = []

if args.infile:
	if args.infile.name == '<stdin>':
	#
	# input from stdin
	#
		while sys.stdin in select.select([args.infile], [], [], 0)[0]:
			line = args.infile.readline()
			if line:
				test_result = process_line(line.rstrip('\n'), get_seconds(args.time), args.date, args.epoch)
				if test_result != None:
					output.append(test_result)
			else:
				break
	else:
	#
	# Input from a file
	#
		for line in iter(args.infile):
			test_result = process_line(line.rstrip('\n'), get_seconds(args.time), args.date, args.epoch)
			if test_result != None:
				output.append(test_result)

#
# Sort the list
if args.oldest:
	output = sorted(output, reverse=True)
else:
	output = sorted(output)

#
# Print line with date on epoch
for line in output:
	if args.epoch:
		print line
	else:
		#
		# get the epoch date
		match = re.search('\d{10}', line)
		str_date = datetime.datetime.strftime(datetime.datetime.fromtimestamp(float(match.group())), args.date)
		print re.sub('\d{10}', str_date.replace(" 0", "  "), line)
