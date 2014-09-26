from pytest import fixture
import pytest
from sanedecayrescaling import utility
import os

@fixture  # Registering this function as a fixture.
def fixture_testfile(request):
    print "start setup"
    source_decay_file=open('testfile.tmp','w')
    source_decay_file.write("a line at start\n")
    source_decay_file.close()

    @request.addfinalizer
    def tearDown():
        print "teardown"
        if os.path.isfile("testfile.tmp"):
            os.remove("testfile.tmp")


def test_open_safely_ok_read(fixture_testfile):
    read_only_file = utility.open_file_safely(
                    'testfile.tmp', 'r')
    with pytest.raises(IOError):
        read_only_file.write('foo')

def test_open_safely_ok_write(fixture_testfile):
    writeable_file = utility.open_file_safely(
                    'testfile.tmp', 'w')
    writeable_file.write('foo')
    writeable_file.close()

def test_open_safely_file_not_found(fixture_testfile):
    with pytest.raises(SystemExit) as cm:
        utility.open_file_safely('foo.tmp','r')
    ex = cm.value
    assert ex.code == os.EX_IOERR # SystemExit should be os.EX_IOERR!