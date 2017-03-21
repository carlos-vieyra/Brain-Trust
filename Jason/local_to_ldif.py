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
			#passwd[p[0],1] = shadow[p[0],1]

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
        open(host + ".ldif", "w")
except IOError:
        print("Opening ldif failed")
	quit()

with open(host + ".ldif", "w") as ld:
	ld.write("dn: " + "".join(str(x) for x in dc2) + "dc=" + dc1 + "\n")
	ld.write("objectClass: dcObject \n")
	ld.write("objectClass: organization \n")
	ld.write("dc: " + domain + "\n")
	ld.write("o: "+ domain + "\n")
	ld.write("\n\n")

	ld.write("dn: ou=Users, " + "".join(str(x) for x in dc2) + "dc=" + dc1 + "\n")
	ld.write("ou: Users \n")
	ld.write("objectClass: top \n")
	ld.write("objectClass: organzationalUnit \n")
	ld.write("\n\n")

	ld.write("dn: ou=Groups," + "".join(str(x) for x in dc2) + "dc=" + dc1 + "\n")
	ld.write("ou: Groups \n")
	ld.write("objectClass: top \n")
	ld.write("objectClass: organizationalUnit \n")
	ld.write("\n\n")

'''for key in passwd:
	if len(passwd[[key],4]) == 0:
		passwd[key[4]] = key
	name = re.split(' ', passwd.get([key],[4]))
	ld.write("dn: cn=" + #key + ", ou=Users," + "".join(str(x) for x in dc2) + "dc=" + dc1 + "\n" )
	ld.write("cn:" ) #+ passwd[key[4]] + "\n")
	ld.write("givenName: ") # + #name[0] + "\n")
	ld.write("sn: " ) #name[0] + "\n")
	ld.write("uid: ") # key + "\n")
	ld.write("uidNumber: ") # + passwd "\n")
	ld.write("homeDirectory" ) # + passwd + "\n")
	ld.write("loginShell: " ) # passwd + "\n")
	ld.write("ObjectClass: top \n")
	ld.write("ObjectClass: shadowAccount \n")
	ld.write("ObjectClass: posixAccount \n")
	ld.write("userPassword: ") # passwd + "\n" )
	ld.write("shadowLastChange: ") # shadow + "\n")
	ld.write("shadowMin") # + shadow + "\n")
	ld.write("shadowMax") # + shadow + "\n")
	ld.write("shadowWarning:") # + shadow + )
	ld.write("\n\n")

#for key in group:
	ld.write("dn: ") #key + "\n")
	ld.write("cn: ") #key + "\n")
	ld.write("objectClass: top \n")
	ld.write("objectClass: groupOfNames \n")
	#members = re.split(',',group key)
	#for member in members:
	#	ld.write("member: cn= ")# member dc)
	ld.write("\n\n")
'''
