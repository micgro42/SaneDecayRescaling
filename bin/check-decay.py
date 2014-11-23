#!/usr/bin/env python
import argparse
import sanedecayrescaling.particle as part

script_description = ('Compare the decays of a particle in an EvtGen decayfile' +
' to the value provided by a reference file from the particle data group.')
parser = argparse.ArgumentParser(description=script_description)
parser.add_argument("reference", help="path to the PDG reference file")
parser.add_argument("source", help="path to the EvtGen .dec file")
parser.add_argument("particle",
                    help="particle whose decays should be checked")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
parser.add_argument("-l", "--log-file",
                    help="if specified, create full log at given location")
args = parser.parse_args()

with part.ParticleDecays(args.particle, source_file_path = args.source, ref_file_path = args.reference) as decays:
    decays.check_sanity()




if __name__ == "__main__":
    pass
