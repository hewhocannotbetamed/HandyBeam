## Imports

import os
import sys
import inspect
import unittest

# Include path to handybeam directory

sys.path.append('../.')

## Class

class TxArrayLibraryTests(unittest.TestCase):

    def setUp(self):

        pass

    def tearDown(self):

        pass
    
    def test_import(self):

        module_name = 'handybeam.tx_array_library'

        import handybeam.tx_array_library

        fail = False

        if module_name not in sys.modules:
            
            fail = True

        self.assertEqual(fail,False)

## Script 

if __name__ == '__main__':

    unittest.main()
