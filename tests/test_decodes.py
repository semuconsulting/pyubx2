"""
test pyubx2.ubxtypes_enums.py

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

@author: semuadmin
"""

import os
import unittest

from pyubx2.ubxtypes_decodes import *


class StaticTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)

    def tearDown(self):
        pass

    def testenums(self):
        for enum in (
            DGNSMODE,
            CONFLVL,
            SIGCFMASK,
            PROTOCOLID,
            DYNMODEL,
            FIXMODE,
            NMEAVERSION,
            SVNUMBERING,
            MAINTALKERID,
            GSVTALKERID,
            ODOPROFILE,
            CHARLEN,
            PARITY,
            NSTOPBITS,
            POL,
            SPIMODE,
            STATE,
            TIMEREF,
            NAVBBRMASK,
            RESETMODE,
            MODE,
            GRIDUTCGNSS,
            PROTIDS,
            ASTATUS,
            APOWER,
            JAMMINGSTATE,
            BOOTTYPE,
            GEOFENCE_STATUS,
            COMBSTATE,
            HEALTH,
            VISIBILITY,
            PLPOSFRAME,
            PLVELFRAME,
            GPSFIX,
            FIXTYPE,
            PSMSTATE,
            CARRSOLN,
            QUALITYIND,
            ORBITSOURCE,
            SBASMODE,
            SBASSYS,
            SBASINTEGRITYUSED,
            CORRSOURCE,
            IONOMODEL,
            SIGID,
            SOURCEOFCURLS,
            SRCOFLSCHANGE,
            SPOOFDETSTATE,
            PSMSTATUS,
            UTCSTANDARD,
        ):
            for key, val in enum.items():
                # print(key, val)
                pass  # test is just for test completion stats


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
