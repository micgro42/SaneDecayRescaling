import os
from extract_decays import extract_decays
def check_sanity(path_to_decayfile, path_to_referencefile, particle):
    if (extract_decays(path_to_decayfile, particle) != 0):
        print "ERROR finding decay in Source File. Exiting"
        raise SystemExit(os.EX_DATAERR)
    try:
        workfile = open("workfile.tmp", 'r')
    except IOError:
        print 'cannot open', "workfile.tmp"
        raise SystemExit(os.EX_SOFTWARE)

    try:
        referencefile = open(path_to_referencefile, 'r')
    except IOError:
        print 'cannot open', path_to_referencefile
        raise SystemExit(os.EX_IOERR)

    try:
        generatorsfile = open("generators", 'r')
    except IOError:
        print 'cannot open', "generators"
        raise SystemExit(os.EX_IOERR)

    generators_list = []
    for i, line in enumerate(generatorsfile):
        if (line != '\n'):
            generators_list.append(line.rstrip('\n'))
    generatorsfile.close()
    generators_set = set(generators_list)


    for i, line in enumerate(workfile):
        if (line == '\n'):
            continue
        parts = line.split()
        try:
            BR = parts.pop(0)
            BR = float(BR)
        except ValueError:
            pass
        else:
            generator_found = False
            while (not generator_found):
                try:
                    last_element = parts.pop(-1)
                except: # FIXME: catch only the correct exception
                    print "ERROR Generator not found in generators file"
                    print line
                    raise SystemExit(os.EX_SOFTWARE)
                last_element = last_element.rstrip(';')
                generator_found = last_element in generators_set
            second_last_element = parts.pop(-1)
            while (second_last_element in generators_set):
                second_last_element = parts.pop(-1)
            parts.append(second_last_element)


            ReferenceBR, ReferenceBRE = find_decay_in_reference(referencefile, parts)
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


def find_decay_in_reference(referencefile, decay_list):
    """search for decay in provided reference file

    
    """

    decay_list.sort()
    referencefile.seek(0)
    decay_found = False
    for i, line in enumerate(referencefile):
        if (line == '\n'):
            continue
        parts = line.split()
        try:
            BR = parts.pop(0)
            BR = float(BR)
            BRE = parts.pop(0)
            BRE = float(BRE)
        except ValueError:
            pass
        else:
            parts.sort()
#             print parts
            if (decay_list == parts):
                decay_found = True
                break
    if (decay_found):
        return BR, BRE
    else:
        return -1, -1






