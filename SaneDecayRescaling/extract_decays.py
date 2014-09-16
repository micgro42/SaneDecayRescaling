def extract_decays(PathToDecayFile, particle):
    try:
        EvtGenDecayDec = open(PathToDecayFile,'r')
    except IOError:
        print 'cannot open', PathToDecayFile
        return 404
    
    stringfound = -1
    linenumberBeginDecay = 0
    while (stringfound == -1):
        linenumberBeginDecay += 1
        line = EvtGenDecayDec.readline()
        stringfound=line.find("Decay " + particle +"\n")
        if (line == ""):
            print "String 'Decay %s' not found!" % (particle)
            return 1 
    
    stringfound = -1
    workfile = open('workfile.tmp','w')
    workfile.write(line)
    linenumberEndDecay = linenumberBeginDecay
    while (stringfound == -1):
        linenumberEndDecay += 1
        line = EvtGenDecayDec.readline()
        stringfound=line.find("Enddecay\n")
        workfile.write(line)
        if (line == ""):
            print "String 'Enddecay' not found!"
            return 2
      
    workfile.close()
    EvtGenDecayDec.close()
    return 0

