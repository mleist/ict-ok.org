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
from zope.schema import vocabulary

# ict_ok.org imports
from org.ict_ok.components.latency.latency import Latency

class GeneralTestCase(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        self.testobj = Latency()
        super(GeneralTestCase, self).setUp()

    def test_initial_values(self):
        pass


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GeneralTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
