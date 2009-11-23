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
from logging import NOTSET

# zope imports
from zope.app.testing.placelesssetup import PlacelessSetup

# ict_ok.org imports
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.libs.lib import oidIsValid


class SuperclassGeneralTestCase(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        self.testobj = Superclass()
        super(SuperclassGeneralTestCase, self).setUp()

    def test_initial_values(self):
        #self.assertEqual(self.testobj.ikName, ...)
        self.assertEqual(self.testobj.dbgLevel, NOTSET)
        self.assertEqual(self.testobj.ikComment, u"")
        self.assertEqual(self.testobj.ikAuthor, u"")
        self.assertEqual(self.testobj.ikNotes, None)
        #self.assertEqual(self.testobj.history, [])

    def test_ObjectId(self):
        oid = self.testobj.getObjectId()
        self.assertTrue(oidIsValid(oid))
        
    #def test_DcTitle(self):
        #self.testobj.setDcTitle(u"testtitle")
        #self.assertEqual(self.testobj.getDcTitle(), u"testtitle2")



#    def test_set_title(self):
#        self.testobj.title = u"empty"
#        self.assertEqual(self.testobj.title, u"empty")
#
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SuperclassGeneralTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
