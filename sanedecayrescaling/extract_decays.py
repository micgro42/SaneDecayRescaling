import os
from utility import *
from translate_particles import *
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
    """
    :return: nothing
    :create: file workreffile.tmp
    """
    t = hep_translator()
    particle = t.translate_evtgen_to_pdg(particle)
    reference_file = open_file_safely(path_to_reference_file, 'r')
    string_found = -1
    linenumber_begin_decay = 0
    for line in iter(reference_file.readline, ''):
        linenumber_begin_decay += 1
        string_found=line.find(particle + " DECAY MODES")
        if (string_found != -1):
            file_position_begin_decay = reference_file.tell()
            print "string '%s DECAY MODES' found at line %i" % (particle, linenumber_begin_decay)
            break;
    if (string_found == -1):
        print "String '%s DECAY MODES' not found!" % (particle)
        raise SystemExit(os.EX_DATAERR)



    string_found = -1
    linenumber_end_decay = linenumber_begin_decay
    end_decay_string = "==========================================="
    for line in iter(reference_file.readline, ''):
        linenumber_end_decay += 1
        string_found=line.find(end_decay_string)
        if (string_found != -1):
            print "string '%s' found at line %i" % (end_decay_string, linenumber_end_decay)
            break;
        if (line == ""):
            print "String '%s' not found!" % (end_decay_string)
            raise SystemExit(os.EX_DATAERR)

    
    decay_length = (linenumber_end_decay -2) - (linenumber_begin_decay + 2)
    print "decay_length", decay_length
    reference_file.seek(file_position_begin_decay, 0)
    reference_file.readline()
    reference_file.readline()

    work_reference_file = open('workreffile.tmp','w')
    work_reference_file.write("Decay " + t.translate_pdg_to_evtgen(particle) +"\n")
    position_in_decay = 0
    for line in iter(reference_file.readline, ''):
        position_in_decay += 1
        if (position_in_decay > decay_length ):
            break;
        if (line == '\n'):
            continue
        if (line[0] == ' '):
            continue
        if (line[0] == '['):
            continue # TODO: Confirm that this is actually correct behavior
        decay_lines = line
        if (line.find('\\') != -1):
            for j in range(0, 2):
                position_without_readahead = reference_file.tell()
                next_line = reference_file.readline()
                try:
                    next_line[77]
                except IndexError:
                    if (next_line.strip() == ''):
                        reference_file.seek(position_without_readahead)
                        break;
                    decay_lines = decay_lines + next_line
                    position_in_decay += 1
                    continue
                else:
                    reference_file.seek(position_without_readahead)
                    break;

        try:
            daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decay_from_lines(decay_lines)
        except (IndexError) as e:
            print "IndexError in line", linenumber_begin_decay + position_in_decay + 2
            raise
        except (ParseError) as e:
            print "ParseError in line", linenumber_begin_decay + position_in_decay + 2
            print e.msg
            print e.line
            raise
        except:
            print "Error in line", linenumber_begin_decay + position_in_decay + 2
            raise
        for i, daughter_in_decay in enumerate(daughters):
            daughters[i] = t.translate_pdg_to_evtgen(daughter_in_decay)
        extracted_line = str(branching_fraction) + ' ' + str(branching_fraction_error_plus) + ' ' + str(branching_fraction_error_minus) + ' ' + ' '.join(daughters) + '\n'
        work_reference_file.write(extracted_line)

    work_reference_file.write('Enddecay\n')
    work_reference_file.close()
    reference_file.close()


def extract_decay_from_lines(lines):
    """
    Return 0 errors for limit cases
    """
    column1, column2, column3, column_mini = make_single_line_snippets(lines)
    lines = lines.split("\n")

# get scale of numbers
#TODO: what should this section do for "senn", "not seen" or "large"?
    if (column2.find('%') != -1):
        scale = 0.01
        column2 = column2.rstrip('%')
    exponent_position = column2.find('E-')
    if ( exponent_position != -1):
        scale = 1 / (10 ** float(column2[exponent_position+2]))
        column2 = column2[:exponent_position]

