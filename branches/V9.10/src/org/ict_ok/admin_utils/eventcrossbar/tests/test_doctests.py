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
from zope.schema import vocabulary

# ict_ok.org imports


def AllEventInstancesVocabulary(obj):
    return vocabulary.SimpleVocabulary([])

def setUpAllEventInstancesVocabulary(test):
    vr = vocabulary.getVocabularyRegistry()
    vr.register('AllEventInstances', AllEventInstancesVocabulary)

def setUp(test):
    pass

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite("eventcrossbar.txt",
                             package = "org.ict_ok.admin_utils.eventcrossbar",
                             setUp=setUp
                             ) 
    ))
