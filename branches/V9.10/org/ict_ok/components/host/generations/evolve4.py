# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade Host from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost

generation = 4

def evolve(context):
    u"""
    host object with snmp settings (version, port, community-strings)
    """
    
    root = getRootFolder(context) # the Zope-Root-Folders

    for host in findObjectsProviding(root, IHost):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "Host(%s): " % host.ikName + evolve_msg
        host.snmpVersion = 1
        host.snmpPort = 161
        host.snmpReadCommunity = u'public'
        host.snmpWriteCommunity = u'private'
        host.appendHistoryEntry(evolve_msg)
