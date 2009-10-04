# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: evolve1.py_cog 506 2009-04-30 14:24:56Z markusleist $
#
"""What to do when upgrade InternalAttachment from gen 0 to gen 1"""

__version__ = "$Id: evolve1.py_cog 506 2009-04-30 14:24:56Z markusleist $"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.int_attachment.interfaces import IInternalAttachment

generation = 1

def evolve(context):
    u"""
    convert object to new standard
    """
    
    root = getRootFolder(context) # the Zope-Root-Folders

    for ikobj in findObjectsProviding(root, IInternalAttachment):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "InternalAttachment(%s): " % ikobj.ikName + evolve_msg
        ikobj.appendHistoryEntry(evolve_msg)
