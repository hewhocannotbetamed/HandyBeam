## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam directory

sys.path.append('../.')

## Class

class ClSystemTests(unittest.TestCase):

    def setUp(self):

        self.cl_system = None


    def tearDown(self):

        del self.cl_system 
    
    def test_import(self):

        module_name = 'handybeam.cl_system'

        import handybeam.cl_system

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

    def test_instance_creation(self):

        import handybeam.cl_system

        self.cl_system  = handybeam.cl_system.OpenCLSystem()
                
        fail = True

        if isinstance(self.cl_system , handybeam.cl_system.OpenCLSystem):
            
            fail = False

        self.assertEqual(fail,False)


## Script 

if __name__ == '__main__':

    unittest.main()
