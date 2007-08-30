# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade Net from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.net.interfaces import INet

generation = 1

def evolve(context):
    u"""
    convert ddd to new format
    """
    
    root = getRootFolder(context) # the Zope-Root-Folders

    for net in findObjectsProviding(root, INet):
        # convert this object
        pass
