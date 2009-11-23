# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade Host from gen 1 to gen 2
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost

generation = 5

def evolve(context):
    u"""
    host object now with health state
    """
    
    root = getRootFolder(context) # the Zope-Root-Folders

    for host in findObjectsProviding(root, IHost):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "Host(%s): " % host.ikName + evolve_msg
        host._counter = {'r': 500}
        host._health = 1.0
        host._weight = {'r': 1.0}
        host._weight_user = 0.5
        host.appendHistoryEntry(evolve_msg)
