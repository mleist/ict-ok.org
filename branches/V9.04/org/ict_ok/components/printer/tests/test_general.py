# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: test_general.py 467 2009-03-05 04:28:59Z markusleist $
#
# pylint: disable-msg=W0221
#

__version__ = "$Id: test_general.py 467 2009-03-05 04:28:59Z markusleist $"

# python imports
import unittest

# zope imports
from zope.app.testing.placelesssetup import PlacelessSetup

# ict_ok.org imports
from org.ict_ok.components.interface.interface import Interface


class GeneralTestCase(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        self.testobj = Interface()
        super(GeneralTestCase, self).setUp()

    def test_initial_values(self):
        self.assertEqual(self.testobj.netType, "ethernet")
        self.assertEqual(self.testobj.mac, u"00:00:00:00:00:00")
        self.assertEqual(self.testobj.ipv4List, [])

    def test_ipv4List(self):
        self.assertEqual(self.testobj.ipv4List, [])
        self.testobj.ipv4List.append(u"172.16.1.1")
        self.assertEqual(self.testobj.ipv4List, [u"172.16.1.1"])

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GeneralTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
