# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0232,W0142
#
"""implementation of browser class of Site object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.app import zapi
from zope.component import getAllUtilitiesRegisteredFor
from zope.i18nmessageid import MessageFactory
from zope.security.checker import canAccess

# zc imports
from zc.table.column import GetterColumn

# z3c imports
from z3c.form import field

# ict-ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm
from org.ict_ok.admin_utils.util_manager.interfaces import IUtilManager
from org.ict_ok.components.superclass.browser.superclass import \
     Overview as SuperclassOverview
from org.ict_ok.components.superclass.browser import \
     superclass

_ = MessageFactory('org.ict_ok')

# --------------- menu entries -----------------------------

# --------------- object details ---------------------------


class AdmUtilManagerDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']


class Overview(SuperclassOverview):
    """Overview Pagelet"""
    columns = (
        GetterColumn(title="",
                     getter=superclass.getStateIcon,
                     cell_formatter=superclass.raw_cell_formatter),
        GetterColumn(title=_('Title'),
                     getter=superclass.getTitel,
                     cell_formatter=superclass.link('')),
        GetterColumn(title=_('Modified On'),
                     getter=superclass.getModifiedDate,
                     cell_formatter=superclass.raw_cell_formatter),
        GetterColumn(title=_('Size'),
                     getter=superclass.getSize),
        GetterColumn(title=_('Actions'),
                     getter=superclass.getActionBottons,
                     cell_formatter=superclass.raw_cell_formatter),
        )

    def objs(self):
        """List of Content objects"""
        objWithPermisson = []
        allObj = getAllUtilitiesRegisteredFor(ISuperclass)
        for obj in allObj:
            myAdapter = zapi.queryMultiAdapter((obj, self.request),
                                               name='details.html')
            if myAdapter is not None and canAccess(myAdapter, 'render'):
                objWithPermisson.append(obj)
        return objWithPermisson


# --------------- forms ------------------------------------


class ViewAdmUtilManagerForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of utility manager')
    fields = field.Fields(IUtilManager).omit(\
        *AdmUtilManagerDetails.omit_viewfields)


class EditAdmUtilManagerForm(EditForm):
    """ Edit for for net """
    label = _(u'edit utility manager')
    fields = field.Fields(IUtilManager).omit(\
        *AdmUtilManagerDetails.omit_editfields)
