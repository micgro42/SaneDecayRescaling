import os
from sanedecayrescaling import check_sanity as cs
from pytest import fixture
import pytest
import sanedecayrescaling.utility as utility


#
# to be tested:
# open_file_safely:
# file found and successfully opened
# file not Found
# file soft link to valid file
# file is fifo pipe 
# test that a file, which is open for reading only can indeed not be written
# test that a file, which is open for writing can indeed be written

# find_decay_in_reference
# find a decay and return branching ratio and branching ratio error
# decay is sorted (not) correctly
# do not find a decay and return -1, -1

# check sanity:
# Path to decay-file falsch
# Path to reference-file falsch
# generators file does not exists
# everything is ok, no deviation
# deviation larger than 1 sigma
# deviation smaller than 1 sigma
# decay not found




@fixture  # Registering this function as a fixture.
def fixture_source_reference(request):
    print "start setup"
    source_decay_file=open('source_decay_file.dec.tmp','w')
    source_decay_file.write("some lines at start\n")
    source_decay_file.write("Decay D*+\n")
    source_decay_file.write("0.6770    D0  pi+ VSS;\n")
    source_decay_file.write("0.3070    D+  pi0 VSS;\n")
    source_decay_file.write("0.0160    D+  gamma VSP_PWAVE;\n")
    source_decay_file.write("Enddecay\n")
    source_decay_file.write("some lines at end\n")
    source_decay_file.write("last line of the file")
    source_decay_file.close()

    reference_file=open('reference.dec.tmp','w')
    reference_file.writelines(["Decay D*+\n",
                              "0.6770 0.005 D0 pi+\n",
                              "0.0160 0.004 D+ gamma\n",
                              "0.3070 0.005 pi0 D+\n",
                              "Enddecay\n","\n"])
    reference_file.close()

    @request.addfinalizer
    def tearDown():
        if os.path.isfile("workfile.tmp"):
            os.remove("workfile.tmp")
        if os.path.isfile("source_decay_file.dec.tmp"):
            os.remove("source_decay_file.dec.tmp")
        if os.path.isfile("reference.dec.tmp"):
            os.remove("reference.dec.tmp")



def test_find_decay_found(fixture_source_reference):
    reference_file = open('reference.dec.tmp')
    decay_list = ["pi+", "D0"]
    branching_ratio, branching_ratio_error = cs.find_decay_in_reference (
                                            reference_file,decay_list)
    assert branching_ratio == 0.6770 # should be the value from the decay file
    assert branching_ratio_error == 0.005 # "should be the value from the decay file")

def test_find_decay_not_found(fixture_source_reference):
    reference_file = open('reference.dec.tmp')
    decay_list = ["pi+", "D+"]
    branching_ratio, branching_ratio_error = cs.find_decay_in_reference (
                                            reference_file,decay_list)
    assert branching_ratio == -1 # should be -1 if decay not found
    assert branching_ratio_error == -1 # should be -1 if decay not found


def test_check_sanity_ok(fixture_source_reference):
    cs.check_sanity('source_decay_file.dec.tmp','reference.dec.tmp','D*+')

if __name__ == '__main__':
    pytest.main()