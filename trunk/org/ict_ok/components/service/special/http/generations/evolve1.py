# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <->
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""upgrade to initial version 1 of Service Http"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.service.special.http.interfaces import \
    IServiceHttp

generation = 1

def evolve(context):
    u"""
    convert object to new standard
    """
    root = getRootFolder(context) # the Zope-Root-Folders

    for service in findObjectsProviding(root, IServiceHttp):
        evolve_msg = "gen. %d (%s)" % \
            (generation, evolve.__doc__.strip())
        print "Service(%s): " % service.ikName + evolve_msg
        service.appendHistoryEntry(evolve_msg)
