# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade Host from gen 0 to gen 1
"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.host.special.vmware_esx.interfaces import \
     IEventIfHostVMwareEsx

generation = 1
print "#5" * 40

def evolve(context):
    u"""
    convert object to new standard
    """
    print "#4" * 40

    root = getRootFolder(context) # the Zope-Root-Folders

    for host in findObjectsProviding(root, IEventIfHostVMwareEsx):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        print "Host(%s): " % host.ikName + evolve_msg
        host.appendHistoryEntry(evolve_msg)
