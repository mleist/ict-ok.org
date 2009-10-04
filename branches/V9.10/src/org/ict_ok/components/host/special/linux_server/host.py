# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of host object

host object represents a Linux Server
"""

__version__ = "$Id$"

# python imports

# zope imports

# ict_ok.org imports
from org.ict_ok.components.host.host import Host as HostBase


class Host(HostBase):
    pass
