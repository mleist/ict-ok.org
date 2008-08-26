# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 
#               Markus Leist <leist@ikom-online.de>
#               Sebastian Napiorkowski <->
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: service.py 73 2007-10-02 09:37:48Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Service Http"""

__version__ = "$Id: service.py 73 2007-10-02 09:37:48Z markusleist $"

# python imports

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.components.service.special.http.interfaces import \
    IServiceHttp
from org.ict_ok.components.service.service import Service as ServiceBase


class Service(ServiceBase):
    """
    the template instance
    """

    implements(IServiceHttp)
