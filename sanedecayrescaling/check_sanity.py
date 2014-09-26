import os
from extract_decays import *
import sanedecayrescaling.utility as utility
def check_sanity(path_to_decayfile, path_to_referencefile, particle):
    """extract and compare the decays with a reference


    """

    if (extract_decays_from_decay(path_to_decayfile, particle) != 0):
        print "ERROR finding decay in Source File. Exiting"
        raise SystemExit(os.EX_DATAERR)

    workfile = utility.open_file_safely("workfile.tmp", 'r')
    referencefile = utility.open_file_safely(path_to_referencefile, 'r')
    generators_set = get_generators()


    for i, line in enumerate(workfile):
        if (line == '\n'):
            continue
        parts = line.split()
        try:
            branching_ratio = parts.pop(0)
            branching_ratio = float(branching_ratio)
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


            reference_branching_ratio, reference_branching_ratio_error = find_decay_in_reference(referencefile, parts)
            if (reference_branching_ratio == -1):
                print "Warning: Decay ", particle, "to", parts, "not found"
            elif (reference_branching_ratio != branching_ratio):
                print "Warning: Decay ", particle, "to", parts, " has a different branching ratios in source and reference file"
                print "source file branching ratio: %f" % (branching_ratio)
                print "reference file branching ratio: %f +- %f" % (reference_branching_ratio, reference_branching_ratio_error)
                print "deviation %f sigma" % (abs((reference_branching_ratio-branching_ratio)/reference_branching_ratio_error))

    workfile.close()
    referencefile.close()
    return 0


def get_generators():
    generators = [
    "VSS",
    "VSP_PWAVE",
    "PHOTOS",
    "ISGW2",
    "VUB",
    "PHSP",
    "SVS",
    "SVV_HELAMP",
    "HELAMP",
    "BTOXSGAMMA",
    "SLN",
    "CB3PI-P00",
    "CB3PI-MPP",
    "STS",
    "PYTHIA",
    "PI0_DALITZ",
    "D_DALITZ",
    "VSS_BMIX",
    "VVS_PWAVE",
    "VVPIPI",
    "PARTWAVE",
    "ETA_DALITZ",
    "SVP_HELAMP",
    "BTO3PI_CP"]
    return set(generators)



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






