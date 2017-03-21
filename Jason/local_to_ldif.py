#!/usr/bin/python

import socket
import os
import re

fqdn = re.split('\W+', socket.gethostname())

domain = fqdn[1]
host = fqdn[0]
dc1 = fqdn[-1]

shadow = {}
passwd = {}
group = {}

if os.getuid() != 0:
	quit()

if fqdn[-1] == 0 or fqdn[1] == 'localdomain':
	userinput = raw_input("FQDN could not be determined automatically. Please enter FQDN: ")
	userinput.rstrip()
	if userinput == "":
		print "Null string not accepted. Please try again. \n"
	else:
		fqdn = re.split('\W+', userinput)

for i in fqdn[1:-1]:
	dc2 = ["dc=" + i + ","]

print "Using " + host + " as Hostname. Output will be in " + host +  ".ldif \n"
print "Using " + "".join(str(x) for x in dc2) + "dc="+ dc1 + " as LDAP suffix. \n"

try:
	open("/etc/shadow", "r")
except IOError:
	print("Opening shadow failed")	
	quit()

with open("/etc/shadow", "r") as sf:
	for line in sf:
		line.rstrip() 
		s = []
		s.extend(re.split(':', line))
		if s[1] != '!!' and s[1] != '*':
			shadow[s[0]] = s
			print shadow
try:
        open("/etc/passwd", "r")
except IOError:
        print("Opening passwd failed")        
	quit()


try:
        open("/etc/group", "r")
except IOError:
        print("Opening group failed")        
	quit()

try:
        open(host +'.ldif', "w")
except IOError:
        print("Opening ldif failed")
	quit()

