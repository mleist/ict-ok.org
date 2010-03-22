# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade IpNet from gen 2 to gen 3
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.ipnet.interfaces import IIpNet

generation = 3

def evolve(context):
    u"""
    net object now with shortName ipnet
    """
    root = getRootFolder(context) # the Zope-Root-Folders

    for net in findObjectsProviding(root, IIpNet):
        # convert this object
        evolve_msg = u"gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print u"IpNet(%s): " % net.ikName + evolve_msg
        net.shortName = "ipnet"
        net.appendHistoryEntry(evolve_msg)
