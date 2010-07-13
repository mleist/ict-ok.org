# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
"""What to do when upgrade Notebook from gen 0 to gen 1"""

__version__ = "$Id$"

# zope imports
from zope.app.zopeappgenerations import getRootFolder
from zope.app.generations.utility import findObjectsProviding

# ict_ok.org imports
from org.ict_ok.components.device.interfaces import IDevice
from org.ict_ok.components.device.wf.nagios import pd as WfPdNagios

generation = 2

def evolve(context):
    u"""
    convert object to new standard
    """
    
    root = getRootFolder(context) # the Zope-Root-Folders

    for ikobj in findObjectsProviding(root, IDevice):
        # convert this object
        evolve_msg = "gen. %d (%s)" % \
                   (generation, evolve.__doc__.strip())
        ikobj.workflows[WfPdNagios.id] = nagios_wf = WfPdNagios()
        setattr(nagios_wf.workflowRelevantData, "state", "-")
        setattr(nagios_wf.workflowRelevantData, "object", ikobj)
        setattr(nagios_wf.workflowRelevantData, "new_state", "2_start")
        nagios_wf.start()
        ikobj.appendHistoryEntry(evolve_msg)
