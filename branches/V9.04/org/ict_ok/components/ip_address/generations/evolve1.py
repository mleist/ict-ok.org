# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: evolve1.py 394 2009-01-06 15:12:30Z markusleist $
#
"""What to do when upgrade IpAddress from gen 0 to gen 1"""

__version__ = "$Id: evolve1.py 394 2009-01-06 15:12:30Z markusleist $"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.ip_address.interfaces import IIpAddress

generation = 1

def evolve(context):
    u"""
    convert object to new standard
    """
    
    root = getRootFolder(context) # the Zope-Root-Folders

    for ikobj in findObjectsProviding(root, IIpAddress):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "IpAddress(%s): " % ikobj.ikName + evolve_msg
        ikobj.appendHistoryEntry(evolve_msg)
