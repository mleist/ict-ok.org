# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of InternalAttachment"""


__version__ = "$Id: interfaces.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# zope imports
from zope.interface import Attribute, Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine, Bytes
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IInternalAttachment(Interface):
    """A InternalAttachment object."""

    filename = TextLine(
        title = _(u'filename'),
        description = _(u"long description text line"),
        required = False)
        
    contentType = TextLine(
        title = _(u'content type'),
        description = _(u"long description choice"),
        required = False)
        
    data = Bytes(
        title = _(u'data'),
        description = _(u"long description date"),
        required = False)

    file = Attribute("file")
        
    def trigger_online():
        """
        trigger workflow
        """


class IInternalAttachmentFolder(Interface):
    """Container for InternalAttachment objects
    """


class IAddInternalAttachment(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllInternalAttachmentTemplates",
        required = False)
