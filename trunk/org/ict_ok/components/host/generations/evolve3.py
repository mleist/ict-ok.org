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
from org.ict_ok.components.host.interfaces import IHost

generation = 3

def evolve(context):
    u"""
    host stores dynamic host groups
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
    import pdb
    pdb.set_trace()

    for host in findObjectsProviding(root, IHost):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "Host(%s): " % host.ikName + evolve_msg
        toDelete = []
        for oldHostGroup in host.hostGroups:
            if convertDict.has_key(oldHostGroup):
                print "delete host group ", oldHostGroup
                toDelete.append(oldHostGroup)
        for i_index in toDelete:
            host.hostGroups.remove(i_index)
        host._p_changed = True
        host.appendHistoryEntry(evolve_msg)
