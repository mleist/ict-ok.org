# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#
"""implementation of 'logical' event objects
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements

# zc imports

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.eventcrossbar.interfaces import \
     IEventLogic, IEventIfEventLogic


class EventLogic(Supernode):
    """
    superclass for any kind of 'logical' event objects
    """
    implements(IEventLogic, IEventIfEventLogic)
    
    def __init__(self, **data):
        """
        constructor of 'logical' event objects
        """
        Supernode.__init__(self, **data)
        for (name, value) in data.items():
            if name in IEventLogic.names():
                setattr(self, name, value)
        self.ikRevision = __version__
