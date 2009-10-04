# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""configuration path to nagios now in nagios generator
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IAdmUtilGeneratorNagios

generation = 3


def evolve(context):
    u"""
    nagios utility now supports path information for nagios data
    """
    
    root = getRootFolder(context) # the Zope-Root-Folders

    for obj in findObjectsProviding(root, IAdmUtilGeneratorNagios):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        obj.pathConfigData = u"/opt/nagios/etc/ict_ok"
        print "Object(%s): " % obj.ikName + evolve_msg
        obj.appendHistoryEntry(evolve_msg)
