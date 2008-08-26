# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0221,W0212
#

__version__ = "$Id$"

# python imports
import unittest

# zope imports
from zope.interface.verify import verifyObject

# ict_ok.org imports
from org.ict_ok.admin_utils.graphviz.interfaces import IAdmUtilGraphviz

class TestIAdmUtilGraphviz(unittest.TestCase):
    """Test the IAdmUtilGraphviz interface""" 

    def makeTestObject(self):
        """Returns an IAdmUtilGraphviz instance"""
        raise NotImplemented()

    def test_verifyInterfaceImplementation(self):
        self.assert_(verifyObject(IAdmUtilGraphviz, self.makeTestObject())) 

def test_suite():
    suite = unittest.TestSuite()
    return suite

if __name__ == '__main__':
    unittest.main()
