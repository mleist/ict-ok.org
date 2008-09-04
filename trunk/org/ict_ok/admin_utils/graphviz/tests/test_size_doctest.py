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
from zope.testing.doctestunit import DocTestSuite

def test_suite():
    return unittest.TestSuite((DocTestSuite('org.ict_ok.admin_utils.graphviz.graphviz'),))

if __name__ == '__main__':
    unittest.main(defaultTest = 'test_suite')
