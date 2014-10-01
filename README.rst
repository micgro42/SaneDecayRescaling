==================
SaneDecayRescaling
==================

small python program to rescale decays from an EvtGen-like DECAY.DEC-file within in the error provided by reference data from the particle data group


planned funcionality
--------------------

1. extract the decays of a particle from an EvtGen Decay.Dec file (and optionally also it's anti-particle)
2. compare it to some reference from pdg and warn with the branching fractions deviate more than the 1-sigma error from pdg
3. change a branching fraction and rescale the rest so that the sum remains 1
4. check that none of the branching fractions rescaled in step 3 has been changed more than its error. (i.e. repeat step 2 for the file created in step 3)
5. redo steps 3 and 4 for some or all decays for that particle, these subsets can be

   I. a certain class of decays, for example semi-leptonic decays
   II. the X decays with the highest branching fraction
    
6. create an appropiate directory-structure and put every file created in step 5 into its own directory

development resources
---------------------

current result of the tests at travis-ci:

.. image:: https://travis-ci.org/micgro42/SaneDecayRescaling.svg
   :align: center
   :target: https://travis-ci.org/micgro42/SaneDecayRescaling


.. image:: https://coveralls.io/repos/micgro42/SaneDecayRescaling/badge.png
  :target: https://coveralls.io/r/micgro42/SaneDecayRescaling
  :align: center


.. image:: https://readthedocs.org/projects/sanedecayrescaling/badge/?version=latest
:target: https://readthedocs.org/projects/sanedecayrescaling/?badge=latest
:alt: Documentation Status
:align: center

see also: http://evtgen.warwick.ac.uk/
