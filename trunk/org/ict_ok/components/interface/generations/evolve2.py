# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade Interface from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.interface.interfaces import IInterface

generation = 2

def evolve(context):
    u"""
    convert interface object: ipv4 now is a list
    """
    
    root = getRootFolder(context) # the Zope-Root-Folders

    for ikinterface in findObjectsProviding(root, IInterface):
        # convert this object
        if not type(ikinterface.ipv4List) is type(list()):
            ikinterface.ipv4List = [ikinterface.ipv4List]
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "Interface(%s): " % ikinterface.ikName + evolve_msg
        ikinterface.appendHistoryEntry(evolve_msg)
