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
from org.ict_ok.admin_utils.categories.interfaces import ICategory
#     IAdmUtilCatHostGroup
from org.ict_ok.admin_utils.categories.categories import \
    AdmUtilCategories, Category
#from org.ict_ok.admin_utils.categories.cat_hostgroup import \
#     AdmUtilCatHostGroup
from org.ict_ok.skin.menu import GlobalMenuSubItem

_ = MessageFactory('org.ict_ok')


# --------------- helper functions -------------------------

def getUsedCounter(item, formatter):
    """display number of objects, which are using this entry"""
    if ICategory.providedBy(item):
        return len(item.components)

# --------------- menu entries -----------------------------

class MSubAddCategory(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Category')
    viewURL = 'add_category.html'
    weight = 50

# --------------- object details ---------------------------


class AdmUtilCategoriesDetails(SupernodeDetails):
    """ Class for Web-Browser-Details
    """
    omit_viewfields = SupernodeDetails.omit_viewfields + ['ikName']
    omit_editfields = SupernodeDetails.omit_editfields + ['ikName']

class CategoryDetails(SupernodeDetails):
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


class AddAdmUtilCategoryForm(AddForm):
    """Add Category form."""
    label = _(u'add category')
    factory = Category
    omitFields = CategoryDetails.omit_addfields
    fields = fieldsForFactory(factory, omitFields)
    
    def nextURL(self):
        """ don't forward the browser """
        return absoluteURL(self.context, self.request)

class EditAdmUtilCategoryForm(EditForm):
    """ Edit of Category """
    label = _(u'edit category settings')
    factory = Category
    omitFields = CategoryDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)

class DeleteAdmUtilCategoryForm(DeleteForm):
    """ Delete the host group """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this host group: '%s'?") % \
               IBrwsOverview(self.context).getTitle()
    
    @button.buttonAndHandler(u'Delete')
    def handleDelete(self, action):
        """delete was pressed"""
        self.deleted = False
        objList = self.getContent().components
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

def getCategories(item, formatter):
    """
    Roles for overview table
    """
    if type(item) is dict and item.has_key('req'):
        item = item["req"]
    ttid = u"categories" + item.getObjectId()
    if len(item.categories) > 2:
        view_url = absoluteURL(item, formatter.request) + '/@@details.html'
        view_html = u'<a href="%s" id="%s">' % (view_url, ttid) + u'[...]</a>'
        rolesList = [i.ikName for i in item.categories]
        rolesList.sort()
        tooltip_text = _(u'<b>Categories:</b>') + u'<br />' +\
            u'<br />'.join(rolesList)
    elif len(item.categories) > 1:
        view0_url = absoluteURL(item.categories[0], formatter.request) +\
                    '/@@details.html'
        view1_url = absoluteURL(item.categories[1], formatter.request) +\
                    '/@@details.html'
        view_html = u'<span id="%s"><a href="%s">' %\
                    (ttid, view0_url) + u'%s</a>' %\
                    item.categories[0].ikName + \
                    u', <a href="%s">' %  (view1_url) + u'%s</a></span>' %\
                    item.categories[1].ikName
        rolesList = [i.ikName for i in item.categories]
        rolesList.sort()
        tooltip_text = _(u'<b>Categories:</b>') + u'<br />' +\
            u'<br />'.join(rolesList)
    elif len(item.categories) == 1:
        view_url = absoluteURL(item.categories[0], formatter.request) +\
                    '/@@details.html'
        view_html = u'<a href="%s" id="%s">' %  (view_url, ttid) + u'%s</a>' %\
                    item.categories[0].ikName
        rolesList = [i.ikName for i in item.categories]
        rolesList.sort()
        tooltip_text = _(u'<b>Categories:</b>') + u'<br />' +\
            u'<br />'.join(rolesList)
    else:
        view_html = u'-'
        tooltip_text = _(u'No roles')
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return view_html + tooltip
