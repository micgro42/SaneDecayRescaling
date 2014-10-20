import pytest
from sanedecayrescaling.particle import ParticleDecays



def test_D0phiKK():
    reference_file = open('reference_file.tmp','w');
    reference_file.writelines([
"                                                               Scale factor/  p\n", 
"D+ DECAY MODES                          Fraction (G(i)/G)             CL(MeV\\\n",
"                                                                        /c)\n", 
"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n", 
" \n",
"                               Inclusive modes\n",
" \n",
"eta'(958) e+ nu(e)                       ( 2.2 +-0.5       )E-4           689\n",
"phi e+ nu(e)                            <  9          E-5         CL=90%  657\n",
"      Fractions of some of the following modes with resonances have\n",
"      already appeared above as submodes of particular\n",
"      charged-particle modes.\n",
" \n",
"Kbar*(892)0 e+ nu(e)                     ( 5.52+-0.15      )%             722\n",
" \n",
"=============================================================================\n",
"======\n",
"| D0 |\n",
"======\n"])
    reference_file.close()
    my_particle = ParticleDecays('D+',ref_file_path = 'reference_file.tmp')
    br, brep, brem = my_particle.get_branching_fraction(['Kbar*(892)0', 'e+', 'nu(e)'])
    assert br == 0.0552
    assert brep == 0.0015
    assert brem == 0.0015