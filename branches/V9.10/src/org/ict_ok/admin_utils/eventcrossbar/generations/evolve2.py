# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade Interface from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.admin_utils.eventcrossbar.interfaces import IAdmUtilEvent

generation = 2

def evolve(context):
    u"""
    event stores one hostgroup (not set of groups)
    """
    root = getRootFolder(context) # the Zope-Root-Folders
    sitemanager = root.getSiteManager()
    default = sitemanager['default']
    eventUtil = default[u'AdmUtilEventCrossbar']

    for obj in findObjectsProviding(eventUtil, IAdmUtilEvent):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        if type(event.hostGroup) == type(set()):
            # old style
            if len(event.hostGroup) == 0:
                event.hostGroup = None
            elif len(event.hostGroup) == 1:
                event.hostGroup = list(event.hostGroup)[0]
            else:
                event.hostGroup = list(event.hostGroup)[0]
                evolve_msg += "**** Error: HostGroup was configured with more than one entry ****"
        print "Object(%s): " % obj.ikName + evolve_msg
        obj.appendHistoryEntry(evolve_msg)
