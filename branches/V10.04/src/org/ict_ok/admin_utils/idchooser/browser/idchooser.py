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
from zope.app.component.hooks import getSiteManager

# zc imports

# z3c imports
from z3c.form import button, field
#from z3c.form import button, field, form, interfaces

# ict-ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.browser.supernode import \
     SupernodeDetails
from org.ict_ok.components.superclass.browser.superclass import \
     DisplayForm, EditForm, AddForm, DeleteForm
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.admin_utils.idchooser.interfaces import IIdChooser
from org.ict_ok.admin_utils.idchooser.idchooser import IdChooser
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------

class MSubAddIdChooser(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add ID chooser')
    viewURL = 'add_idchooser.html'
    weight = 50

# --------------- object details ---------------------------


class IdChooserDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + []
    omit_editfields = SupernodeDetails.omit_editfields + ['wasUsed']
    omit_addfields = SupernodeDetails.omit_addfields + ['wasUsed']

# --------------- forms ------------------------------------


class DetailsIdChooserForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of id chooser')
    factory = IdChooser
    omitFields = IdChooserDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)



class AddIdChooserForm(AddForm):
    """Add form."""
    label = _(u'add id chooser')
    factory = IdChooser
    omitFields = IdChooserDetails.omit_addfields
    fields = fieldsForFactory(factory, omitFields)
    
    def nextURL(self):
        """ don't forward the browser """
        return absoluteURL(self.context, self.request)
    
    def createAndAdd(self, data):
        obj = AddForm.createAndAdd(self, data)
        sitem = getSiteManager(self)
        sitem.registerUtility(obj, IIdChooser,
                              name=obj.ikName)
        return obj
    

class EditIdChooserForm(EditForm):
    """ Edit of id chooser"""
    label = _(u'edit host group settings')
    factory = IdChooser
    omitFields = IdChooserDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)
    
    def update(self):
        """update all widgets"""
        if self.context.wasUsed:
            omitList = IdChooserDetails.omit_editfields
            omitList.append('counter')
            self.fields = field.Fields(IIdChooser).omit(*omitList)
        return EditForm.update(self)

class DeleteIdChooserForm(DeleteForm):
    """ Delete the id chooser """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this id chooser: '%s'?") % \
               IBrwsOverview(self.context).getTitle()
    
    @button.buttonAndHandler(u'Delete')
    def handleDelete(self, action):
        """delete was pressed"""
        self.deleted = False
        if self.getContent().wasUsed:
            self.deleted = False
            self.status = u"already used"
        else:
            if ISuperclass.providedBy(self.context):
                sitem = getSiteManager(self)
                parent = self.getContent().__parent__
                sitem.unregisterUtility(component=self.getContent(),
                                        provided=IIdChooser,
                                        name=self.getContent().ikName)
                del parent[self.context.objectID]
                self.deleted = True
                self.context = parent
                url = absoluteURL(parent, self.request)
                self.request.response.redirect(url)
