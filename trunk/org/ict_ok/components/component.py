# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of host object

host object represents a single computer system
this might be: server, switch, router, workstation, notebook etc
"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.components.host.interfaces import IHost, IEventIfEventHost
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.components.host.wf.nagios import pd as WfPdNagios
from org.ict_ok.admin_utils.wfmc.wfmc import AdmUtilWFMC


class Host(Supernode):
    """
    the template instance
    """

    implements(IHost, IEventIfEventHost)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    hostname = FieldProperty(IHost['hostname'])
    manufacturer = FieldProperty(IHost['manufacturer'])
    vendor = FieldProperty(IHost['vendor'])
    workinggroup = FieldProperty(IHost['workinggroup'])
    hardware = FieldProperty(IHost['hardware'])
    user = FieldProperty(IHost['user'])
    inv_id = FieldProperty(IHost['inv_id'])
    building = FieldProperty(IHost['building'])
    room = FieldProperty(IHost['room'])
    osList = FieldProperty(IHost['osList'])
    url = FieldProperty(IHost['url'])
    url_type = FieldProperty(IHost['url_type'])
    url_authname = FieldProperty(IHost['url_authname'])
    url_authpasswd = FieldProperty(IHost['url_authpasswd'])
    console = FieldProperty(IHost['console'])
    genNagios = FieldProperty(IHost['genNagios'])
    esxUuid = FieldProperty(IHost['esxUuid'])
    
    eventInpObjs_shutdown = FieldProperty(\
        IEventIfEventHost['eventInpObjs_shutdown'])
    
    wf_pd_dict = {}
    wf_pd_dict[WfPdNagios.id] = WfPdNagios
    AdmUtilWFMC.wf_pd_dict[WfPdNagios.id] = WfPdNagios

    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        # find our correct factory, is there a better solution?
        for (fact_name, fact_obj) in zapi.getFactoriesFor(IHost):
            if (len(fact_name) > 11) and (fact_name[:11]=='org.ict_ok.'):
                self.myFactory = unicode(fact_name)
        # initialize OS List
        self.osList = []
        self.eventInpObjs_shutdown = set([])
        for (name, value) in data.items():
            if name in IHost.names() or \
               name in IEventIfEventHost.names():
                setattr(self, name, value)
        self.ikRevision = __version__
