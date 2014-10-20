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
        self.source_file_path = kwargs.get('source_file_path','')
        if (self.ref_file_path is not ''):
            self.read_pdg_reference(self.ref_file_path)
        if (self.source_file_path is not ''):
            self.read_evtgen_source(self.source_file_path)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if os.path.isfile(self.particle + "_ref.tmp"):
            os.remove(self.particle + "_ref.tmp")
        if os.path.isfile(self.particle + "_source.tmp"):
            os.remove(self.particle + "_source.tmp")


    def get_branching_fraction(self, daughters):
        """get the branching fraction for a specific decay if available

        returns:
            - branching_fraction: float
            - branching_fraction_error_plus: float
            - branching_fraction_error_minus: float
        """
        t = translate_particles.HepTranslator()
        daughters = map(t.translate_pdg_to_evtgen, daughters)
        branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus = check_sanity.find_decay_in_reference(self.ref_file, daughters, 0)
        return branching_fraction, branching_fraction_error_plus, branching_fraction_error_minus

    def read_pdg_reference(self, path_to_reference_file):
        """
        extract the decays from a reference file and store them in local var

        """
        extract_decays.extract_decays_from_reference(path_to_reference_file, self.particle, self.particle + "_ref.tmp")
        self.ref_file = open(self.particle + "_ref.tmp")
        self.ref_lines = self.ref_file.readlines()
        #ref_file.close() #@TODO: properly handle files and remove them when done
        #os.remove(self.particle + "_ref.tmp")

    def read_evtgen_source(self, path_to_source):
        """
        extract data from a evtgen source file
        """
        extract_decays.extract_decays_from_decay(path_to_source, self.particle, self.particle + "_source.tmp")
        self.source_file = open(self.particle + "_source.tmp")
        self.source_lines = self.source_file.readlines()

    def check_sanity(self):
        pass
        