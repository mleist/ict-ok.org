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
from org.ict_ok.admin_utils.eventcrossbar.tests.test_doctests import \
     setUpAllEventInstancesVocabulary

def setUp(test):
    setUpAllEventInstancesVocabulary(test)

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite("snmpvalue.txt",
                             package = "org.ict_ok.components.snmpvalue",
                             setUp=setUp,
                             ) #,
        ))
