# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0602
#
"""supervisor object

the supervisor object will manage all starts of ICT_Ok and
will notice special events in an event-history

"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.util_manager.interfaces import IUtilManager


class UtilManager(Supernode):
    """Supervisor instance
    """
    implements(IUtilManager)
