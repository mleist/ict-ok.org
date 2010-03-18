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
"""implementation of browser class of OrganisationalUnit"""

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
from org.ict_ok.components.organisational_unit.interfaces import \
    IOrganisationalUnit, IAddOrganisationalUnit, IOrganisationalUnitFolder
from org.ict_ok.components.organisational_unit.organisational_unit import OrganisationalUnit
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.superclass.browser.superclass import \
    Overview as SuperOverview
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm
from org.ict_ok.components.superclass.browser.superclass import \
    GetterColumn, DateGetterColumn, getStateIcon, raw_cell_formatter, \
    getHealth, getTitle, getModifiedDate, link, getActionBottons, IctGetterColumn
from org.ict_ok.components.address.browser.address import getAddresses

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddOrganisationalUnit(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add OrganisationalUnit')
    viewURL = 'add_organisational_unit.html'
    weight = 50


class MGlobalAddOrganisationalUnit(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add OrganisationalUnit')
    viewURL = 'add_organisational_unit.html'
    weight = 50
    folderInterface = IOrganisationalUnitFolder

class MSubInvOrganisationalUnit(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'All OrganisationalUnits')
    viewURL = '/@@all_organizations_unit.html'
    weight = 100

# --------------- object details ---------------------------


class OrganisationalUnitDetails(ComponentDetails):
    """ Class for OrganisationalUnit details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class OrganisationalUnitFolderDetails(ComponentDetails):
    """ Class for OrganisationalUnit details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = IOrganisationalUnit
    factory = OrganisationalUnit
    omitFields = OrganisationalUnitDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)

# --------------- forms ------------------------------------


class DetailsOrganisationalUnitForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of OrganisationalUnit')
    factory = OrganisationalUnit
    omitFields = OrganisationalUnitDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddOrganisationalUnitForm(AddComponentForm):
    """Add OrganisationalUnit form"""
    label = _(u'Add OrganisationalUnit')
    factory = OrganisationalUnit
    attrInterface = IOrganisationalUnit
    addInterface = IAddOrganisationalUnit
    omitFields = OrganisationalUnitDetails.omit_addfields
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    _session_key = 'org.ict_ok.components.organisational_unit'
    allFields['isTemplate'].widgetFactory = \
        checkbox.SingleCheckBoxFieldWidget


class EditOrganisationalUnitForm(EditForm):
    """ Edit for OrganisationalUnit """
    label = _(u'OrganisationalUnit Edit Form')
    factory = OrganisationalUnit
    omitFields = OrganisationalUnitDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteOrganisationalUnitForm(DeleteForm):
    """ Delete the OrganisationalUnit """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this OrganisationalUnit: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = OrganisationalUnit
    attrInterface = IOrganisationalUnit
    omitFields = OrganisationalUnitDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.organisational_unit.organisational_unit.OrganisationalUnit'
    allFields = fieldsForInterface(attrInterface, [])


def getMembers(item, formatter):
    """
    Roles for overview table
    """
    if type(item) is dict:
        item = item["obj"]
    ttid = u"members" + item.getObjectId()

    if len(item.members) > 2:
        view_url = absoluteURL(item, formatter.request) + '/@@details.html'
        view_html = u'<a href="%s" id="%s">' % (view_url, ttid) + u'[...]</a>'
        addressesList = [i.ikName for i in item.members]
        addressesList.sort()
        tooltip_text = _(u'<b>Addresses:</b>') + u'<br />' +\
            u'<br />'.join(addressesList)
    elif len(item.members) > 1:
        view0_url = absoluteURL(item.members[0], formatter.request) +\
                    '/@@details.html'
        view1_url = absoluteURL(item.members[1], formatter.request) +\
                    '/@@details.html'
        view_html = u'<span id="%s"><a href="%s">' %\
                    (ttid, view0_url) + u'%s</a>' %\
                    item.members[0].ikName + \
                    u', <a href="%s">' %  (view1_url) + u'%s</a></span>' %\
                    item.members[1].ikName
        addressesList = [i.ikName for i in item.members]
        addressesList.sort()
        tooltip_text = _(u'<b>Addresses:</b>') + u'<br />' +\
            u'<br />'.join(addressesList)
    elif len(item.members) == 1:
        view_url = absoluteURL(item.members[0], formatter.request) +\
                    '/@@details.html'
        view_html = u'<a href="%s" id="%s">' %  (view_url, ttid) + u'%s</a>' %\
                    item.members[0].ikName
        tooltip_text = u''
    else:
        view_html = u'-'
        tooltip_text = _(u'No roles')
    tooltip = u"<script type=\"text/javascript\">tt_%s = new YAHOO." \
            u"widget.Tooltip('tt_%s', { autodismissdelay:'15000', " \
            u"context:'%s', text:'%s' });</script>" \
            % (ttid, ttid, ttid, tooltip_text)
    return view_html + tooltip


class Overview(SuperOverview):
    columns = (
        GetterColumn(title="",
                     getter=getStateIcon,
                     cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Health'),
                     getter=getHealth),
        IctGetterColumn(title=_('Title'),
                        getter=getTitle,
                        cell_formatter=link('overview.html')),
        IctGetterColumn(title=_('Members'),
                        getter=getMembers,
                        cell_formatter=raw_cell_formatter),
        DateGetterColumn(title=_('Modified'),
                        getter=getModifiedDate,
                        subsort=True,
                        cell_formatter=raw_cell_formatter),
        GetterColumn(title=_('Actions'),
                     getter=getActionBottons,
                     cell_formatter=raw_cell_formatter),
        )
    pos_column_index = 1
    sort_columns = [1, 2, 3, 4]

class AllOrganisationalUnits(Overview):
    objListInterface = IOrganisationalUnit
