# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: test_doctests.py 394 2009-01-06 15:12:30Z markusleist $
#
# pylint: disable-msg=W0221
#

__version__ = "$Id: test_doctests.py 394 2009-01-06 15:12:30Z markusleist $"

# python imports
import unittest

# zope imports
from zope.testing import doctest

# ict_ok.org imports
from org.ict_ok.admin_utils.eventcrossbar.tests.test_doctests import \
     setUpAllEventInstancesVocabulary

def setUp(test):
    setUpAllEventInstancesVocabulary(test)

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite("interface.txt",
                             package = "org.ict_ok.components.interface",
                             setUp=setUp
                             ) #,
        ))
