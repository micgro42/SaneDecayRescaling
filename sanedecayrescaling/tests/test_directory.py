import os
import sys
import shutil
from pytest import fixture
import sanedecayrescaling.utility as utility


@fixture  # Registering this function as a fixture.
def fixture_dir(request):
    base_dir = os.getcwd()
    work_dir = base_dir + '/TEST_TEMP'
    if not os.path.exists(work_dir):
        os.mkdir(work_dir)
    else:
        print 'TEST_TEMP already exists in ', base_dir, ' please remove'
        sys.exit()
    
    
    @request.addfinalizer
    def tearDown():
        os.chdir(base_dir)
        if os.path.exists(work_dir):
            shutil.rmtree(work_dir)



def test_create_dirs(fixture_dir):
    os.chdir('TEST_TEMP')
    work_dir = os.getcwd()
    utility.create_dirs(123,work_dir + '/mc')
    for i in range(0,9):
        assert os.path.isdir(work_dir + '/mc/00' + str(i))

    for i in range(10,99):
        assert os.path.isdir(work_dir + '/mc/0' + str(i))

    for i in range(100,122):
        assert os.path.isdir(work_dir + '/mc/' + str(i))