# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of PhysicalComponent"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.traversing.browser import absoluteURL
from zope.i18nmessageid import MessageFactory
from zope.schema import vocabulary
from zope.app.pagetemplate.urlquote import URLQuote

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.components.physical_component.interfaces import IPhysicalComponent
from org.ict_ok.components.physical_component.physical_component import PhysicalComponent
from org.ict_ok.components.browser.component import ComponentDetails

_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------

def vocabValue(vocabName=None, token=None, request=None):
    if vocabName is None:
        return None
    if token is None:
        return None
    vocabReg = vocabulary.getVocabularyRegistry()
    if vocabReg is not None:
        vocab = vocabReg.get(request, vocabName)
        if vocab is not None:
            try:
                vocabTerm = vocab.getTerm(token)
            except LookupError:
                return None
            if vocabTerm:
                return vocabTerm.title
    return None

def getUserName(item, formatter):
    """
    Titel for Overview
    """
    if hasattr(item, 'user'):
        username = vocabValue('AllLdapUser', item.user, formatter.request)
    else:
        return u''
    if username:
        return username
    else:
        return u''

def getRoom(item, formatter):
    """
    Room title for Overview
    """
    if hasattr(item, 'room') and item.room is not None:
        room = item.room
        ttid = u"room" + room.getObjectId()
        roomFullName = room.ikName
        roomNumberStr = u''
        if len(roomFullName) > 15:
            roomShortName = roomFullName[:15] + '...'
        else:
            roomShortName = roomFullName[:15]
        if hasattr(room, 'number') and room.number is not None:
            roomNumberStr = room.number[:8]
            roomText = u'%s&nbsp;(%s)' % (roomShortName, roomNumberStr)
        else:
            roomText = roomShortName
        view_url = absoluteURL(room, formatter.request) + \
                    '/@@details.html'
        view_html = u'<a href="%s" id="%s">' %  (view_url, ttid) + u'%s</a>' %\
                    roomText
        tooltip_text = u'<b>' + _(u'Room:') + u'</b>' + roomFullName
        if len(roomNumberStr) > 0:
            tooltip_text += u'<br />' + \
                u'<b>' + _(u'Number:') + u'</b>&nbsp;' + roomNumberStr
        if hasattr(room, 'building') and room.building is not None:
            building = room.building
            tooltip_text += u'<br />' + \
                u'<b>' + _(u'Building:') + u'</b>&nbsp;' + \
                building.ikName[:40]
            if hasattr(building, 'location') and building.location is not None:
                location = building.location
                tooltip_text += u'<br />' + \
                    u'<b>' + _(u'Location:') + u'</b>&nbsp;' + \
                    location.ikName[:40]
        tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
                u"widget.Tooltip('tt_%s', { autodismissdelay:'25000', " \
                u"context:'%s', text:'%s' });</script>" \
                % (ttid, ttid, ttid, tooltip_text)
    return view_html + tooltip

def fsearch_user_formatter(value, item, formatter):
    if hasattr(item, 'user'):
        username = vocabValue('AllLdapUser', item.user, formatter.request)
    else:
        return u''
    if username:
        quoter = URLQuote(item.user)
        return u'<a href="/@@fsearch?key=%s">%s</a>' % (quoter.quote(), username)
    else:
        return u''


# --------------- object details ---------------------------


class PhysicalComponentDetails(ComponentDetails):
    """ Class for PhysicalComponent details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class PhysicalComponentFolderDetails(ComponentDetails):
    """ Class for MobilePhone details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + ['requirement']
    omit_addfields = ComponentDetails.omit_addfields + ['requirement']
    omit_editfields = ComponentDetails.omit_editfields + ['requirement']
