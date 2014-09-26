import os
import utility
def extract_decays_from_decay(path_to_decay_file, particle):
    """get the decays from an EvtGen Decay.Dec file and write them to disk

    return is 0 on success, Exception otherwise
    """

    try:
        evtgen_decay_dec = open(path_to_decay_file, 'r')
    except IOError:
        print 'cannot open', path_to_decay_file
        raise SystemExit(os.EX_IOERR)

    stringfound = -1
    linenumber_begin_decay = 0
    while (stringfound == -1):
        linenumber_begin_decay += 1
        line = evtgen_decay_dec.readline()
        stringfound=line.find("Decay " + particle +"\n")
        if (line == ""):
            print "String 'Decay %s' not found!" % (particle)
            raise SystemExit(os.EX_DATAERR)

    stringfound = -1
    workfile = open('workfile.tmp','w')
    workfile.write(line)
    linenumber_end_decay = linenumber_begin_decay
    while (stringfound == -1):
        linenumber_end_decay += 1
        line = evtgen_decay_dec.readline()
        stringfound=line.find("Enddecay\n")
        workfile.write(line)
        if (line == ""):
            print "String 'Enddecay' not found!"
            raise SystemExit(os.EX_DATAERR)

    workfile.close()
    evtgen_decay_dec.close()
    return 0

def extract_decays_from_reference(path_to_reference_file, particle):
    reference_file = open_file_safely(path_to_reference_file, 'r')
    stringfound = -1
    linenumber_begin_decay = 0
    while (stringfound == -1):
        linenumber_begin_decay += 1
        line = reference_file.readline()
        stringfound=line.find(particle + " DECAY MODES")
        if (line == ""):
            print "String '%s DECAY MODES' not found!" % (particle)
            raise SystemExit(os.EX_DATAERR)
    print "string '%s DECAY MODES' found at line %i" % (particle, linenumber_begin_decay)

    stringfound = -1
    linenumber_end_decay = linenumber_begin_decay
    end_decay_string = "==========================================="
    while (stringfound == -1):
        linenumber_end_decay += 1
        line = reference_file.readline()
        stringfound=line.find(end_decay_string)
        if (line == ""):
            print "String '%s' not found!" % (end_decay_string)
            raise SystemExit(os.EX_DATAERR)

    print "string '%s' found at line %i" % (end_decay_string, linenumber_end_decay)

    reference_file.seek(0)
    work_reference_file = open('workreffile.tmp','w')
    # somehow the linenumbers are one line off ?
    for i, line in enumerate(reference_file):
        if ((i > linenumber_begin_decay + 1) and (i < linenumber_end_decay - 2)):
            lineparts = line.split()
            print lineparts
            scale = -2
            decay_products = [lineparts[0], lineparts[1]]
            print "decay products:", decay_products
            if (lineparts[2]=='('):
                lineparts.pop(2)
            branching_ratio = lineparts[2]
            branching_ratio = branching_ratio.rstrip('%')
            branching_ratio = branching_ratio.rstrip(')')
            branching_ratio = branching_ratio.lstrip('(')
            branching_ratio = branching_ratio.split('+')
            branching_ratio_error = branching_ratio.pop(-1)
            branching_ratio = branching_ratio[0]
            branching_ratio_error = branching_ratio_error.lstrip('-')
            try:
                branching_ratio = float(branching_ratio)
                branching_ratio_error = float(branching_ratio_error)
            except ValueError:
                print "recognising branching fraction at line %i failed" % (i)
                print line
                raise SystemExit(os.EX_SOFTWARE)
            branching_ratio = branching_ratio * (10 ** scale)
            branching_ratio_error = branching_ratio_error * (10 ** scale)

            work_reference_file.writelines([str(branching_ratio), " ",
                                            str(branching_ratio_error), " ",
                                            decay_products[0], " ",
                                            decay_products[1], "\n"])
#             print "i", i
#             print linenumber_begin_decay + 1
#             print linenumber_end_decay - 2
#             print line
        if (i > linenumber_end_decay):
            break
    work_reference_file.close()
    reference_file.close()


def extract_decay_from_lines(lines):
    lines = lines.split("\n")

# get scale of numbers
    if (lines[0].find('%') != -1):
        scale = 0.01
    exponent = lines[0].find('E-')
    if ( exponent != -1):
        print lines[0][exponent+2]
        scale = 1 / (10 ** float(lines[0][exponent+2]))

# get daughters
    parts = lines[0].split()
    daughters = []
    i = 0
    while (parts[i][0] != '('):
        daughters.append(parts[i])
        i += 1

# get branching fraction an errors
    try:
        parts[i][1]
    except IndexError:
        parts.pop(i)
    else:
        parts[i] = parts[i].lstrip('(')
    try:
        branching_fraction = float(parts[i])*scale
    except ValueError:
        branching_fraction = float(parts[i].split('+')[0])*scale
    else:
        parts.pop(i)
    parts[i] = parts[i].rstrip('%')
    parts[i] = parts[i].rstrip(')')
    branching_fraction_error = float(parts[i].split('-')[1])*scale
    return daughters, branching_fraction, branching_fraction_error































