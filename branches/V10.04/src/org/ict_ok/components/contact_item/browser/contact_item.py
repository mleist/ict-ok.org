# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of ContactItem"""

__version__ = "$Id: template.py_cog 465 2009-03-05 02:34:02Z markusleist $"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory
from zope.traversing.browser import absoluteURL

# z3c imports
from z3c.form import field
from z3c.form.browser import checkbox

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.contact_item.interfaces import \
    IContactItem, IAddContactItem, IContactItemFolder
from org.ict_ok.components.contact_item.contact_item import ContactItem
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddContactItem(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Contact Item')
    viewURL = 'add_contact_item.html'
    weight = 50


class MGlobalAddContactItem(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Contact Item')
    viewURL = 'add_contact_item.html'
    weight = 50
    folderInterface = IContactItemFolder

# --------------- object details ---------------------------


class ContactItemDetails(ComponentDetails):
    """ Class for ContactItem details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class ContactItemFolderDetails(ComponentDetails):
    """ Class for ContactItem details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IContactItem
    factory = ContactItem
    omitFields = ContactItemDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsContactItemForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Contact Item')
    factory = ContactItem
    omitFields = ContactItemDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddContactItemForm(AddComponentForm):
    """Add Contact Item form"""
    label = _(u'Add Contact Item')
    factory = ContactItem
    attrInterface = IContactItem
    addInterface = IAddContactItem
    omitFields = ContactItemDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.contact_item'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditContactItemForm(EditForm):
    """ Edit for Contact Item """
    label = _(u'Contact Item Edit Form')
    factory = ContactItem
    omitFields = ContactItemDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteContactItemForm(DeleteForm):
    """ Delete the Contact Item """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this ContactItem: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = ContactItem
    attrInterface = IContactItem
    omitFields = ContactItemDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.contact_item.contact_item.ContactItem'
    allFields = fieldsForInterface(attrInterface, [])


def getRoles(item, formatter):
    """
    Roles for overview table
    """
    if type(item) is dict:
        item = item["obj"]
    ttid = u"roles" + item.getObjectId()
    if len(item.roles) > 2:
        view_url = absoluteURL(item, formatter.request) + '/@@details.html'
        view_html = u'<a href="%s" id="%s">' % (view_url, ttid) + u'[...]</a>'
        rolesList = [i.ikName for i in item.roles]
        rolesList.sort()
        tooltip_text = _(u'<b>Roles:</b>') + u'<br />' +\
            u'<br />'.join(rolesList)
    elif len(item.roles) > 1:
        view0_url = absoluteURL(item.roles[0], formatter.request) +\
                    '/@@details.html'
        view1_url = absoluteURL(item.roles[1], formatter.request) +\
                    '/@@details.html'
        view_html = u'<span id="%s"><a href="%s">' %\
                    (ttid, view0_url) + u'%s</a>' %\
                    item.roles[0].ikName + \
                    u', <a href="%s">' %  (view1_url) + u'%s</a></span>' %\
                    item.roles[1].ikName
        rolesList = [i.ikName for i in item.roles]
        rolesList.sort()
        tooltip_text = _(u'<b>Roles:</b>') + u'<br />' +\
            u'<br />'.join(rolesList)
    elif len(item.roles) == 1:
        view_url = absoluteURL(item.roles[0], formatter.request) +\
                    '/@@details.html'
        view_html = u'<a href="%s" id="%s">' %  (view_url, ttid) + u'%s</a>' %\
                    item.roles[0].ikName
        membersList = [i.ikName for i in item.roles[0].contactItems]
        membersList.sort()
        tooltip_text = _(u'<b>Members:</b>') + u'<br />' +\
            u'<br />'.join(membersList)
    else:
        view_html = u'-'
        tooltip_text = _(u'No roles')
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return view_html + tooltip
