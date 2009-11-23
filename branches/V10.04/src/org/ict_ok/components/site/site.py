# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0612,W0142
#
"""implementation of site """

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import adapter
from zope.app.component.site import SiteManagerContainer, LocalSiteManager
from zope.app.container.interfaces import IObjectAddedEvent
from zope.event import notify

# ict-ok.org imports
from org.ict_ok.components.superclass.superclass import MsgEvent
from org.ict_ok.components.component import Component
from org.ict_ok.components.site.interfaces import ISite, IEventIfEventSite
from org.ict_ok.components.ipnet.interfaces import IIpNet
from org.ict_ok.components.site.interfaces import INewSiteEvent

class NewSiteEvent(object):
    implements(INewSiteEvent)

    def __init__(self, site):
        print "NewSiteEvent:__init__(%s)" % (site)
        self.object = site



class Site(Component, SiteManagerContainer):
#class Site(Component):
    """ ICT_Ok site object """
    implements(ISite, IEventIfEventSite)
    sitename = FieldProperty(ISite['sitename'])
    eventInpObjs_inward_relaying_shutdown = FieldProperty(\
        IEventIfEventSite['eventInpObjs_inward_relaying_shutdown'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        SiteManagerContainer.__init__(self, **data)
        for (name, value) in data.items():
            if name in ISite.names():
                setattr(self, name, value)
        self.eventInpObjs_inward_relaying_shutdown = set([])
        self.ikRevision = __version__

    def setSiteManager(self, sm):
        SiteManagerContainer.setSiteManager(self, sm)
        notify(NewSiteEvent(self))
        
    def eventInp_inward_relaying_shutdown(self, eventMsg=None):
        """
        forward the event to all objects in this container through the signal filter
        """
        print "Site.eventInp_inward_relaying_shutdown()"
        for name, obj in self.items():
            if ISite.providedBy(obj):
                targetFunctionName = "inward_relaying_shutdown"
            elif IIpNet.providedBy(obj):
                targetFunctionName = "inward_relaying_shutdown"
            else:
                targetFunctionName = None
            if eventMsg is not None:
                inst_event = MsgEvent(senderObj = self,
                                      oidEventObject = eventMsg.oidEventObject,
                                      logText = u"inward relaying by site '%s'"\
                                      % self.ikName,
                                      targetFunctionName = targetFunctionName)
                eventMsg.stopit(self,
                                u"relaying by site '%s'" % self.ikName)
            else:
                inst_event = MsgEvent(senderObj = self,
                                      logText = u"inward relaying by site '%s'"\
                                      % self.ikName,
                                      targetFunctionName = targetFunctionName)
            obj.injectInpEQueue(inst_event)

        
@adapter(ISite, IObjectAddedEvent)
def setSiteManagerWhenAdded(site, event):
    site.setSiteManager(LocalSiteManager(site))
    
from zope.app.component.hooks import setSite
from zope.app import zapi


@adapter(INewSiteEvent)
def createLocalUtils(event):
    from org.ict_ok.admin_utils.supervisor.bootstrap import \
        createUtils as createSupervisorUtils
    from org.ict_ok.admin_utils.util_manager.bootstrap import \
        createUtils as createUtilityManagerUtils
    from org.ict_ok.admin_utils.categories.bootstrap import \
        createUtils as createCategoriesUtils
    from org.ict_ok.admin_utils.reports.bootstrap import \
        createUtils as createReportUtils
#    from org.ict_ok.admin_utils.snmpd.bootstrap import \
#        createUtils as createSnmpdUtils
#    from org.ict_ok.admin_utils.ticker.bootstrap import \
#        createUtils as createTickerUtils
    from org.ict_ok.admin_utils.public_viewing.bootstrap import \
        createUtils as createPublicViewingUtils
    from org.ict_ok.admin_utils.notifier.bootstrap import \
        createUtils as createNotifierUtils
    from org.ict_ok.admin_utils.notifier.imail.bootstrap import \
        createUtils as createNotifierIMailUtils
#    from org.ict_ok.admin_utils.notifier.jabber.bootstrap import \
#        createUtils as createNotifierJabberUtils
#    from org.ict_ok.admin_utils.linux_ha.bootstrap import \
#        createUtils as createLinuxHaUtils
    from org.ict_ok.admin_utils.graphviz.bootstrap import \
        createUtils as createGraphvizUtils
    from org.ict_ok.admin_utils.generators.smokeping.bootstrap import \
        createUtils as createGeneratorsSmokepingUtils
    from org.ict_ok.admin_utils.generators.nagios.bootstrap import \
        createUtils as createGeneratorsNagiosUtils
#    from org.ict_ok.admin_utils.generators.honeyd.bootstrap import \
#        createUtils as createGeneratorsHoneydUtils
    from org.ict_ok.admin_utils.eventcrossbar.bootstrap import \
        createUtils as createEventcrossbarUtils
#    from org.ict_ok.admin_utils.esx_vim.bootstrap import \
#        createUtils as createEsxVimUtils
#    from org.ict_ok.admin_utils.cron.bootstrap import \
#        createUtils as createCronUtils
    from org.ict_ok.admin_utils.compliance.bootstrap import \
        createUtils as createComplianceUtils
    from org.ict_ok.admin_utils.wfmc.bootstrap import \
        createUtils as createWfmcUtils
    from org.ict_ok.admin_utils.usermanagement.bootstrap import \
        createUtils as createUsermanagementUtils
    from org.ict_ok.admin_utils.netscan.bootstrap import \
        createUtils as createNetscanUtils
    from org.ict_ok.admin_utils.netscan.demo1.bootstrap import \
        createUtils as createNetscanDemo1Utils
    from org.ict_ok.admin_utils.netscan.nmap.bootstrap import \
        createUtils as createNetscanNmapUtils
    from org.ict_ok.admin_utils.netscan.simple1.bootstrap import \
        createUtils as createNetscanSimple1Utils
    from org.ict_ok.admin_utils.idchooser.bootstrap import \
        createUtils as createIdChooserUtils

    from org.ict_ok.components.appsoftware.bootstrap import \
        createUtils as createApplicationSoftwareUtils
    from org.ict_ok.components.patchpanel.bootstrap import \
        createUtils as createPatchPanelUtils
    from org.ict_ok.components.printer.bootstrap import \
        createUtils as createPrinterUtils
    from org.ict_ok.components.physical_link.bootstrap import \
        createUtils as createPhysicalLinkUtils
    from org.ict_ok.components.pc.bootstrap import \
        createUtils as createPersonalComputerUtils
    from org.ict_ok.components.patchport.bootstrap import \
        createUtils as createPatchPortUtils
    from org.ict_ok.components.outlet.bootstrap import \
        createUtils as createOutletUtils
    from org.ict_ok.components.osoftware.bootstrap import \
        createUtils as createOperatingSoftwareUtils
    from org.ict_ok.components.notebook.bootstrap import \
        createUtils as createNotebookUtils
    from org.ict_ok.components.ipnet.bootstrap import \
        createUtils as createNetUtils
    from org.ict_ok.components.muninvalue.bootstrap import \
        createUtils as createMuninValueUtils
    from org.ict_ok.components.mobilephone.bootstrap import \
        createUtils as createMobilePhoneUtils
    from org.ict_ok.components.happliance.bootstrap import \
        createUtils as createHardwareApplianceUtils
    from org.ict_ok.components.isdnphone.bootstrap import \
        createUtils as createISDNPhoneUtils
    from org.ict_ok.components.ipc.bootstrap import \
        createUtils as createIndustrialComputerUtils
    from org.ict_ok.components.interface.bootstrap import \
        createUtils as createInterfaceUtils
    from org.ict_ok.components.host.bootstrap import \
        createUtils as createHostUtils
    from org.ict_ok.components.display_unit.bootstrap import \
        createUtils as createDisplayUnitUtils
    from org.ict_ok.components.building.bootstrap import \
        createUtils as createBuildingUtils
    from org.ict_ok.components.switch.bootstrap import \
        createUtils as createSwitchUtils
    from org.ict_ok.components.snmpvalue.bootstrap import \
        createUtils as createSNMPValueUtils
    from org.ict_ok.components.service.bootstrap import \
        createUtils as createServiceUtils
    from org.ict_ok.components.room.bootstrap import \
        createUtils as createRoomUtils
    from org.ict_ok.components.rack.bootstrap import \
        createUtils as createRackUtils
    from org.ict_ok.components.misc_physical.bootstrap import \
        createUtils as createMiscPhysicalUtils
    from org.ict_ok.components.location.bootstrap import \
        createUtils as createLocationUtils
    from org.ict_ok.components.latency.bootstrap import \
        createUtils as createLatencyUtils
    from org.ict_ok.components.x509certificate.bootstrap import \
        createUtils as createX509certificateUtils
    from org.ict_ok.components.ip_address.bootstrap import \
        createUtils as createIpAddressUtils

    from org.ict_ok.components.product.bootstrap import \
        createUtils as createProductUtils
    from org.ict_ok.components.address.bootstrap import \
        createUtils as createAddressUtils
    from org.ict_ok.components.organization.bootstrap import \
        createUtils as createOrganizationUtils
    from org.ict_ok.components.person.bootstrap import \
        createUtils as createPersonUtils
    from org.ict_ok.components.contact.bootstrap import \
        createUtils as createContactUtils
    from org.ict_ok.components.contact_item.bootstrap import \
        createUtils as createContactItemUtils
    from org.ict_ok.components.work_order.bootstrap import \
        createUtils as createWorkOrderUtils

    from org.ict_ok.components.group.bootstrap import \
        createUtils as createGroupUtils
    from org.ict_ok.components.role.bootstrap import \
        createUtils as createRoleUtils
    from org.ict_ok.components.physical_media.bootstrap import \
        createUtils as createPhysicalMediaUtils

    setSite(event.object)
#    default = zapi.traverse(event.object, '++etc++site/default')
    
    createSupervisorUtils(event.object)
    createUtilityManagerUtils(event.object)
    createCategoriesUtils(event.object)
    createReportUtils(event.object)
#    createSnmpdUtils(event.object)
#    createTickerUtils(event.object)
    createPublicViewingUtils(event.object)
    createNotifierUtils(event.object)
    createNotifierIMailUtils(event.object)
#    createNotifierJabberUtils(event.object)
#    createLinuxHaUtils(event.object)
    createGraphvizUtils(event.object)
    createGeneratorsSmokepingUtils(event.object)
    createGeneratorsNagiosUtils(event.object)
#    createGeneratorsHoneydUtils(event.object)
    createEventcrossbarUtils(event.object)
#   createEsxVimUtils(event.object)
#    createCronUtils(event.object)
    createComplianceUtils(event.object)
    createWfmcUtils(event.object)
    createUsermanagementUtils(event.object)
    createNetscanUtils(event.object)
    createNetscanDemo1Utils(event.object)
    createNetscanNmapUtils(event.object)
    createNetscanSimple1Utils(event.object)
    createIdChooserUtils(event.object)

    createApplicationSoftwareUtils(event.object)
    createPatchPanelUtils(event.object)
    createPrinterUtils(event.object)
    createPhysicalLinkUtils(event.object)
    createPersonalComputerUtils(event.object)
    createPatchPortUtils(event.object)
    createOutletUtils(event.object)
    createOperatingSoftwareUtils(event.object)
    createNotebookUtils(event.object)
    createNetUtils(event.object)
    createMuninValueUtils(event.object)
    createMobilePhoneUtils(event.object)
    createHardwareApplianceUtils(event.object)
    createISDNPhoneUtils(event.object)
    createIndustrialComputerUtils(event.object)
    createInterfaceUtils(event.object)
    createHostUtils(event.object)
    createDisplayUnitUtils(event.object)
    createBuildingUtils(event.object)
    createSwitchUtils(event.object)
    createSNMPValueUtils(event.object)
    createServiceUtils(event.object)
    createRoomUtils(event.object)
    createRackUtils(event.object)
    createMiscPhysicalUtils(event.object)
    createLocationUtils(event.object)
    createLatencyUtils(event.object)
    createX509certificateUtils(event.object)
    createIpAddressUtils(event.object)

    createProductUtils(event.object)
    createAddressUtils(event.object)
    createOrganizationUtils(event.object)
    createPersonUtils(event.object)
    createContactUtils(event.object)
    createContactItemUtils(event.object)
    createWorkOrderUtils(event.object)

    createRoleUtils(event.object)
    createGroupUtils(event.object)
    createPhysicalMediaUtils(event.object)
