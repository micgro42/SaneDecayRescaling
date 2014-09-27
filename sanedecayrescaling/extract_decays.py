import os
import utility
from xml.dom import minicompat
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
    column1, column2, column3, column_mini = make_single_line_snippets(lines)
    lines = lines.split("\n")

# get scale of numbers
#TODO: what should this section do for "senn", "not seen" or "large"?
    if (column2.find('%') != -1):
        scale = 0.01
        column2 = column2.rstrip('%')
    exponent_position = column2.find('E-')
    if ( exponent_position != -1):
        print column2[exponent_position+2]
        scale = 1 / (10 ** float(column2[exponent_position+2]))
        column2 = column2[:exponent_position]

# get daughters
    parts = lines[0].split()
    daughters = []
    i = 0
    while (parts[i][0] != '('):
        daughters.append(parts[i])
        i += 1
    daughters = column1.split()

# get branching fraction and errors
    if (column2[0] == '('): #default
        column2 = column2.lstrip('(')
        column2 = column2.rstrip(')')
        column2 = column2.strip()
        branching_fraction = column2.split('+')[0]
        if (column2.find('+-') != -1):
            branching_fraction_error_plus = column2.split('-')[1]
            branching_fraction_error_minus = branching_fraction_error_plus
        else:
            branching_fraction_error_plus = column2.split('+')[1]
            branching_fraction_error_minus = column2.split('-')[1]
    elif (column2[0] == '<'): #limit
        pass
    elif (column2[0] == 's'): #seen
        pass
    elif (column2[0] == 'n'): #not seen
        pass
    elif (column2[0] == 'l'): #large
        pass
    else:
        raise ParseError(lines,"first char in '" + column2 + "' not implemented")

    try:
        branching_fraction_error_plus = float(branching_fraction_error_plus)
        branching_fraction_error_minus = float(branching_fraction_error_minus)
    except ValueError:
        raise ParseError(lines,"failed to parse braching fraction correctly")
    else:
        branching_fraction_error_plus = branching_fraction_error_plus * scale
        branching_fraction_error_minus = branching_fraction_error_minus * scale


    return daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus


def make_single_line_snippets(input_lines):
    """
    The ascii-refernece file has more or less 3 columns, the first until 40 chars
    the second column goes to 66, after which comes the last colum, which is
    irrelevant.
    The indicator for a multi-line decay is the presence of a '\' char, which
    signals a linebreak for that column.
    This first column contains the decay products and and sometimes some other
    characters, the second column contains the branching fraction
    """

    lines = input_lines.rstrip("\n")
    lines = lines.split("\n")
    first_column = []
    second_column = []
    third_column = []
    mini_column = []
    for line in lines:
        if (line[:40] != ''):
            first_column.append(line[:40])
        if (line[40:66] != ''):
            second_column.append(line[40:66])
        if (line[66:] != ''):
            third_column.append(line[66:])

    while (first_column[0].find('\\ ') != -1):
        if (first_column[0].find('[') != -1):
            mini_column = [first_column[0][first_column[0].find('['):].rstrip('\\ ')]
            first_column[0] = first_column[0][:first_column[0].find('[')]
            if (first_column[1].find(']') == -1):
                mini_column.append(first_column[1][36:].rstrip('\\'))
                first_column[1] = first_column[1][:36].rstrip()
                mini_column.append(first_column[2][36:])
                first_column[2] = first_column[2][:36].rstrip()
            else:
                mini_column.append(first_column[1][36:])
                first_column[1] = first_column[1][:36].rstrip()
            continue
        first_column[0] = first_column[0].rstrip("\\ ")
        first_column[0] = first_column[0] + first_column[1]
        first_column.pop(1) 
    while (second_column[0].find('\\ ') != -1):
        second_column[0] = second_column[0].rstrip("\\ ")
        second_column[0] = second_column[0] + second_column[1]
        second_column.pop(1) 
    while (third_column[0].find('\\ ') != -1):
        third_column[0] = third_column[0].rstrip("\\ ")
        third_column[0] = third_column[0] + third_column[1]
        third_column.pop(1)
    if (len(first_column) > 1):
        if (first_column[1] == ''):
            first_column.pop(1)
        else:
            raise ParseError(input_lines,"string '" + first_column[1] + "should be empty")
    if (len(first_column) == 1):
        first_column = first_column[0]
        first_column = first_column.strip()
    else:
        raise ParseError(input_lines,"the list first_column should only have 1 item, but it currently has " + len(first_column))
    if (len(second_column) == 1):
        second_column = second_column[0]
        second_column = second_column.strip()
    else:
        raise ParseError(input_lines,"the list second_column should only have 1 item, but it currently has " + len(second_column))
    if (len(third_column) == 1):
        third_column = third_column[0]
        third_column = third_column.strip()
    else:
        raise ParseError(input_lines,"the list third_column should only have 1 item, but it currently has " + len(third_column))
    
    while (len(mini_column) > 1):
        mini_column[0] = mini_column[0] + mini_column[1]
        mini_column.pop(1)
    if (len(mini_column) == 1):
        mini_column = mini_column[0]
    else:
        mini_column = ''

    return first_column, second_column, third_column, mini_column

    # @TODO: rebuild and return the columns seperately because only the first 
    # contains daughters and only the second contains the branching fraction  



























