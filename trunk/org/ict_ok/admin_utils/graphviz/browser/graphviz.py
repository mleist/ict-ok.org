# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142,R0901
#
"""implementation of browser class of the graphviz-utility 
"""

__version__ = "$Id$"

# zope imports
from zope.app import zapi
from zope.proxy import removeAllProxies
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form import field

# ict_ok.org imports
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.graphviz.interfaces import \
     IAdmUtilGraphviz

_ = MessageFactory('org.ict_ok')


class AdmUtilGraphvizDetails(SupernodeDetails):
    """Browser implementation of Graphviz picture generator
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + []

    def getPngFile(self):
        """get dot file and convert to png
        """
        return self.context.getPngFile(zapi.getRoot(self))

    def getCmapxText(self):
        """get dot file and convert to client side image map
        """
        return self.context.getCmapxText(zapi.getRoot(self))

    def getValuePngHref(self):
        """get path of object as string
        """
        obj = removeAllProxies(self.context)
        return zapi.getPath(obj)

# --------------- forms ------------------------------------


class ViewAdmUtilGraphvizForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of graphviz adapter')
    fields = field.Fields(IAdmUtilGraphviz).omit(\
        *AdmUtilGraphvizDetails.omit_viewfields)


class EditAdmUtilGraphvizForm(EditForm):
    """ Edit for for net """
    label = _(u'edit graphviz adapter')
    fields = field.Fields(IAdmUtilGraphviz).omit(\
        *AdmUtilGraphvizDetails.omit_editfields)
