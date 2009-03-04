# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py_cog 411M 2009-02-02 23:31:12Z (lokal) $
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of PatchPort"""


__version__ = "$Id: interfaces.py_cog 411M 2009-02-02 23:31:12Z (lokal) $"

# zope imports
from zope.interface import Interface, Invalid, invariant
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Bytes, List

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


class IPatchPort(Interface):
    """A PatchPort object."""

    patchpanel = Choice(
        title = _(u'Patch panel'),
        vocabulary = 'AllPatchPanels',
        required = False)
    
#    frontLink = Choice(
#        title=_(u'front link'),
#        vocabulary='AllPhysicalLinks',
#        required=False
#        )
#
#    rearLink = Choice(
#        title=_(u'rear link'),
#        vocabulary='AllPhysicalLinks',
#        required=False
#        )

#    ddd = List (
#        title = _("ddd"),
#        value_type = Bytes(
#            title = _("ddd1")),
#        readonly = False,
#        required = False)

#    @invariant
#    def ensurePortAndPanelInSameRoom(event):
#        import pdb
#        pdb.set_trace()
#        if event.room is not None and \
#           event.patchpanel is not None and \
#           event.patchpanel.room is not None and \
#           event.patchpanel.room != event.room:
#            raise Invalid(
#                "Port (%s) and Panel (%s) in different rooms." % \
#                event.room.ikName, event.patchpanel.room.ikName)

    def trigger_online():
        """
        trigger workflow
        """
        
    def ensureInvariants(formObj):
        """
        invariants for the patchport
        """


class IPatchPortFolder(Interface):
    """Container for PatchPort objects
    """


class IAddPatchPort(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllPatchPortTemplates",
        required = False)
