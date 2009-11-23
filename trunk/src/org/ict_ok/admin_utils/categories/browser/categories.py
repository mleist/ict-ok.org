# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0613,W0232,W0201,W0142,W0107
#
"""implementation of browser class of IkSite object
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.traversing.browser import absoluteURL

# zc imports

# z3c imports
from z3c.form import button

# ict-ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm, AddForm, DeleteForm
from org.ict_ok.components.superclass.browser.superclass import \
     Overview as SuperclassOverview
from org.ict_ok.components.superclass.browser.superclass import \
     GetterColumn, getStateIcon, getTitle, raw_cell_formatter, \
     link, getModifiedDate, getActionBottons
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.admin_utils.categories.interfaces import \
     IAdmUtilCatHostGroup
from org.ict_ok.admin_utils.categories.categories import AdmUtilCategories
from org.ict_ok.admin_utils.categories.cat_hostgroup import \
     AdmUtilCatHostGroup
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------

def getUsedCounter(item, formatter):
    """display number of objects, which are using this entry"""
    if IAdmUtilCatHostGroup.providedBy(item):
        return len(item.isUsedIn())

# --------------- menu entries -----------------------------

class MSubAddCatHostGroup(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Host Group')
    viewURL = 'add_hostgroup.html'
    weight = 50

# --------------- object details ---------------------------


class AdmUtilCategoriesDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

class AdmUtilCatHostGroupDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields
    omit_editfields = SupernodeDetails.omit_editfields
    omit_addfields = SupernodeDetails.omit_addfields

    
class Overview(SuperclassOverview):
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Title'),
                     getter=getTitle,
                     cell_formatter=link('overview.html')),
        GetterColumn(title=_('used nr.'),
                     getter=getUsedCounter),
        GetterColumn(title=_('Modified'),
                     getter=getModifiedDate,
                     subsort=True,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    #sort_columns = [0]
# --------------- forms ------------------------------------

# ------ Categories

class DetailsAdmUtilCategoriesForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of categories')
    factory = AdmUtilCategories
    omitFields = AdmUtilCategoriesDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# ------ Host Group


class AddAdmUtilCatHostGroupForm(AddForm):
    """Add form."""
    label = _(u'add host group')
    factory = AdmUtilCatHostGroup
    omitFields = AdmUtilCatHostGroupDetails.omit_addfields
    fields = fieldsForFactory(factory, omitFields)
    
    def nextURL(self):
        """ don't forward the browser """
        return absoluteURL(self.context, self.request)

class EditAdmUtilCatHostGroupForm(EditForm):
    """ Edit of host group """
    label = _(u'edit host group settings')
    factory = AdmUtilCatHostGroup
    omitFields = AdmUtilCatHostGroupDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)

class DeleteAdmUtilCatHostGroupForm(DeleteForm):
    """ Delete the host group """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this host group: '%s'?") % \
               IBrwsOverview(self.context).getTitle()
    
    @button.buttonAndHandler(u'Delete')
    def handleDelete(self, action):
        """delete was pressed"""
        self.deleted = False
        objList = self.getContent().isUsedIn()
        nameList = [obj.ikName for obj in objList]
        if len(objList) > 0:
            self.deleted = False
            self.status = u"already used in: '%s'" % "' ,'".join(nameList)
        else:
            if ISuperclass.providedBy(self.context):
                parent = self.getContent().__parent__
                del parent[self.context.objectID]
                self.deleted = True
                self.context = parent
                url = absoluteURL(parent, self.request)
                self.request.response.redirect(url)
