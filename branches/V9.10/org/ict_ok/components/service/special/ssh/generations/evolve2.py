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
from org.ict_ok.components.service.special.ssh.interfaces import \
     IServiceSsh

generation = 2

def evolve(context):
    u"""
    ssh service object now supports port number
    """
    root = getRootFolder(context) # the Zope-Root-Folders
    for service in findObjectsProviding(root, IServiceSsh):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "Service(%s): " % service.ikName + evolve_msg
        # todo ....
        service.appendHistoryEntry(evolve_msg)
