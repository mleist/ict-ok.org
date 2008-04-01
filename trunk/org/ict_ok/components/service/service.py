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

# phython imports

# zope imports
from zope.app import zapi
from zope.schema.fieldproperty import FieldProperty
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.service.interfaces import IService
from org.ict_ok.components.service.wf.nagios import pd as WfPdNagios
from org.ict_ok.admin_utils.wfmc.wfmc import AdmUtilWFMC
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds


class Service(Component):
    """
    the template instance
    """

    implements(IService)
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
        self.product = u""
        self.ipprotocol = None
        for (name, value) in data.items():
            if name in IService.names():
                setattr(self, name, value)
        self.ikRevision = __version__


def getAllServices():
    """ get a list of all services
    """
    retList = []
    uidutil = getUtility(IIntIds)
    for (myid, myobj) in uidutil.items():
        if IService.providedBy(myobj.object):
            retList.append(myobj.object)
    return retList
