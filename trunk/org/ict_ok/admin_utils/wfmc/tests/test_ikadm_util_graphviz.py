# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0221,W0212
#

__version__ = "$Id$"

# phython imports
import unittest

# zope imports

# ict_ok.org imports
from org.ict_ok.admin_utils.graphviz.tests.test_iikadm_util_graphviz \
     import TestIAdmUtilGraphviz
from org.ict_ok.admin_utils.graphviz.graphviz import AdmUtilGraphviz


class TestAdmUtilGraphviz(TestIAdmUtilGraphviz):
    """Test the AdmUtilGraphviz implementation""" 

    def makeTestObject(self):
        return AdmUtilGraphviz()

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestAdmUtilGraphviz))
    return suite

if __name__ == '__main__':
    unittest.main()
