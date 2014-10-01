class hep_translator:
    """translate particle names from one set into another"""
    pdg_evtgen_dict = {
            'nu(e)': 'nu_e',
            'nubar(e)': 'anti-nu_e',
            'nu(mu)': 'nu_mu',
            'nubar(mu)': 'anti-nu_mu',
            'nu(tau)': 'nu_tau',
            'nubar(tau)': 'anti-nu_tau',
            'Kbar0': 'anti-K0',
            'Kbar*0': 'anti-K*0',
            'Kbar*(892)0': 'anti-K*0',
            'K(S)0': 'K_S0',
            'K(L)0': 'K_L0',
            'K*(892)+': 'K*+',
            'K*(892)-': 'K*-',
            'K*(892)0': 'K*0',
            'D*(2010)+-': 'D*+-',
            'D*(2010)+': 'D*+',
            'D*(2010)-': 'D*-',
            'Dbar0': 'anti-D0',
            'D*(2007)0': 'D*0',
            'Dbar*(2007)0': 'anti-D*0',
            'D(s)-': 'D_s-',
            'D(s)+': 'D_s+',
            'D(s)*-': 'D_s-',
            'D(s)*+': 'D_s*+',
            'eta(c)': 'eta_c',
            'J/psi(1S)': 'J/psi',
            'p': 'p+',
            'pbar': 'anti-p-',
            'Lambda': 'Lambda0',
            'Lambdabar': 'anti-Lambda0',
            'Lambda(c)+': 'Lambda_c+',
            'Lambda(c)-': 'anti-Lambda_c-',
            'Xi(c)0': 'Xi_c0',
            'Xibar(c)0': 'anti-Xi_c0'
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