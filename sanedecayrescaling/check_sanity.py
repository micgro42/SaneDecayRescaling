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

    number_of_decays_found = 0
    pdg_BR_decays_found = 0
    evtgen_BR_decays_found = 0
    number_of_decays_not_found = 0
    evtgen_BR_decays_not_found = 0
    number_of_decays_skipped_pythia = 0
    evtgen_BR_decays_skipped = 0
    number_of_decays_skipped_0BR = 0



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
            if (branching_ratio == 0.0): # TODO: research what decays are affected by this and if they are relevant
                number_of_decays_skipped_0BR += 1
                continue
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
            if (last_element == 'PYTHIA'):
                number_of_decays_skipped_pythia +=1
                evtgen_BR_decays_skipped += branching_ratio
                continue
            second_last_element = parts.pop(-1)
            while (second_last_element in generators_set):
                second_last_element = parts.pop(-1)
            parts.append(second_last_element)


            pdg_branching_ratio, pdg_branching_ratio_error_plus, \
            pdg_branching_ratio_error_minus = find_decay_in_reference(referencefile, parts)
            if (pdg_branching_ratio == -1): # TODO: replace print with raise warning and write appropriate tests
                print "Warning: Decay ", particle, "to", parts, "not found"
                number_of_decays_not_found += 1
                evtgen_BR_decays_not_found += branching_ratio
            # \TODO: include pdg_branching_ratio == 0 case (not seen)
            elif (pdg_branching_ratio_error_plus == 0):
                print "Warning: Decay ", particle, "to", parts, " is a limit decay"
                if (branching_ratio > pdg_branching_ratio):
                    print "branching ratio of ", branching_ratio, " exceeds limit of ", pdg_branching_ratio
                else:
                    pass
#                    print "branching ratio of ", branching_ratio, " doesn't exceed limit of ", pdg_branching_ratio 
            elif (abs((pdg_branching_ratio-branching_ratio)/pdg_branching_ratio_error_plus) > 1): 
                print "Warning: Decay ", particle, "to", parts, " has a different branching ratios in source and reference file"
                print "source file branching ratio: %f" % (branching_ratio)
                print "reference file branching ratio: %f +- %f" % (pdg_branching_ratio, pdg_branching_ratio_error_plus)
                print "deviation %f sigma" % (abs((pdg_branching_ratio-branching_ratio)/pdg_branching_ratio_error_plus))
                #TODO: deviation should be shown relative to the appropriate error
            if (pdg_branching_ratio != -1):
                number_of_decays_found += 1
                pdg_BR_decays_found += pdg_branching_ratio
                evtgen_BR_decays_found += branching_ratio
    print "\n"
    print "*****************************"
    print "******** Statistics *********"
    print "*****************************"
    print "particle:", particle
    print "reference file used:", path_to_referencefile
    print "decay file used:", path_to_decayfile, "\n"
    
    print "number of decays found:", number_of_decays_found
    print "summed EvtGen branching ratio of decays found:", evtgen_BR_decays_found
    print "summed pdg branching ratio of decays found:", pdg_BR_decays_found, "\n"
    
    print "number of decays not found:", number_of_decays_not_found
    print "summed EvtGen branching ratio of decays not found:", evtgen_BR_decays_not_found, "\n"
    
    print "Number of the Decays skipped because they are done by pythia:", number_of_decays_skipped_pythia
    print "summed EvtGen branching ratio of the decays skipped:", evtgen_BR_decays_skipped, "\n"
    
    print "sum of the above EvtGen branching ratios:", evtgen_BR_decays_found + evtgen_BR_decays_not_found + evtgen_BR_decays_skipped
    print "number of decays skipped because the branching ratio is 0:", number_of_decays_skipped_0BR
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
            branching_ratio = parts.pop(0)
            branching_ratio = float(branching_ratio)
            branching_ratio_error_plus = parts.pop(0)
            branching_ratio_error_plus = float(branching_ratio_error_plus)
            branching_ratio_error_minus = parts.pop(0)
            branching_ratio_error_minus = float(branching_ratio_error_minus)
        except ValueError:
            pass
        else:
            parts.sort()
#             print parts
            if (decay_list == parts):
                decay_found = True
                break
    if (decay_found):
        return branching_ratio, branching_ratio_error_plus, branching_ratio_error_minus
    else:
        return -1, -1, -1






