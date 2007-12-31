# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of host object"""

__version__ = "$Id$"

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.schema import TextLine

# ict_ok.org imports
from org.ict_ok.components.supernode.interfaces import \
     IEventIfSupernode
from org.ict_ok.components.host.interfaces import IHost

_ = MessageFactory('org.ict_ok')


class IHostVMwareVm(IHost):
    """A host object."""
    # TODO move to own Interface towards admin_util.esx...
    esxUuid = TextLine(
        max_length = 80,
        title = _("ESX UUID"),
        description = _("UUID of virtual machine in ESX."),
        default = u"",
        required = False)
    
    def poweroff():
        """
        trigger poweroff
        """
    def poweron():
        """
        trigger poweron
        """

class IEventIfHostVMwareVm(IEventIfSupernode):
    """ event interface of object """
