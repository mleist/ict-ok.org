# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of host object"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import TextLine, Set, Choice

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IEventIfEventHost
from org.ict_ok.components.host.interfaces import IHost

_ = MessageFactory('org.ict_ok')


class IHostVMwareEsx(IHost):
    """A host object."""
    # TODO move to own Interface towards admin_util.esx...
    esxUuid = TextLine(
        max_length = 80,
        title = _("ESX UUID"),
        description = _("UUID of virtual machine in ESX."),
        default = u"",
        required = False)

    def shutdownHost(self):
        """
        trigger shutdownHost
        """
    def enterMaintenanceMode(self):
        """
        trigger enterMaintenanceMode
        """


class IEventIfHostVMwareEsx(IEventIfEventHost):
    """ event interface of object """
    eventInpObjs_inward_relaying_shutdown = Set(
        title = _("inward relaying shutdown <-"),
        value_type = Choice(
            title = _("objects"),
            vocabulary="AllEventInstances"),
        default = set([]),
        readonly = False,
        required = True)
    
    def eventInp_inward_relaying_shutdown(eventMsg):
        """
        forward the event to all objects in this container through the signal filter
        """
