# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of an Slave object
"""

__version__ = "$Id$"

# zope imports
from zope.interface import implements
from zope.component import adapter
from zope.event import notify
from zope.schema.fieldproperty import FieldProperty
from zope.app.component.site import LocalSiteManager, SiteManagerContainer
from zope.app.container.interfaces import IObjectAddedEvent
from zope.app.appsetup.bootstrap import ensureUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.intid import IntIds
from zope.app.catalog.catalog import Catalog
from zope.app.catalog.interfaces import ICatalog
from zope.app.component import hooks
from zope.app.catalog.text import TextIndex
from zope.index.text.interfaces import ISearchableText

# ict_ok imports
from org.ict_ok.components.component import Component
from org.ict_ok.components.slave.interfaces import INewSlaveEvent, ISlave
from org.ict_ok.admin_utils.supervisor.interfaces import IAdmUtilSupervisor
from org.ict_ok.admin_utils.supervisor.supervisor import AdmUtilSupervisor


class Slave(SiteManagerContainer, Component):
    """A objectcontainer for new slave data."""

    implements(ISlave)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    title = FieldProperty(ISlave['title'])

    def __init__(self, **data):
        """
        constructor of Slave
        """
        Component.__init__(self, **data)
        for (name, value) in data.items():
            if name in ISlave.names():
                setattr(self, name, value)
        self.ikRevision = __version__
        
    def setSiteManager(self, sm):
        """
        will setup Slave with a site manager
        """
        super(Slave, self).setSiteManager(sm)
        notify(NewSlaveEvent(self))


class NewSlaveEvent(object):
    """
    Indicates that a new ICT_Ok slave node has been created
    """
    
    implements(INewSlaveEvent)
    
    def __init__(self, site):
        self.object = site


@adapter(ISlave, IObjectAddedEvent)
def setSiteManagerWhenAdded(site, event):
    """
    event handler to register
    """
    if ISlave.providedBy(event.object):
        site.setSiteManager(LocalSiteManager(site))
        try:
            old_site = hooks.getSite()
            hooks.setSite(site)
            ensureUtility(event.object, 
                          IIntIds,
                          '',
                          IntIds,
                          '', 
                          copy_to_zlog=False, 
                          asObject=True)
            madeUtilityICatalog = ensureUtility(\
                event.object,
                ICatalog, 
                '', 
                Catalog,
                '', 
                copy_to_zlog=False, 
                asObject=True)
            oid_index = TextIndex(interface=ISearchableText,
                                   field_name='getSearchableOid',
                                   field_callable=True)
            madeUtilityICatalog['oid_index'] = oid_index
            madeAdmUtilSupervisor = ensureUtility(\
                event.object, 
                IAdmUtilSupervisor,
                'AdmUtilSupervisor', 
                AdmUtilSupervisor,
                '',
                copy_to_zlog=False, 
                asObject=True)
            madeAdmUtilSupervisor.status2Master = u"will be a slave"
        finally:
            hooks.setSite(old_site)
    