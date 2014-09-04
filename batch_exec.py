#!/usr/bin/python

""" [USAGE]

Make a file with command, following below is format of command_file.

---------- start of File ----------
echo "HELLO"
echo "HELLO" @10
ping google.com -t 256
echo "WORLD" | cat
---------- end of File ----------

@ 	: time delay arg, unit time is sec
| 	: pipe flag, notifying this command is piped

"""

import subprocess
import sys
import time


def parsing(file_name):
	print '[parsing start]'
	f = open(file_name, 'r')
	txt = f.read()
	command_list = txt.split('\n')
	for cmd in command_list:
		if cmd:

			print '[parsing command]', '[', cmd, ']'

			wait_time = cmd.split('@')

			#check cmd with pipe
			pipe_flag = cmd.find('|')
			
			#excute it
			if pipe_flag < 1 : 
				_exc(cmd.split(' '))
			else:
				excs = cmd.split('|')
				_piped_exc(excs[0].split(' '), excs[1].split(' '))

			# waiting
			if len(wait_time) > 1:
				print '[parsing waiting]', '[', wait_time,  ']'
				time.sleep( float(wait_time[1]) )



def _exc( exc_list ):
	print '[EXC]', exc_list
	subprocess.Popen( exc_list )


def _piped_exc(exc_list1, exc_list2):
	print '[EXC]', exc_list1, '|', exc_list2
	p1 = subprocess.Popen(exc_list1, stdout=subprocess.PIPE) #Set up the echo command and direct the output to a pipe
	p2 = subprocess.Popen(exc_list2, stdin=p1.stdout) #send p1's output to p2
	p1.stdout.close() #make sure we close the output so p2 doesn't hang waiting for more input
	output = p2.communicate()[0] #run our commands




if len(sys.argv) == 1:
	print 'usage : python batch_exc.py filename'
if len(sys.argv) > 1:
	parsing(sys.argv[1])
