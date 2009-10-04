# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade Site from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.site.interfaces import ISite

generation = 2

def evolve(context):
    u"""
    site with inward relaying shutdown events
    """
    root = getRootFolder(context) # the Zope-Root-Folders

    for site in findObjectsProviding(root, ISite):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "Site(%s): " % site.ikName + evolve_msg
        site.eventInpObjs_inward_relaying_shutdown = set([])
        site.appendHistoryEntry(evolve_msg)
