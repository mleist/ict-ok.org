# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0221
#

__version__ = "$Id$"

# python imports
import unittest

# zope imports
from zope.app.testing.placelesssetup import PlacelessSetup

# ict_ok imports
from org.ict_ok.components.slave.slave import Slave


class SlaveXxxTestCase(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        self.testobj = Slave()
        super(SlaveXxxTestCase, self).setUp()

    def test_initial_values(self):
        self.assertEqual(self.testobj.title, u"Title")

    def test_set_title(self):
        self.testobj.title = u"empty"
        self.assertEqual(self.testobj.title, u"empty")

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SlaveXxxTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
