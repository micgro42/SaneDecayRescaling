import os
from extract_decays import extract_decays
def check_sanity(PathToDecayFile, PathToReferenceFile, particle):
    if (extract_decays(PathToDecayFile,particle) != 0):
        print "ERROR finding decay in Source File. Exiting"
        raise SystemExit,os.EX_DATAERR
    try:
        workfile = open("workfile.tmp",'r')
    except IOError:
        print 'cannot open', "workfile.tmp"
        raise SystemExit,os.EX_SOFTWARE
    
    try:
        referencefile = open(PathToReferenceFile,'r')
    except IOError:
        print 'cannot open', PathToReferenceFile
        raise SystemExit,os.EX_IOERR
    
    try:
        generatorsFile = open("generators",'r')
    except IOError:
        print 'cannot open', "generators"
        raise SystemExit,os.EX_IOERR
    
    generatorsList=[]
    for i, line in enumerate(generatorsFile):
        if (line != '\n'):
            generatorsList.append(line.rstrip('\n'))
    generatorsFile.close()
    generatorsSet=set(generatorsList)
    
    
    for i, line in enumerate(workfile):
        if (line == '\n'):
            continue
        parts = line.split()
        try:
            BR=parts.pop(0)
            BR=float(BR)
        except ValueError:
            pass
        else:
            generatorFound = False
            while (not generatorFound):
                try:
                    lastElement = parts.pop(-1)
                except: # FIXME: catch only the correct exception
                    print "ERROR Generator not found in generators file"
                    print line
                    raise SystemExit,os.EX_SOFTWARE
                lastElement = lastElement.rstrip(';')
                generatorFound = lastElement in generatorsSet
            secondLastElement = parts.pop(-1)
            while (secondLastElement in generatorsSet):
                secondLastElement = parts.pop(-1)
            parts.append(secondLastElement)
                

            ReferenceBR,ReferenceBRE=findDecayInReference(referencefile,parts)
            if (ReferenceBR == -1):
                print "Warning: Decay ", particle, "to", parts, "not found"
            elif (ReferenceBR != BR):
                print "Warning: Decay ", particle, "to", parts, " has a different branching ratios in source and reference file"
                print "source file branching ratio: %f" % (BR)
                print "reference file branching ratio: %f +- %f" % (ReferenceBR, ReferenceBRE)
                print "deviation %f sigma" % (abs((ReferenceBR-BR)/ReferenceBRE))
                
    workfile.close()
    referencefile.close()
    return 0


def findDecayInReference(referencefile, decayList):
    decayList.sort()
    referencefile.seek(0)
    decayFound = False
    for i, line in enumerate(referencefile):
        if (line == '\n'):
            continue
        parts = line.split()
        try:
            BR=parts.pop(0)
            BR=float(BR)
            BRE=parts.pop(0)
            BRE=float(BRE)
        except ValueError:
            pass
        else:
            parts.sort()
#             print parts
            if (decayList == parts):
                decayFound = True
                break
    if (decayFound):
        return BR, BRE
    else:
        return -1,-1
    
    
    






