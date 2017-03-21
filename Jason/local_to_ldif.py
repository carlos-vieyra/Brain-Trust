#!/usr/bin/python
import socket
import os
import re

if os.getuid() != 0:
	quit()

fqdn = re.split('\W+', socket.gethostname())

if fqdn[-1] == 0 or fqdn[1] == 'localdomain':
	userinput = raw_input("FQDN could not be determined automatically. Please enter FQDN: ")
	userinput.rstrip()
	if userinput == "":
		print "Null string not accepted. Please try again. \n"
	else:
		fqdn = re.split('\W+', userinput)

domain = fqdn[1]
host = fqdn[0]
dc2 = fqdn[-1]

for i in fqdn[1:-1]:
	dc = ["dc=" + i + ","]

print "Using " + host + " as Hostname. Output will be in " + host +  ".ldif \n"
print "Using " + "".join(str(x) for x in dc) + "dc="+ dc2 + " as LDAP suffix. \n"

