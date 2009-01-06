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

generation = 3

def evolve(context):
    u"""
    event stores dynamic host group
    """
    convertDict = {
        u'dns': u'DNS-Server',
        u'file': u'File-Server',
        u'misc': u'Miscellaneous-Server',
        u'smtp': u'SMTP-Server',
        u'terminal': u'Terminal-Server',
        u'util': u'Utility-Server',
        u'workstation': u'Workstation',
    }

    root = getRootFolder(context) # the Zope-Root-Folders
    sitemanager = root.getSiteManager()
    default = sitemanager['default']
    eventUtil = default[u'AdmUtilEventCrossbar']

    for obj in findObjectsProviding(eventUtil, IAdmUtilEvent):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        if convertDict.has_key(event.hostGroup):
            event.hostGroup = None
            event._p_changed = True
        print "Object(%s): " % obj.ikName + evolve_msg
        obj.appendHistoryEntry(evolve_msg)
