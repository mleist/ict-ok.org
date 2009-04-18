# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 467 2009-03-05 04:28:59Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of IpAddress"""


__version__ = "$Id: interfaces.py_cog 467 2009-03-05 04:28:59Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.schema.ipvalid import NetIpValid

_ = MessageFactory('org.ict_ok')


class IIpAddress(Interface):
    """A IpAddress object."""

    ipv4 = NetIpValid(
        title = _(u'IP Address'),
        description = _(u"IP address of the device."),
        required = True)
        

    interface = Choice(
        title = _(u'Interface'),
        vocabulary = 'AllInterfaces',
        required = False)
        
    ipNet = Choice(
        title = _(u'IP Net'),
        vocabulary = 'AllIpNets',
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IIpAddressFolder(Interface):
    """Container for IpAddress objects
    """


class IAddIpAddress(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllIpAddressTemplates",
        required = False)
