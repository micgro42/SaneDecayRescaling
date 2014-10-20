"""
provide class hep_translator


"""
class HepTranslator(object):
    """
    translate particle names from one set into another

    """
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
            'K(1)(1270)0': 'K_10',
            'K(1)(1270)-': 'K_1-',
            'K(1)(1270)+': 'K_1+',
            'K(1)(1400)0': "K'_10", #.. todo:: K'_10 and anti-K'_10 should translate equivalently?
            'K(1)(1270)0': "anti-K'_10", #maybe this should be Kbar(1)(1270)0
            'K(1)(1400)-': "K'_1-",
            'K(1)(1400)+': "K'_1+",
            'K(0)*(1430)0': 'K_0*0',
            'K(0)*(1430)-': 'K_0*-',
            'K(0)*(1430)+': 'K_0*+',
            'D*(2010)+-': 'D*+-',
            'D*(2010)+': 'D*+',
            'D*(2010)-': 'D*-',
            'Dbar0': 'anti-D0',
            'D*(2007)0': 'D*0',
            'Dbar*(2007)0': 'anti-D*0',
            'D(0)*(2400)0': 'D_0*0',
            'D(0)*(2400)-': 'D_0*-',
            'D(0)*(2400)+': 'D_0*+',
            'D(0)*0': 'D_0*0',
            'D(0)*-': 'D_0*-',
            'D(0)*+': 'D_0*+',
            'D(1)(2420)0': 'D_10',
            'D(1)(2420)-': 'D_1-',
            'D(1)(2420)+': 'D_1+',
            'D(1)0': 'D_10',
            'D(1)-': 'D_1-',
            'D(1)+': 'D_1+',
            'D(2)*(2460)0': 'D_2*0',
            'D(2)*(2460)-': 'D_2*-',
            'D(2)*(2460)+': 'D_2*+',
            'D(2)*0': 'D_2*0',
            'D(2)*-': 'D_2*-',
            'D(2)*+': 'D_2*+',
            'D(1)(2420)0': "D'_10",
            'D(1)(2420)+': "D'_1+",
            'D(1)(2420)-': "D'_1-",
            'D(s)-': 'D_s-',
            'D(s)+': 'D_s+',
            'D(s)*-': 'D_s*-',
            'D(s)*+': 'D_s*+',
            'D(s0)*(2317)+': 'D_s0*+',
            'D(s0)*(2317)-': 'D_s0*-',
            'D(s1)(2460)+': 'D_s1+',
            'D(s1)(2460)-': 'D_s1-',
            'D(s1)(2536)+': "D'_s1+",
            'D(s1)(2536)-': "D'_s1-",
            'phi(1020)': 'phi',
            "eta'(958)": "eta'",
            'eta(c)': 'eta_c',
            'eta(c)(2S)': 'eta_c(2S)',
            'chi(c0)': 'chi_c0',
            'chi(c1)': 'chi_c1',
            'chi(c2)': 'chi_c2',
            'J/psi(1S)': 'J/psi',
            'p': 'p+',
            'pbar': 'anti-p-',
            'n': 'n0',
            'nbar': 'anti-n0',
            'Lambda': 'Lambda0',
            'Lambdabar': 'anti-Lambda0',
            'Lambda(c)+': 'Lambda_c+',
            'Lambda(c)-': 'anti-Lambda_c-',
            'Xi(c)0': 'Xi_c0',
            'Xibar(c)0': 'anti-Xi_c0',
            'a(0)0': 'a_00',
            'a(0)+': 'a_0+',
            'a(0)-': 'a_0-',
            'a(1)(1260)0': 'a_10',
            'a(1)(1260)+': 'a_1+',
            'a(1)(1260)-': 'a_1-',
            'a(1)0': 'a_10',
            'a(1)+': 'a_1+',
            'a(1)-': 'a_1-',
            'a(2)(1320)0': 'a_20',
            'a(2)(1320)+': 'a_2+',
            'a(2)(1320)-': 'a_2-',
            'a(2)0': 'a_20',
            'a(2)+': 'a_2+',
            'a(2)-': 'a_2-',
            'b(1)(1235)0': 'b_10',
            'b(1)(1235)-': 'b_1-',
            'b(1)(1235)+': 'b_1+',
            'b(1)0': 'b_10',
            'b(1)-': 'b_1-',
            'b(1)+': 'b_1+',
            'f(0)(980)': 'f_0',
            'f(0)(1500)': 'f_0(1500)',
            'f(1)(1285)': 'f_1',
            'f(2)(1270)': 'f_2',
    }

    """
    the pdg ascii-file usually doesn't show the antiparticles seperately
    """
    pdg_anti_particle_dict={
            'p':'pbar',
            'n':'nbar',
            'e+': 'e-',
            'mu+': 'mu-',
            'tau+': 'tau-',
            'nu(e)': 'nubar(e)',
            'nu(mu)': 'nubar(mu)',
            'nu(tau)': 'nubar(tau)',
            'pi+': 'pi-',
            'rho+': 'rho-',
            'K+': 'K-',
            'K0': 'Kbar0',
            'K*(892)+': 'K*(892)-',
            'K*(892)0': 'Kbar*(892)0',
            'D+': 'D-',
            'D0': 'Dbar0',
            'D*(2010)+': 'D*(2010)-',
            'D(s)+': 'D_s-',
    }

    """
    some particles have two names in the pdg ascii file
    """
    pdg_alt_names={}

    def __init__(self):
        self.evtgen_pdg_dict = {v: k for k, v in self.pdg_evtgen_dict.iteritems()}
        self.pdg_anti_particle_inv_dict = {v: k for k, v in self.pdg_anti_particle_dict.iteritems()}


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

    def translate_pdg_anti_particle(self, pdg_particle_name):
        """Translate the name of a particle to it's anti-particle"""
        if pdg_particle_name in self.pdg_anti_particle_dict:
            anti_particle_name = self.pdg_anti_particle_dict(pdg_particle_name)
        elif pdg_particle_name in self.pdg_anti_particle_inv_dict:
            anti_particle_name = self.pdg_anti_particle_inv_dict(pdg_particle_name)
        else:
            anti_particle_name = pdg_particle_name

        return anti_particle_name