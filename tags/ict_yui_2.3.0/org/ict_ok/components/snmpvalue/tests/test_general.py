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

# phython imports
import unittest

# zope imports
from zope.app.testing.placelesssetup import PlacelessSetup

# ict_ok.org imports
from org.ict_ok.components.host.host import Host


class HostGeneralTestCase(PlacelessSetup, unittest.TestCase):

    def setUp(self):
        self.testobj = Host()
        super(HostGeneralTestCase, self).setUp()

    def test_initial_values(self):
        self.assertEqual(self.testobj.hostname, u'systemname')
        self.assertEqual(self.testobj.manufacturer, u"")
        self.assertEqual(self.testobj.vendor, u"")
        self.assertEqual(self.testobj.workinggroup, u"")
        self.assertEqual(self.testobj.hardware, u"")
        self.assertEqual(self.testobj.user, u"")
        self.assertEqual(self.testobj.inv_id, u"")
        self.assertEqual(self.testobj.building, u"")
        self.assertEqual(self.testobj.room, u"")
        self.assertEqual(self.testobj.osList, [])
        self.assertEqual(self.testobj.url, u"")
        self.assertEqual(self.testobj.url_type, "direct")
        self.assertEqual(self.testobj.url_authname, u"")
        self.assertEqual(self.testobj.url_authpasswd, u"")
        self.assertEqual(self.testobj.console, u"")
        self.assertEqual(self.testobj.genNagios, True)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(HostGeneralTestCase))
    return suite

if __name__ == '__main__':
    unittest.main()
