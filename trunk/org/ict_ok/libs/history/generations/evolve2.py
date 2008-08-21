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
from org.ict_ok.components.superclass.interfaces import ISuperclass

generation = 2

def evolve(context):
    u"""
    convert this all history-entries, additional 'repeated data'
    """
    root = getRootFolder(context) # the Zope-Root-Folders
    sm = root.getSiteManager()
    # convert this all history-entries
    for obj in findObjectsProviding(root, ISuperclass):
        for historyEntry in obj.history.get():
            try:
                tmp = historyEntry._repeated
            except AttributeError:
                historyEntry._repeated = None
    for utility in sm.registeredUtilities():
        if hasattr(utility.component, "history"):
            for historyEntry in utility.component.history.get():
                try:
                    tmp = historyEntry._repeated
                except AttributeError:
                    historyEntry._repeated = None
