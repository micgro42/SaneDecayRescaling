"""This module provides functions to extract data from files (source and reference)
"""
import os
import sanedecayrescaling
def extract_decays_from_decay(path_to_decay_file, particle, work_file_name="workfile.tmp"):
    """get the decays from an EvtGen Decay.Dec file and write them to disk

    returns:
        - 0 on success
        - Exception otherwise
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
        stringfound = line.find("Decay " + particle + "\n")
        if (line == ""):
            print "String 'Decay %s' not found!" % (particle)
            raise SystemExit(os.EX_DATAERR)

    stringfound = -1
    workfile = open(work_file_name, 'w')
    workfile.write(line)
    linenumber_end_decay = linenumber_begin_decay
    while (stringfound == -1):
        linenumber_end_decay += 1
        line = evtgen_decay_dec.readline()
        stringfound = line.find("Enddecay\n")
        workfile.write(line)
        if (line == ""):
            print "String 'Enddecay' not found!"
            raise SystemExit(os.EX_DATAERR)

    workfile.close()
    evtgen_decay_dec.close()
    return 0

def extract_decays_from_reference(path_to_reference_file, particle, ref_file_name="workreffile.tmp"):
    """
    Extracts decay of particle from reference file

    The functionality to extract the decay of an anti-particle to a particle in
    the reference file is not yet implemented.

    returns:
        - nothing

    creates:
        - file ref_file_name, which defaults to workreffile.tmp
    """
    _t = sanedecayrescaling.translate_particles.HepTranslator()
    particle = _t.translate_evtgen_to_pdg(particle)
    reference_file = sanedecayrescaling.utility.open_file_safely(path_to_reference_file, 'r')

    file_position_begin_decay, linenumber_begin_decay, decay_length = find_particle_in_reference(particle, reference_file)
    reference_file.seek(file_position_begin_decay, 0)
    reference_file.readline()
    reference_file.readline()

    work_reference_file = open(ref_file_name,'w')
    work_reference_file.write("Decay " + _t.translate_pdg_to_evtgen(particle) +"\n")
    position_in_decay = 0
    for line in iter(reference_file.readline, ''):
        position_in_decay += 1
        if (position_in_decay > decay_length ):
            break
        if (line == '\n'):
            continue
        if (line[0] == ' '):
            continue
        if (line[0] == '['):
            continue # TODO: Confirm that this is actually correct behavior
        decay_lines = line
        if (line.find('\\') != -1):
            next_line = reference_file.readline()
            decay_lines = decay_lines + next_line
            position_in_decay += 1
            if (next_line.find('\\') != -1):
                next_line = reference_file.readline()
                decay_lines = decay_lines + next_line
                position_in_decay += 1


        try:
            daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = extract_decay_from_lines(decay_lines)
        except (IndexError) as ex:
            print "IndexError in line", linenumber_begin_decay + position_in_decay + 2
            print decay_lines
            raise
        except (sanedecayrescaling.utility.ParseError) as ex:
            print "ParseError in line", linenumber_begin_decay + position_in_decay + 2
            print ex.msg
            print ex.line
            raise
        except (sanedecayrescaling.utility.BadData) as ex:
            daughters = ex.daughters
            branching_fraction = "bad"
            branching_fraction_error_plus = "bad"
            branching_fraction_error_minus = "bad"
        except:
            print "Error in line", linenumber_begin_decay + position_in_decay + 2
            raise
        for i, daughter_in_decay in enumerate(daughters):
            daughters[i] = _t.translate_pdg_to_evtgen(daughter_in_decay)
        extracted_line = str(branching_fraction) + ' ' + str(branching_fraction_error_plus) + ' ' + str(branching_fraction_error_minus) + ' ' + ' '.join(daughters) + '\n'
        work_reference_file.write(extracted_line)

    work_reference_file.write('Enddecay\n')
    work_reference_file.close()
    reference_file.close()


def extract_decay_from_lines(lines):
    """
    parse lines from a decayfile into decay-daughters, branching fraction, errors

    returns:
        - daughters: list of strings
        - branching_fraction: float
        - branching_fraction_error_plus, branching_fraction_error_plus: float
        - 0 errors for limit cases
        - 0 branching fraction for cases of "not seen"
    .. todo:: Expand the section on subdecays to allow a second subdecay
    .. todo:: better handling for the exceptions from subdecay defolding
    """
    column1, column2, column3, column_mini = make_single_line_snippets(lines)
    lines = lines.split("\n")

# get scale of numbers
    if (column2.find('%') != -1):
        scale = 0.01
        column2 = column2.rstrip('%')
    exponent_position = column2.find('E-')
    if (exponent_position != -1):
        scale = 1 / (10 ** float(column2[exponent_position + 2]))
        column2 = column2[:exponent_position]

# get daughters
    while (column1[0] == '.'):
        column1 = column1[1:]
    daughters = column1.split()
    # defold multiplicity
    for index, daughter in enumerate(daughters):
        if (daughter[0].isdigit()):
            mutliplicity = int(daughter[0])
            daughter = daughter[1:]
            daughters[index] = daughter
            for i in range(1, mutliplicity):
                daughters.insert(index, daughter)
    # handle sub decays with products
    subdecay_br = 0
    subdecay_brep = 0
    subdecay_brem = 0
    if (',' in daughters):  # /todo there is possibly more than one subdecay per decay
        sep_position = daughters.index(',')
        subdecay = daughters[sep_position + 1:]
        print subdecay
        daughters = daughters[:sep_position]
        print daughters
        subdecay_mother = subdecay.pop(0)
        subdecay_daughters = subdecay[1:]
        try:
            with sanedecayrescaling.particle.ParticleDecays(subdecay_mother, ref_file_path='PDG2012-SummaryTables-ASCII.txt') as subdecay:  # /todo get the ref_file_path from an argument or variable
                subdecay_br, subdecay_brep, subdecay_brem = subdecay.get_branching_fraction(subdecay_daughters)
        except:  # /todo: decent exception handling
            pass

# get branching fraction and errors
    try:
        column2[0]
    except IndexError:
        raise sanedecayrescaling.utility.BadData(lines, daughters)
    if (column2[0] == '('):  # default
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
    elif (column2[0] == '<'):  # limit
        column2 = column2.lstrip('<')
        column2 = column2.strip()
        branching_fraction = column2
        branching_fraction_error_plus = 0
        branching_fraction_error_minus = 0
    elif (column2[0] == 's'):  # seen
        branching_fraction = 0
        branching_fraction_error_plus = 0
        branching_fraction_error_minus = 0
        scale = 0
    elif (column2[0] == 'n'):  # not seen
        branching_fraction = 0
        branching_fraction_error_plus = 0
        branching_fraction_error_minus = 0
        scale = 0
    elif (column2[0] == 'l'):  # large
        pass
    elif (column2[0] == 'd'):  # dominant
        branching_fraction = 1
        branching_fraction_error_plus = 0
        branching_fraction_error_minus = 0
        scale = 1
    else:
        raise sanedecayrescaling.utility.ParseError(lines, "first char in '" + column2 + "' not implemented")

    try:
        branching_fraction = float(branching_fraction)
        branching_fraction_error_plus = float(branching_fraction_error_plus)
        branching_fraction_error_minus = float(branching_fraction_error_minus)
    except ValueError:
        print "branching_fraction:", branching_fraction
        print "branching_fraction_error_plus:", branching_fraction_error_plus
        print "branching_fraction_error_minus:", branching_fraction_error_minus
        raise sanedecayrescaling.utility.ParseError(lines, "failed to parse branching fraction correctly")
    else:
        branching_fraction = branching_fraction * scale
        branching_fraction_error_plus = branching_fraction_error_plus * scale
        branching_fraction_error_minus = branching_fraction_error_minus * scale
        if (subdecay_br > 0):
            branching_fraction = branching_fraction / subdecay_br


    return daughters, branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus


def make_single_line_snippets(input_lines):
    """
    create and return reconstructed snippets

    The ascii-refernece file has more or less 3 columns, the first until 40 chars
    the second column goes to 66, after which comes the last colum, which is
    irrelevant.
    The indicator for a multi-line decay is the presence of a '\' char, which
    signals a linebreak for that column.
    This first column contains the decay products and and sometimes some other
    characters, the second column contains the branching fraction

    returns:
        - first_column: string with the decay products
        - second_column: string with the branching fractions if existent
        - third_column: string with phase space, confidence limit and scale
        - mini_column: flags removed from first column
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
    flag_list = ''
    while (first_column[0].find('\\') != -1):
        first_column[0], flag_list = remove_flags(first_column[0], flag_list)
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
            raise sanedecayrescaling.utility.ParseError(input_lines, "string '" + first_column[1] + "' should be empty")
    if (len(first_column) == 1):
        first_column = first_column[0]
        first_column = first_column.strip()
    else:
        raise sanedecayrescaling.utility.ParseError(input_lines, "the list first_column should only have 1 item, but it currently has " + str(len(first_column)) + ":" + str(first_column))
    if (len(second_column) == 1):
        second_column = second_column[0]
        second_column = second_column.strip()
    else:
        print "the list second_column should only have 1 item, but it currently has " + str(len(second_column))
        print input_lines
        raise sanedecayrescaling.utility.ParseError(input_lines, "the list second_column should only have 1 item, but it currently has " + str(len(second_column)))
    if (len(third_column) == 1):
        third_column = third_column[0]
        third_column = third_column.strip()
    else:
        raise sanedecayrescaling.utility.ParseError(input_lines, "the list third_column should only have 1 item, but it currently has " + len(third_column))

    while (len(mini_column) > 1):
        mini_column[0] = mini_column[0] + mini_column[1]
        mini_column.pop(1)
    if (len(mini_column) == 1):
        mini_column = mini_column[0]
    else:
        mini_column = ''

    first_column, flag_list = remove_flags(first_column, flag_list)
    mini_column = flag_list + " " + mini_column
    mini_column = mini_column.strip()

    return first_column, second_column, third_column, mini_column



