# -*- coding: utf-8 -*-
#
# Copyright (c) 2008, 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Notebook"""

__version__ = "$Id: template.py_cog 399 2009-01-08 14:00:17Z markusleist $"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.app.intid.interfaces import IIntIds
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.folder import Folder

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut
from lovely.relation.property import FieldRelationManager

# ict_ok.org imports
from org.ict_ok.libs.lib import getRefAttributeNames
from org.ict_ok.components.superclass.superclass import Superclass
from org.ict_ok.components.notebook.interfaces import INotebook
from org.ict_ok.components.notebook.interfaces import INotebookFolder
from org.ict_ok.components.appsoftware.interfaces import IApplicationSoftware
from org.ict_ok.components.osoftware.interfaces import IOperatingSoftware
from org.ict_ok.components.device.device import Device, DeviceFolder
from org.ict_ok.components.component import Component

def AllNotebooks(dummy_context):
    """Which Notebook are there
    """
    terms = []
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if INotebook.providedBy(oobj.object):
            myString = u"%s" % (oobj.object.getDcTitle())
            terms.append(                SimpleTerm(oobj.object,
                          token=oid,
                          title=myString))
    return SimpleVocabulary(terms)

Notebook_AppSoftware_RelManager = FieldRelationManager(INotebook['appsoftwares'],
                                                       IApplicationSoftware['device'],
                                                       relType='notebook:appsoftwares')
Notebook_OSoftware_RelManager = FieldRelationManager(INotebook['osoftwares'],
                                                       IOperatingSoftware['device'],
                                                       relType='notebook:osoftwares')

class Notebook(Device):
    """
    the template instance
    """
    implements(INotebook)
    shortName = "notebook"
    user = FieldProperty(INotebook['user'])
    productionState = FieldProperty(INotebook['productionState'])
    hardware = FieldProperty(INotebook['hardware'])
    serialNumber = FieldProperty(INotebook['serialNumber'])
    inv_id = FieldProperty(INotebook['inv_id'])
    modelType = FieldProperty(INotebook['modelType'])
    deliveryDate = FieldProperty(INotebook['deliveryDate'])

    appsoftwares = RelationPropertyOut(Notebook_AppSoftware_RelManager)
    osoftwares = RelationPropertyOut(Notebook_OSoftware_RelManager)

    def __init__(self, **data):
        """
        constructor of the object
        """
        Device.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Notebook)
        for (name, value) in data.items():
            if name in INotebook.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def store_refs(self, **data):
        Device.store_refs(self, **data)
        refAttributeNames = getRefAttributeNames(Notebook)
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class NotebookFolder(DeviceFolder):
    implements(INotebookFolder)
    def __init__(self, **data):
        """
        constructor of the object
        """
        DeviceFolder.__init__(self, **data)
