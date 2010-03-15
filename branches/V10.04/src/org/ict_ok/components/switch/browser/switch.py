# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=W0232,W0142
#
"""implementation of browser class of Switch"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.i18nmessageid import MessageFactory

# z3c imports
from z3c.form.browser import checkbox
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify

# ict_ok.org imports
from org.ict_ok.libs.lib import fieldsForFactory, fieldsForInterface
from org.ict_ok.components.switch.interfaces import \
    ISwitch, IAddSwitch, ISwitchFolder
from org.ict_ok.components.switch.switch import Switch
from org.ict_ok.components.browser.component import ComponentDetails
from org.ict_ok.components.superclass.interfaces import IBrwsOverview
from org.ict_ok.skin.menu import GlobalMenuSubItem, GlobalMenuAddItem
from org.ict_ok.components.superclass.browser.superclass import \
     AddForm, DeleteForm, DisplayForm, EditForm
from org.ict_ok.components.browser.component import AddComponentForm
from org.ict_ok.components.browser.component import ImportCsvDataComponentForm
from org.ict_ok.components.browser.component import ImportXlsDataComponentForm
from org.ict_ok.components.interface.interface import Interface
from org.ict_ok.components.interface.interfaces import IInterfaceFolder
from org.ict_ok.components.superclass.superclass import objectsWithInterface

_ = MessageFactory('org.ict_ok')


# --------------- menu entries -----------------------------


class MSubAddSwitch(GlobalMenuSubItem):
    """ Menu Item """
    title = _(u'Add Switch')
    viewURL = 'add_switch.html'
    weight = 50


class MGlobalAddSwitch(GlobalMenuAddItem):
    """ Menu Item """
    title = _(u'Add Switch')
    viewURL = 'add_switch.html'
    weight = 50
    folderInterface = ISwitchFolder

# --------------- object details ---------------------------


class SwitchDetails(ComponentDetails):
    """ Class for Switch details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []


class SwitchFolderDetails(ComponentDetails):
    """ Class for Switch details
    """
    omit_viewfields = ComponentDetails.omit_viewfields + []
    omit_addfields = ComponentDetails.omit_addfields + []
    omit_editfields = ComponentDetails.omit_editfields + []
    attrInterface = ISwitch
    factory = Switch
    fields = fieldsForFactory(factory, omit_editfields)

# --------------- forms ------------------------------------


class DetailsSwitchForm(DisplayForm):
    """ Display form for the object """
    label = _(u'settings of Switch')
    factory = Switch
    omitFields = SwitchDetails.omit_viewfields
    fields = fieldsForFactory(factory, omitFields)


class AddSwitchForm(AddComponentForm):
    """Add Switch form"""
    label = _(u'Add Switch')
    factory = Switch
    omitFields = SwitchDetails.omit_addfields
    attrInterface = ISwitch
    addInterface = IAddSwitch
    _session_key = 'org.ict_ok.components.switch'
    allFields = fieldsForFactory(factory, omitFields)
    addFields = fieldsForInterface(addInterface, [])
    allFields['isTemplate'].widgetFactory = checkbox.SingleCheckBoxFieldWidget

    def createAndAdd(self, data):
        obj = self.create(data)
        notify(ObjectCreatedEvent(obj))
        self.add(obj)
        oneParent = None
        for object in objectsWithInterface(IInterfaceFolder):
            oneParent = object
            break
        if oneParent is not None and obj.ifCount != None:
            for i in range(1, obj.ifCount+1):
                dataVect = {}
                dataVect['ikName'] = u'%s-%02d' % (obj.ikName, i)
                dataVect['device'] = obj
                newObj = Interface(**dataVect)
                newObj.__post_init__()
                IBrwsOverview(newObj).setTitle(dataVect['ikName'])
                oneParent[newObj.objectID] = newObj
                if hasattr(newObj, "store_refs"):
                    newObj.store_refs(**dataVect)
                notify(ObjectCreatedEvent(newObj))
        return obj



class EditSwitchForm(EditForm):
    """ Edit for Switch """
    label = _(u'Switch Edit Form')
    factory = Switch
    omitFields = SwitchDetails.omit_editfields
    fields = fieldsForFactory(factory, omitFields)


class DeleteSwitchForm(DeleteForm):
    """ Delete the Switch """
    
    def getTitle(self):
        """this title will be displayed in the head of form"""
        return _(u"Delete this Switch: '%s'?") % \
               IBrwsOverview(self.context).getTitle()


class ImportCsvDataForm(ImportCsvDataComponentForm):
    pass


class ImportXlsDataForm(ImportXlsDataComponentForm):
    attrInterface = ISwitch
    factory = Switch
    factoryId = u'org.ict_ok.components.switch.switch.Switch'
    allFields = fieldsForInterface(attrInterface, [])
