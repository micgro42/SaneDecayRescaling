class hep_translator:
    """translate particle names from one set into another"""
    pdg_evtgen_dict = {
            'D*(2010)+-': 'D*+-',
            'D*(2010)+': 'D*+',
            'D*(2010)-': 'D*-',
    }

    def __init__(self):
        self.evtgen_pdg_dict = {v: k for k, v in self.pdg_evtgen_dict.iteritems()}


    def translate_pdg_to_evtgen(self, pdg_particle_name):
        """Return the name of the particle in an EvtGen Decay-File
        :param pdg_particle_name: name of a particle in the pdg ascii-file
        :type pdg_particle_name: string
        """
        if pdg_particle_name in self.pdg_evtgen_dict:
            return self.pdg_evtgen_dict[pdg_particle_name]
        else:
            return pdg_particle_name
    def translate_evtgen_to_pdg(self, evtgen_particle_name):
        """Return the name of the particle in an pdg ASCII-File
        :param evtgen_particle_name: name of a particle in the evtgen decay.dec
        :type evtgen_particle_name: string
        """
        if evtgen_particle_name in self.evtgen_pdg_dict:
            return self.evtgen_pdg_dict[evtgen_particle_name]
        else:
            return evtgen_particle_name