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
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm

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


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    factory = OrganisationalUnit
    attrInterface = IOrganisationalUnit
    omitFields = OrganisationalUnitDetails.omit_viewfields
    factoryId = u'org.ict_ok.components.organisational_unit.organisational_unit.OrganisationalUnit'
    allFields = fieldsForInterface(attrInterface, [])