def remove_flags(column, flag_list):
    """returns the column without the flags at the end, which have been added
    to the flag list, which is also returned

    returns:
        - column: input column string minus the flags
        - flag_list: input flag_list string with the flags added in front
    """
    flags = set(['L',
                 'B',
                 'LF',
                 'B1',
                 'C1',
                 'DC',
                 'CP',
                 '3-body',
                 'parallel',
                 'perpendicular',
                 'longitudinal',
                 'helicities'])
    column = column.split()
    while (column[-1].strip(',') in flags):
        flag_list = column.pop(-1).strip(',') + " " + flag_list
    column = ' '.join(column)
    column = column.rstrip().rstrip(',').rstrip()
    flag_list = flag_list.strip()
    return column, flag_list


def find_particle_in_reference(particle, ref_file):
    """
    find the particle in the pdg ascii file

    :param particle: pdg name of the particle
    :type particle: string

    :param ref_file: the file which should be searched
    :type ref_file: open file handle


    :returns: - (*int*) file position for the begin of the decay
              - (*int*) linenumber of the first line for the decay of this particle
              - (*int*) decay length
    """
    string_found = -1
    linenumber_begin_decay = 0
    for line in iter(ref_file.readline, ''):
        linenumber_begin_decay += 1
        string_found = line.find(particle + " DECAY MODES")
        if (string_found != -1):
            file_position_begin_decay = ref_file.tell()
            break
#   if (string_found == -1):
    else:
        print "String '%s DECAY MODES' not found!" % (particle)
        raise SystemExit(os.EX_DATAERR)



    string_found = -1
    linenumber_end_decay = linenumber_begin_decay
    end_decay_string = "==========================================="
    for line in iter(ref_file.readline, ''):
        linenumber_end_decay += 1
        string_found = line.find(end_decay_string)
        if (string_found != -1):
            break
        if (line == ""):
            print "String '%s' not found!" % (end_decay_string)
            raise SystemExit(os.EX_DATAERR)

    decay_length = (linenumber_end_decay - 2) - (linenumber_begin_decay + 2)
#    print "decay_length", decay_length
    return file_position_begin_decay, linenumber_begin_decay, decay_length


















