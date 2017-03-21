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
		s = []
		line.rstrip()
		if line == re.split('/^\s*#/', line):
			pass 
		s.extend(re.split(':', line))
		if s[1] != '!!' and s[1] != '*':
			shadow[s[0]] = s

try:
        open("/etc/passwd", "r")
except IOError:
        print("Opening passwd failed")        
	quit()

with open("/etc/passwd", "r") as pw:
        for line in pw:
                p = []
		line.rstrip()
   		if line == re.split('/^\s*#/', line):
                        pass
                p.extend(re.split(':', line))
                if p[0] not in shadow and p[2] >= 100:
                        passwd[p[0]] = p
			#passwd[p[0]][1] = shadow[p[0]][1]

try:
        open("/etc/group", "r")
except IOError:
        print("Opening group failed")        
	quit()

with open("/etc/group", "r") as gp:
        for line in gp:
                g = []
                line.rstrip()
                if line == re.split('/^\s*#/', line):
                        pass
                g.extend(re.split(':', line))
                if [3] in g and g[2] >= 100:
                        group[g[0]] = g
 

try:
        open(host +'.ldif', "w")
except IOError:
        print("Opening ldif failed")
	quit()

 
