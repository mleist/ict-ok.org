# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""What to do when upgrade ikslave from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok imports
from org.ict_ok.components.slave.interfaces import ISlave

generation = 1

def evolve(context):
    u"""
    new ikdate1
    """ # Dieser Doc-String wird später im ZMI angezeigt.
    
    root = getRootFolder(context) # Ermitteln des Zope-Root-Folders

    for ikslave in findObjectsProviding(root, ISlave):
        # Schleife über alle Objekte, die IPerson erfüllen.
        ikslave.ikdate1 = None # Setzen des Defaults
