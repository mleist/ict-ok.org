# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232
#
"""Interface of Site"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.schema import Bool, TextLine, Set, Choice
from zope.i18nmessageid import MessageFactory
from zope.app.container.constraints import contains

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class ISite(Interface):
    """
    The interface of Site-objects
    """
    contains('org.ict_ok.components.site.interfaces.ISite')

    sitename = TextLine(
        max_length = 80,
        title = _("Sitename"),
        description = _("Name of the site."),
        default = _("mysite"),
        required = True)

    
class IEventIfEventSite(Interface):
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


class IIkDeleteConfirm(Interface):
    """ Confirm the delete """
    confirmed = Bool(
        title = _(u"Confirm"),
        description = _(u"please confirm"),
        default = False)

from zope.component.interfaces import IObjectEvent

class INewSiteEvent(IObjectEvent):
    """Indicates that a new WorldCookery site has been created"""
