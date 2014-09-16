def check_sanity(PathToReferenceFile, particle):
    try:
        workfile = open("workfile.tmp",'r')
    except IOError:
        print 'cannot open', "workfile.tmp"
        return 404
    
    try:
        referencefile = open(PathToReferenceFile,'r')
    except IOError:
        print 'cannot open', PathToReferenceFile
        return 404
    
    try:
        generatorsFile = open("generators",'r')
    except IOError:
        print 'cannot open', "generators"
        return 404
    
    generatorsList=[]
    for i, line in enumerate(generatorsFile):
        if (line != '\n'):
            generatorsList.append(line.rstrip('\n'))
    generatorsFile.close()
    generatorsSet=set(generatorsList)
    
    print generatorsList
    print generatorsSet
    
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
                lastElement = parts.pop(-1)
                lastElement = lastElement.rstrip(';')
                generatorFound = lastElement in generatorsSet
            secondLastElement = parts.pop(-1)
            while (secondLastElement in generatorsSet):
                secondLastElement = parts.pop(-1)
            parts.append(secondLastElement)
                
            print parts
    workfile.close()
    referencefile.close()       


