# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade Service from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.service.interfaces import IService

generation = 1

def evolve(context):
    u"""
    convert object to new standard
    """
    
    root = getRootFolder(context) # the Zope-Root-Folders

    for ikservice in findObjectsProviding(root, IService):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "Service(%s): " % ikservice.ikName + evolve_msg
        ikservice.appendHistoryEntry(evolve_msg)
