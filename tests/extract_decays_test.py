# -*- coding: utf-8 -*-
from nose.tools import *
import os
from SaneDecayRescaling.extract_decays import extract_decays as blub

class Testclass:

    def setUp(self):
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
    
    def tearDown(self):
        print "TEAR DOWN!"
        os.remove("SourceDecayFile.dec.tmp")
        if os.path.isfile("workfile.tmp"):
            os.remove("workfile.tmp")
        
    def test_successfully_extracting_decay(self):
        assert blub('SourceDecayFile.dec.tmp', "B0") == 0
        workfile=open("workfile.tmp",'r')
        for i, line in enumerate(workfile):
            if i == 0:
                assert line == 'Decay B0\n'
            elif i == 7:
                assert line == 'Enddecay\n'
            elif i > 7:
                break
    
    
    def test_decay_not_found(self):
        assert blub('SourceDecayFile.dec.tmp', "B+") == 1
        assert not os.path.isfile("workdir.tmp")
        
    def test_decayfile_not_found(self):
        assert blub('XSourceDecayFile.dec.tmp', "B0") == 404 
        assert not os.path.isfile("workdir.tmp")
    
    def test_particle_name_incomplete(self):
        assert blub('SourceDecayFile.dec.tmp', "B") == 1
        assert not os.path.isfile("workdir.tmp")
    
    
        
    
if __name__ == '__main__':
    unittest.main()
    