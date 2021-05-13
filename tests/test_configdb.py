"""
Sanity check of configdb key definitions

Does a simple comparison between the active ubxtypes_configdb key definitions and a
baselined copy to check for inadvertant corruption.

Created on 19 Apr 2021 

@author: semuadmin
"""

import unittest

from pyubx2.ubxtypes_configdb import UBX_CONFIG_DATABASE
from tests.configdb_baseline import UBX_CONFIG_DATABASE_BASELINE


class ConfigTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def testConfigDB(self):  # sanity check against baselined configdb definitions
        for (keyname, keytuple) in UBX_CONFIG_DATABASE.items():
            keyid, _ = keytuple
            try:
                keytuple2 = UBX_CONFIG_DATABASE_BASELINE[keyname]
                keyid2, _ = keytuple2
                self.assertEqual(keyid, keyid2)
            except KeyError:
                pass  # ignore any keys added since baseline


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