# get daughters
    while (column1[0] == '.'):
        column1 = column1[1:]
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
            branching_fraction_error_plus = column2.split('+')[1].split('-')[0]
            branching_fraction_error_minus = column2.split('-')[1]
    elif (column2[0] == '<'): #limit
        column2 = column2.lstrip('<')
        column2 = column2.strip()
        branching_fraction = column2
        branching_fraction_error_plus = 0
        branching_fraction_error_minus = 0
    elif (column2[0] == 's'): #seen
        pass
    elif (column2[0] == 'n'): #not seen
        branching_fraction = 0
        branching_fraction_error_plus = 0
        branching_fraction_error_minus = 0
        scale = 0
    elif (column2[0] == 'l'): #large
        pass
    else:
        raise ParseError(lines,"first char in '" + column2 + "' not implemented")

    try:
        branching_fraction = float(branching_fraction)
        branching_fraction_error_plus = float(branching_fraction_error_plus)
        branching_fraction_error_minus = float(branching_fraction_error_minus)
    except ValueError:
        print "branching_fraction:", branching_fraction
        print "branching_fraction_error_plus:", branching_fraction_error_plus
        print "branching_fraction_error_minus:", branching_fraction_error_minus
        raise ParseError(lines,"failed to parse braching fraction correctly")
    else:
        branching_fraction = branching_fraction * scale
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

    while (first_column[0].find('\\') != -1):
        if (first_column[0].find('[') != -1):
            mini_column = [first_column[0][first_column[0].find('['):].rstrip('\\ ')]
            first_column[0] = first_column[0][:first_column[0].find('[')]
            if (first_column[1].find(']') == -1):
                mini_column.append(first_column[1][36:].strip().rstrip('\\'))
                first_column[1] = first_column[1][:36].rstrip()
                mini_column.append(first_column[2][36:])
                first_column[2] = first_column[2][:36].rstrip()
                if (first_column[2] == ''):
                    first_column.pop(2)
            else:
                mini_column.append(first_column[1][36:])
                first_column[1] = first_column[1][:36].rstrip()
            continue
        first_column[0] = first_column[0].strip().rstrip("\\")
        first_column[0] = first_column[0] + first_column[1]
        first_column.pop(1)

    try:
        second_column[0].find('\\ ')
    except IndexError:
        print "IndexError in the following", lines
        raise
    else:
        while (second_column[0].find('\\ ') != -1):
            second_column[0] = second_column[0].rstrip("\\ ")
            second_column[0] = second_column[0] + second_column[1]
            second_column.pop(1)
    try:
        third_column[0].find('\\ ')
    except IndexError:
        print "IndexError in the following", lines
        raise
    else:
        while (third_column[0].find('\\ ') != -1):
            third_column[0] = third_column[0].rstrip("\\ ")
            third_column[0] = third_column[0] + third_column[1]
            third_column.pop(1)

    if (len(first_column) > 1):
        first_column[1] = first_column[1].strip()
        if (first_column[1] == ''):
            first_column.pop(1)
        else:
            raise ParseError(input_lines,"string '" + first_column[1] + "' should be empty")
    if (len(first_column) == 1):
        first_column = first_column[0]
        first_column = first_column.strip()
    else:
        raise ParseError(input_lines,"the list first_column should only have 1 item, but it currently has " + str(len(first_column)) + ":" + str(first_column))
    if (len(second_column) == 1):
        second_column = second_column[0]
        second_column = second_column.strip()
    else:
        print "the list second_column should only have 1 item, but it currently has " + str(len(second_column))
        print input_lines
        raise ParseError(input_lines,"the list second_column should only have 1 item, but it currently has " + str(len(second_column)))
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

    flags = set(['L', 'B', 'LF', 'B1'])
    first_column = first_column.split()
    while (first_column[-1].strip(',') in flags):
        mini_column = first_column.pop(-1).strip(',') + " " + mini_column
    first_column = ' '.join(first_column)
    mini_column = mini_column.strip()

    return first_column, second_column, third_column, mini_column




























