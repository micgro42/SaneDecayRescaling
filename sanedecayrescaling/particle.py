import translate_particles
import extract_decays
import check_sanity
import os
class particle_decays(object):
    """
    @TODO: Description of class particle_decays

    """

    def __init__(self, particle, *args, **kwargs):
        self.particle = particle
        self.ref_file_path = kwargs.get('ref_file_path','')
        if (self.ref_file_path is not ''):
            self.read_pdg_reference(self.ref_file_path)

    def get_branching_fraction(self, daughters):
        """get the branching fraction for a specific decay if available

        returns:
            - branching_fraction: float
            - branching_fraction_error_plus: float
            - branching_fraction_error_minus: float
        """
        t = translate_particles.hep_translator()
        daughters = map(t.translate_pdg_to_evtgen, daughters)
        branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = check_sanity.find_decay_in_reference(self.ref_file, daughters, 0)
        return branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus

    def read_pdg_reference(self, path_to_reference_file):
        """
        extract the decays from a reference file and store them in local var

        """
        extract_decays.extract_decays_from_reference(path_to_reference_file, self.particle, self.particle + "_ref.tmp")
        self.ref_file = open(self.particle + "_ref.tmp")
        self.reflines = self.ref_file.readlines()
        #ref_file.close() #@TODO: properly
        #os.remove(self.particle + "_ref.tmp")
