#Timetail

###Description:

Print the last 60 minutes of FILE to standard output. With no FILE read from standard input. 

	usage: timetail [-h] [-t TIME] [-d DATE FORMAT] [-e] [-o] [FILE]
	
	positional arguments:
	FILE                  Read data from FILE. With no FILE, read standard
        	              input.
	
	
	optional arguments:

	-h, --help            		show this help message and exit
	
	-t TIME, --time TIME  		Time period to display data from log. Append

	-d DATE FORMAT, --date DATE FORMAT
	
                        		Time and date format of the input file

	-e, --epoch           		Display date in UNIX epoch time format

	-o, --oldest          		Display oldest records last (reverse output).

###Install:
	sudo pip install argparse
	sudo wget -P /usr/local/bin/ https://raw.githubusercontent.com/colinhenryfraser/timetail/master/timetail.py
	sudo mv /usr/local/bin/timetail.py /usr/local/bin/timetail
	sudo chmod a+x /usr/local/bin/timetail

###Examples:

Display the last 60 minutes of the /var/log/secure file:

	timetail /var/log/secure

Display the last 60 minutes of the /var/log/secure file in reverse (oldest entries last):

	timetail -o /var/log/secure

Display the last 60 minutes of the /var/log/secure with epoch time stamps:

	timetail -e /var/log/secure

Display the last day of the /var/log/secure:

	timetail -t 1d /var/log/secure

Display the last 30 seconds of the /var/log/secure:

	timetail -t 30 /var/log/secure

Read all the /var/log/secure logs from stdin and display the last week in revers order:

	cat /var/log/secure* | timetail -t 1w -o

Read the last 3 hours of the Apache access log from stdin:

	cat /var/log/httpd/access_log | timetail -d "%d/%b/%Y:%H:%M:%S" -t 3h

