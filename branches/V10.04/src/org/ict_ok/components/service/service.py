# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of Service

Service does ....

"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.schema.fieldproperty import FieldProperty
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.component import Component, ComponentFolder
from org.ict_ok.components.service.interfaces import \
    IService, IAddService, IServiceFolder
from org.ict_ok.components.service.wf.nagios import pd as WfPdNagios
from org.ict_ok.admin_utils.wfmc.wfmc import AdmUtilWFMC
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from org.ict_ok.components.superclass.superclass import objectsWithInterface


def getAllServices():
    """ get a list of all services
    """
    return objectsWithInterface(IService)

def AllServiceTemplates(dummy_context):
    """Which MobilePhone templates exists
    """
    terms = []
    for object in objectsWithInterface(IService):
        if object.isTemplate:
            myString = u"%s [T]" % (object.getDcTitle())
            terms.append(SimpleTerm(object,
                                    token=getattr(object, 'objectID'),
                                    title=myString))
    return SimpleVocabulary(terms)


class Service(Component):
    """
    the template instance
    """

    implements(IService)
    shortName = "service"
    port = FieldProperty(IService['port'])
    product = FieldProperty(IService['product'])
    ipprotocol = FieldProperty(IService['ipprotocol'])

    # for ..Contained we have to:
    __name__ = __parent__ = None
    #ikAttr = FieldProperty(IService['ikAttr'])
    wf_pd_dict = {}
    wf_pd_dict[WfPdNagios.id] = WfPdNagios
    AdmUtilWFMC.wf_pd_dict[WfPdNagios.id] = WfPdNagios

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(Service)
        self.product = u""
        self.ipprotocol = None
        for (name, value) in data.items():
            if name in IService.names():
                if name not in refAttributeNames:
                    setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(Service)

    def store_refs(self, **data):
        Component.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class ServiceFolder(ComponentFolder):
    implements(IServiceFolder, 
               IAddService)
    contentFactory = Service
    shortName = "service folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
