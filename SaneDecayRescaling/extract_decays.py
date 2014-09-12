# -*- coding: utf-8 -*-
from sys import argv

script, DecayFileName, particle = argv

EvtGenDecayDec = open(DecayFileName,'r')

stringfound = -1
linenumberBeginDecay = 0
while (stringfound == -1):
    linenumberBeginDecay += 1
    line = EvtGenDecayDec.readline()
    stringfound=line.find("Decay " + particle)

print "String 'Decay %s' found at line %i:" % (particle, linenumberBeginDecay)
print line

stringfound = -1
workfile = open('workfile.dec','w+')
workfile.write(line)
linenumberEndDecay = linenumberBeginDecay
while (stringfound == -1):
    linenumberEndDecay += 1
    line = EvtGenDecayDec.readline()
    stringfound=line.find("Enddecay")
    workfile.write(line)

print "String 'Enddecay' found at line %i:" % (linenumberEndDecay)



workfile.close()
EvtGenDecayDec.close()