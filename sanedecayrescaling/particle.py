class particle_decays(object):
    """
    @TODO: Description of class particle_decays

    """

    def __init__(self, particle):
        self.particle = particle

    def get_branching_fraction(self, daughters):
        """get the branching fraction for a specific decay if available

        returns:
            - branching_fraction: float
            - branching_fraction_error_plus: float
            - branching_fraction_error_minus: float
        """
        pass

    def read_pdg_reference(self, path_to_reference_file):
        pass
