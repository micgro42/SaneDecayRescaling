from nose.tools import ok_, assert_raises
import os
from sanedecayrescaling.extract_decays import extract_decays as blub
from pytest import fixture

@fixture  # Registering this function as a fixture.
def fixture_source(request):
    print "start setup"
    SourceDecayFile=open('SourceDecayFile.dec.tmp','w')
    SourceDecayFile.write("some lines at start\n")
    SourceDecayFile.write("Decay B0\n")
    SourceDecayFile.write("some lines 1\n")
    SourceDecayFile.write("some lines 2\n")
    SourceDecayFile.write("some lines 3\n")
    SourceDecayFile.write("some lines 4\n")
    SourceDecayFile.write("some lines 5\n")
    SourceDecayFile.write("some lines 6\n")
    SourceDecayFile.write("Enddecay\n")
    SourceDecayFile.write("some lines at end\n")
    SourceDecayFile.write("last line of the file")
    SourceDecayFile.close()

    @request.addfinalizer
    def tearDown():
        print "TEAR DOWN!"
        os.remove("SourceDecayFile.dec.tmp")
        if os.path.isfile("workfile.tmp"):
            os.remove("workfile.tmp")

def test_successfully_extracting_decay(fixture_source):
    assert blub('SourceDecayFile.dec.tmp', "B0") == 0
    workfile=open("workfile.tmp",'r')
    for i, line in enumerate(workfile):
        if i == 0:
            assert line == 'Decay B0\n'
        elif i == 7:
            assert line == 'Enddecay\n'
        elif i > 7:
            break


def test_decay_not_found(fixture_source):
    with assert_raises(SystemExit) as cm:
        blub('SourceDecayFile.dec.tmp', "B+")
    ex = cm.exception
    ok_(ex.code == os.EX_DATAERR, 'SystemExit should be os.EX_DATAERR!')
    ok_(not os.path.isfile("workdir.tmp"), "workdir.tmp has been created even so it shouldn't have been")


def test_decayfile_not_found(fixture_source):
    with assert_raises(SystemExit) as cm:
        blub('XSourceDecayFile.dec.tmp', "B0")
    ex = cm.exception
    ok_(ex.code == os.EX_IOERR, 'SystemExit should be os.EX_IOERR!')
    ok_(not os.path.isfile("workdir.tmp"), "workdir.tmp has been created even so it shouldn't have been")


def test_particle_name_incomplete(fixture_source):
    with assert_raises(SystemExit) as cm:
        blub('SourceDecayFile.dec.tmp', "B")
    ex = cm.exception
    ok_(ex.code == os.EX_DATAERR, 'SystemExit should be os.EX_DATAERR!')
    ok_(not os.path.isfile("workdir.tmp"), "workdir.tmp has been created even so it shouldn't have been")



if __name__ == '__main__':
    pytest.main()
