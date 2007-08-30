# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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
from zope.testing import doctest

# ict_ok.org imports

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite("net.txt",
                             package = "org.ict_ok.components.net") #,
        ))
