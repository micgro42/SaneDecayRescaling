import os
import sanedecayrescaling


def check_sanity(path_to_decayfile, path_to_referencefile, particle):
    """extract decays of a particle from a source file and compare them with a reference

    The function will print out warnings if
        I. The decay is not found in the reference
        II. The decay is found, but the branching fraction in the source differs by more than 1 sigma from the branching fraction in the reference
        III. The decay is found, but the branching fraction in the source is larger than the limit in the reference

    This function will also print some statistics at the end
    """

    if (sanedecayrescaling.extract_decays.extract_decays_from_decay(path_to_decayfile, particle) != 0):
        print "ERROR finding decay in Source File. Exiting"
        raise SystemExit(os.EX_DATAERR)

    workfile = sanedecayrescaling.utility.open_file_safely("workfile.tmp", 'r')
    referencefile = sanedecayrescaling.utility.open_file_safely(path_to_referencefile, 'r')
    generators_set = get_generators()

    number_of_decays_found = 0
    pdg_br_decays_found = 0
    evtgen_br_decays_found = 0
    number_of_decays_not_found = 0
    evtgen_br_decays_not_found = 0
    number_of_decays_skipped_pythia = 0
    evtgen_br_decays_skipped = 0
    number_of_decays_skipped_0br = 0

    number_of_not_found_because_pi0 = 0

    phi_decays_found = 0
    br_phi_decays_found = 0
    phi_decays_not_found = 0
    br_phi_decays_not_found = 0

    eta_decays_found = 0
    br_eta_decays_found = 0
    eta_decays_not_found = 0
    br_eta_decays_not_found = 0

    etap_decays_found = 0
    br_etap_decays_found = 0
    etap_decays_not_found = 0
    br_etap_decays_not_found = 0


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
                number_of_decays_skipped_0br += 1
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
                evtgen_br_decays_skipped += branching_ratio
                continue
            second_last_element = parts.pop(-1)
            while (second_last_element in generators_set):
                second_last_element = parts.pop(-1)
            parts.append(second_last_element)


            pdg_branching_ratio, pdg_branching_ratio_error_plus, \
            pdg_branching_ratio_error_minus = find_decay_in_reference(referencefile, parts, branching_ratio)
            if (pdg_branching_ratio == -1): # TODO: replace print with raise warning and write appropriate tests
                print "Warning: Decay ", particle, "to", parts, "not found"
                number_of_decays_not_found += 1
                evtgen_br_decays_not_found += branching_ratio
                for elem in parts:
                    if (elem == 'pi0'):
                        parts.remove('pi0')
                        tmp_br, tmp_brep, tmp_brem = find_decay_in_reference(referencefile, parts, branching_ratio)
                        if (tmp_br != -1):
                            number_of_not_found_because_pi0 += 1
                            break
            # \TODO: include pdg_branching_ratio == 0 case (not seen)
            elif (pdg_branching_ratio_error_plus == 0):
                #print "Warning: Decay ", particle, "to", parts, " is a limit decay"
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
                pdg_br_decays_found += pdg_branching_ratio
                evtgen_br_decays_found += branching_ratio
                if ('phi' in parts):
                    phi_decays_found += 1
                    br_phi_decays_found += branching_ratio
                if ('eta' in parts):
                    eta_decays_found += 1
                    br_eta_decays_found += branching_ratio
                if ("eta'" in parts):
                    etap_decays_found += 1
                    br_etap_decays_found += branching_ratio
            else:
                if ('phi' in parts):
                    phi_decays_not_found += 1
                    br_phi_decays_not_found += branching_ratio
                if ('eta' in parts):
                    eta_decays_not_found += 1
                    br_eta_decays_not_found += branching_ratio
                if ("eta'" in parts):
                    etap_decays_not_found += 1
                    br_etap_decays_not_found += branching_ratio
    print "\n"
    print "*****************************"
    print "******** Statistics *********"
    print "*****************************"
    print "particle:", particle
    print "reference file used:", path_to_referencefile
    print "decay file used:", path_to_decayfile, "\n"
    
    print "number of decays found:", number_of_decays_found
    print "summed EvtGen branching ratio of decays found:", evtgen_br_decays_found
    print "summed pdg branching ratio of decays found:", pdg_br_decays_found, "\n"
    
    print "number of decays not found:", number_of_decays_not_found
    print "summed EvtGen branching ratio of decays not found:", evtgen_br_decays_not_found, "\n"
    
    print "Number of the Decays skipped because they are done by pythia:", number_of_decays_skipped_pythia
    print "summed EvtGen branching ratio of the decays skipped:", evtgen_br_decays_skipped, "\n"
    
    print "sum of the above EvtGen branching ratios:", evtgen_br_decays_found + evtgen_br_decays_not_found + evtgen_br_decays_skipped
    print "number of decays skipped because the branching ratio is 0:", number_of_decays_skipped_0br, "\n"

    print "number of decays not found because of one or more additional pi0:", number_of_not_found_because_pi0
    if (number_of_decays_not_found > 0):
        print "that are ", 100.0 * number_of_not_found_because_pi0 / number_of_decays_not_found, "% of the decays not found.\n"

    print "number of phi decays found:", phi_decays_found
    print "braning ratio of phi decays found:", br_phi_decays_found
    print "number of phi decays not found:", phi_decays_not_found
    print "braning ratio of phi decays not found:", br_phi_decays_not_found
    if (br_phi_decays_found + br_phi_decays_not_found > 0):
        print "percentage (BR) of phi decays found:", 100*br_phi_decays_found/(br_phi_decays_found + br_phi_decays_not_found), "\n"

    
    print "number of eta decays found:", eta_decays_found
    print "braning ratio of eta decays found:", br_eta_decays_found
    print "number of eta decays not found:", eta_decays_not_found
    print "braning ratio of eta decays not found:", br_eta_decays_not_found
    if (br_eta_decays_found + br_eta_decays_not_found > 0):
        print "percentage (BR) of eta decays found:", 100*br_eta_decays_found/(br_eta_decays_found + br_eta_decays_not_found), "\n"
    
    print "number of eta' decays found:", etap_decays_found
    print "braning ratio of eta' decays found:", br_etap_decays_found
    print "number of eta' decays not found:", etap_decays_not_found
    print "braning ratio of eta' decays not found:", br_etap_decays_not_found
    if (br_etap_decays_found + br_etap_decays_not_found > 0):
        print "percentage (BR) of eta' decays found:", 100*br_etap_decays_found/(br_etap_decays_found + br_etap_decays_not_found), "\n"
    workfile.close()
    referencefile.close()
    return 0


