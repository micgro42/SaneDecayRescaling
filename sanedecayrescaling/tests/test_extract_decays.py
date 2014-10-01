import os
from sanedecayrescaling.extract_decays import extract_decays_from_decay as blub
from sanedecayrescaling.extract_decays import extract_decays_from_reference
from pytest import fixture
import pytest

@fixture  # Registering this function as a fixture.
def fixture_source(request):
    print "start setup"
    source_decay_file=open('source_decay_file.dec.tmp','w')
    source_decay_file.write("some lines at start\n")
    source_decay_file.write("Decay B0\n")
    source_decay_file.write("some lines 1\n")
    source_decay_file.write("some lines 2\n")
    source_decay_file.write("some lines 3\n")
    source_decay_file.write("some lines 4\n")
    source_decay_file.write("some lines 5\n")
    source_decay_file.write("some lines 6\n")
    source_decay_file.write("Enddecay\n")
    source_decay_file.write("some lines at end\n")
    source_decay_file.write("Decay D*+\n")
    source_decay_file.write("0.6770    D0  pi+ VSS;\n")
    source_decay_file.write("0.3070    D+  pi0 VSS;\n")
    source_decay_file.write("0.0160    D+  gamma VSP_PWAVE;\n")
    source_decay_file.write("Enddecay\n")
    source_decay_file.write("last line of the file")
    source_decay_file.close()

    reference_file=open('reference_file.tmp','w')
    reference_file.writelines(["=============\n",
"| D*(2007)0 |\n",
"=============\n",
"I(JP) = 1/2(1-)   I, J, P need confirmation.\n", 
"         Mass m = 2006.98+-0.15 MeV\n",
"         mass(D*0) - mass(D0) = 142.12+-0.07 MeV\n",
         "Full width Gamma < 2.1 MeV, CL = 90%\n",
" \n",
"      Dbar*(2007)0 modes are charge conjugates of modes below.\n",
"D*(2007)0 DECAY MODES                   Fraction (G(i)/G)           p (MeV/c)\n",
"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n",
 
"D0 pi0                                  (61.9+-2.9)%                       43\n",
"D0 gamma                                (38.1+-2.9)%                      137\n",
" \n",
"=============================================================================\n",
"==============\n",
"| D*(2010)+- |\n",
"==============\n",
"I(JP) = 1/2(1-)   I, J, P need confirmation.\n",
"         Mass m = 2010.28+-0.13 MeV\n",
"         mass(D*(2010)+) - mass(D+) = 140.66+-0.10 MeV(S = 1.1)\n",
"         mass(D*(2010)+) - mass(D0) = 145.421+-0.010 MeV(S = 1.1)\n",
"         Full width Gamma = 96+-22 keV\n",
" \n",
"      D*(2010)- modes are charge conjugates of the modes below.\n",
"D*(2010)+- DECAY MODES                  Fraction (G(i)/G)           p (MeV/c)\n",
"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n",
" \n",
"D0 pi+                                  (67.7+-0.5)%                       39\n",
"D+ pi0                                  (30.7+-0.5)%                       38\n",
"D+ gamma                                ( 1.6+-0.4)%                      136\n",
" \n",
"=============================================================================\n",
"================\n",
"| D(0)*(2400)0 |\n",
"================\n",
"I(JP) = 1/2(0+)\n",
"         Mass m = 2318+-29 MeV(S = 1.7)\n",
"         Full width Gamma = 267+-40 MeV\n",
" \n",
"D(0)*(2400)0 DECAY MODES                Fraction (G(i)/G)           p (MeV/c)\n",
"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n",
" \n",
"D+ pi-                                  seen                              385\n",
" \n",
"============================================================================="])
    reference_file.close()

    @request.addfinalizer
    def tearDown():
        print "TEAR DOWN!"
        os.remove("source_decay_file.dec.tmp")
        if os.path.isfile("workfile.tmp"):
            os.remove("workfile.tmp")
        os.remove('reference_file.tmp')


def test_successfully_extracting_decay(fixture_source):
    assert blub('source_decay_file.dec.tmp', "B0") == 0
    workfile=open("workfile.tmp",'r')
    for i, line in enumerate(workfile):
        if i == 0:
            assert line == 'Decay B0\n'
        elif i == 7:
            assert line == 'Enddecay\n'
        elif i > 7:
            break


def test_decay_not_found(fixture_source):
    with pytest.raises(SystemExit) as cm:
        blub('source_decay_file.dec.tmp', "B+")
    ex = cm.value
    assert ex.code == os.EX_DATAERR # SystemExit should be os.EX_DATAERR!
    assert not os.path.isfile("workdir.tmp") # workdir.tmp has been created even so it shouldn't have been


def test_decayfile_not_found(fixture_source):
    with pytest.raises(SystemExit) as cm:
        blub('Xsource_decay_file.dec.tmp', "B0")
    ex = cm.value
    assert ex.code == os.EX_IOERR # SystemExit should be os.EX_IOERR!
    assert not os.path.isfile("workdir.tmp") # workdir.tmp has been created even so it shouldn't have been


def test_particle_name_incomplete(fixture_source):
    with pytest.raises(SystemExit) as cm:
        blub('source_decay_file.dec.tmp', "B")
    ex = cm.value
    assert ex.code == os.EX_DATAERR # SystemExit should be os.EX_DATAERR!
    assert not os.path.isfile("workdir.tmp") # workdir.tmp has been created even so it shouldn't have been

def test_extract_decays_from_reference(fixture_source):
    extract_decays_from_reference('reference_file.tmp','D*(2010)+-')
    reference_file = open('workreffile.tmp','r')
    reference_file_lines = reference_file.readlines()
    assert reference_file_lines[0] == 'Decay D*+-\n'
    assert reference_file_lines[1] == '0.677 0.005 0.005 D0 pi+\n'
    assert reference_file_lines[2] == '0.307 0.005 0.005 D+ pi0\n'
    assert reference_file_lines[3] == '0.016 0.004 0.004 D+ gamma\n'
    assert reference_file_lines[4] == 'Enddecay\n'
    os.remove("workreffile.tmp")


# see D+
def test_extract_decays_from_reference_missing_blank_line():
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
    extract_decays_from_reference('reference_file.tmp','D+')
    work_ref_file = open('workreffile.tmp','r')
    work_ref_file_lines = work_ref_file.readlines()
    assert work_ref_file_lines[0] == 'Decay D+\n'
    assert work_ref_file_lines[1] == "0.00022 5e-05 5e-05 eta'(958) e+ nu_e\n"
    assert work_ref_file_lines[2] == "9e-05 0.0 0.0 phi e+ nu_e\n"
    assert work_ref_file_lines[3] == "0.0552 0.0015 0.0015 Kbar*(892)0 e+ nu_e\n"
    assert work_ref_file_lines[4] == "Enddecay\n"


if __name__ == '__main__':
    pytest.main()
