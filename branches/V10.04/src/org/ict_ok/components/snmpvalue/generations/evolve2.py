# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade SnmpValue from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.snmpvalue.interfaces import ISnmpValue

generation = 2

def evolve(context):
    u"""
    convert object with new input multiplier
    """

    root = getRootFolder(context) # the Zope-Root-Folders

    for iksnmpvalue in findObjectsProviding(root, ISnmpValue):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "SNMP Value(%s): " % iksnmpvalue.ikName + evolve_msg
        iksnmpvalue.inpMultiplier = 1.0
        iksnmpvalue.appendHistoryEntry(evolve_msg)
