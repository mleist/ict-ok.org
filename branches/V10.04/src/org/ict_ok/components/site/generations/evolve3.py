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
from BTrees.OOBTree import OOBTree
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.site.interfaces import ISite

generation = 3

def evolve(context):
    u"""
    site with OOBTree for items data
    """
    root = getRootFolder(context) # the Zope-Root-Folders

    for site in findObjectsProviding(root, ISite):
        # convert this object
        if not hasattr(site, 'data'):
            evolve_msg = "gen. %d (%s)" % \
                       (generation, evolve.__doc__.strip())
            print u"Site(%s): " % site.ikName + evolve_msg
            site.data=site._SampleContainer__data
            site.appendHistoryEntry(evolve_msg)
