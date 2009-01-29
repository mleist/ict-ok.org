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
"""Interface of Outlet"""


__version__ = "$Id: interfaces.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine
from zope.app.folder.interfaces import IFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.interfaces import IComponent

_ = MessageFactory('org.ict_ok')


class IOutlet(IComponent):
    """A Outlet object."""

    conns = List(title=u"Conns 0..n",
                 #value_type=Object(IObject),
                 value_type=Choice(vocabulary='AllOutlets'),
                 required=False,
                 default=[])
    conn = Choice(
        title=u'Conn 0..1',
        vocabulary='AllOutlets',
        required=False
        )
    #related = schema.List(
            #title=u"Related",
            #value_type=schema.Choice(vocabulary='demo.documentsInParent'),
            #required=False,
            #default=[])

    attrFoo = TextLine(
        max_length = 80,
        title = _("Foo"),
        description = _("Foo of the system."),
        default = _("default foo"),
        required = True)

    def trigger_online():
        """
        trigger workflow
        """


class IOutletFolder(ISuperclass, IFolder):
    """Container for Outlet objects
    """


class IAddOutlet(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllOutletTemplates",
        required = False)
