# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of Notebook"""


__version__ = "$Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IDevice(Interface):
    """A device object."""

    cpuType = TextLine(
        title = _(u'CPU type'),
        description = _(u'Text of CPU type'),
        required = False)
        
    memsize = Int(
        title = _(u'Memory size (MB)'),
        description = _(u'Memory size in MB'),
        required = False)

    
    interfaces = List(title=_(u"Interface"),
                      value_type=Choice(vocabulary='AllUnusedOrUsedDeviceInterfaces'),
                      required=False,
                      default=[])
    
    osoftwares = List(title=_(u"Operating software"),
                      value_type=Choice(vocabulary='AllUnusedOrUsedDeviceOperatingSoftwares'),
                      required=False,
                      default=[])
    
    appsoftwares = List(title=_(u"Application software"),
                      value_type=Choice(vocabulary='AllUnusedOrUsedDeviceApplicationSoftwares'),
                      required=False,
                      default=[])


class IDeviceFolder(Interface):
    """Container for Notebook objects
    """
