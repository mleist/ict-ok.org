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
from zope.testing import doctest

# ict_ok.org imports

def test_suite():
    return unittest.TestSuite((
        #doctest.DocFileSuite("locking.txt", package = "z3c.dav",
                             #checker = z3c.etree.testing.xmlOutputChecker,
                             #setUp = z3c.etree.testing.etreeSetup,
                             #tearDown = z3c.etree.testing.etreeTearDown),
        doctest.DocFileSuite("superclass.txt",
                             package = "org.ict_ok.components.superclass") #,
                             #checker = z3c.etree.testing.xmlOutputChecker,
                             #setUp = z3c.etree.testing.etreeSetup,
                             #tearDown = z3c.etree.testing.etreeTearDown),
        ))