def get_generators():
    """return a set of the generators used in the EvtGen Decay.dec file""" 
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



def find_decay_in_reference(referencefile, decay_list, br=0):
    """search for decay in provided reference file

    The reference file created by extract_decays_from_reference() is searched
    for the decay into the given particles and the first match is returned
    
    If the decay contains a K_0L and is not found then it tries again with 
    the K_0L replaced by K_0S.

    returns:
        - branching_ratio: float
        - branching_ratio_error_plus: float
        - branching_ratio_error_minus: float
        - -1 for all variables if the decay is not found
    """

    decay_list.sort()
    referencefile.seek(0)
    decay_found = False
    found_decays = []
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
                distance = abs(br - branching_ratio) # /TODO: decide if sigma would be a better measure here.
                decay_tuple = distance, branching_ratio, branching_ratio_error_plus, branching_ratio_error_minus
                found_decays.append(decay_tuple)

    if (decay_found):
        if (len(found_decays) > 1):
            print "Warning, this decays has been found more than once in the decayfile"
            #.. todo:: Add some way to count these multiple occurrences
            found_decays.sort(key = lambda tup: tup[0])
        return found_decays[0][1], found_decays[0][2], found_decays[0][3]
    elif ('K_L0' in decay_list):
        mod_decay_list = []
        for particle in decay_list:
            if (particle == 'K_L0'):
                mod_decay_list.append('K_S0')
            else:
                mod_decay_list.append(particle)
        return find_decay_in_reference(referencefile, mod_decay_list, br)
    else:
        return -1, -1, -1






