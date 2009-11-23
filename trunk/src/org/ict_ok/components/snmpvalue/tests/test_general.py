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
from org.ict_ok.components.snmpvalue.snmpvalue import SnmpValue
from org.ict_ok.components.snmpvalue.tests import setUpSnmpCheckTypes

class GeneralTestCase(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        setUpSnmpCheckTypes(self)
        self.testobj = SnmpValue()
        super(GeneralTestCase, self).setUp()

    def test_initial_values(self):
        pass
        #self.assertEqual(self.testobj.checktype, u"oid")
        #self.assertEqual(self.testobj.oid1, u"1.3.6.1.2.1.1.1.0")
        #self.assertEqual(self.testobj.oid2, u"1.3.6.1.2.1.1.1.0")
        #self.assertEqual(self.testobj.cmd, u"none")
        #self.assertEqual(self.testobj.inptype, u"cnt")
        #self.assertEqual(self.testobj.checkMax, False)
        #self.assertEqual(self.testobj.snmpIndexType, u"mac")
        #self.assertEqual(self.testobj.inpQuantity, u"8.0 bit")
        #self.assertEqual(self.testobj.displUnitAbs, u"b")
        #self.assertEqual(self.testobj.displUnitVelocity, None)
        #self.assertEqual(self.testobj.displUnitAcceleration, None)
        #self.assertEqual(self.testobj.maxQuantityAbs, None)
        #self.assertEqual(self.testobj.maxQuantityVelocity, None)
        #self.assertEqual(self.testobj.maxQuantityAcceleration, None)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(GeneralTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
