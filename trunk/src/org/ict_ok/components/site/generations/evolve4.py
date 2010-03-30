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
from org.ict_ok.admin_utils.supervisor.bootstrap import \
    createUtils as createSupervisorUtils

generation = 4

def evolve(context):
    u"""
    site update with some bootstraps
    """
    root = getRootFolder(context) # the Zope-Root-Folders

    for site in findObjectsProviding(root, ISite):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print u"Site(%s): " % site.ikName + evolve_msg
        createSupervisorUtils(site)
        site.appendHistoryEntry(evolve_msg)
