# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611
#
"""implementation of a "esx_vim daemon" 
"""

#TODO delete Debug-Statements 

__version__ = "$Id$"

# phython imports
from datetime import datetime

# zope imports
from zope.interface import implements
from zope.dublincore.interfaces import IZopeDublinCore
from zope.lifecycleevent import ObjectCreatedEvent
from zope.event import notify
from zope.component import createObject

# ict_ok.org imports
from org.ict_ok.admin_utils.esx_vim.esx_vim_obj import EsxVimObj
from org.ict_ok.admin_utils.esx_vim.interfaces import \
     IEsxVimVirtualMachine
from org.ict_ok.admin_utils.esx_vim.esx_vim import globalEsxVimUtility
from org.ict_ok.components.net.net import getAllNetworks


class EsxVimVirtualMachine(EsxVimObj):
    """
    VirtualMachine is the managed object type for manipulating virtual
    machines, including templates that can be deployed (repeatedly) as new
    virtual machines. This type provides methods for configuring and
    controlling a virtual machine.
    """
    implements(IEsxVimVirtualMachine)
    def keys(self):
        '''See interface `IReadContainer`'''
        print "EsxVimVirtualMachine.keys"
        return {}.keys()

    def __iter__(self):
        print "EsxVimVirtualMachine.__iter__"
        iter({})

    def __getitem__(self, key):
        '''See interface `IReadContainer`'''
        print "EsxVimVirtualMachine.__getitem__(%s)" % key
        return {}[key]

    def get(self, key, default=None):
        '''See interface `IReadContainer`'''
        print "EsxVimVirtualMachine.get('%s','%s')" % (key, default)
        if self.localEsxUtil is None:
            return None
        utilOId = self.localEsxUtil.getObjectId()
        myParams = {\
            'admUtilEsxVim': self.localEsxUtil,
            'cmd': 'call_fcnt_on_obj',
            'perlRef': self.perlEsxObjRef,
            'fnct_name': 'name',
            'fnct_args': [],
            }
        globalEsxVimUtility.esxThread.getQueue(utilOId)['in'].put(myParams, True, 15)
        #print "bbbaa13"
        globalEsxVimUtility.esxThread.getQueue(utilOId)['in'].join()
        #print "bbbaa14"
        #self.esxThread.queue1_in.put(localEsxUtil, True, 5)
        #self.esxThread.queue1_in.join()
        retValue = globalEsxVimUtility.esxThread.getQueue(utilOId)['out'].get(True, 15)
        #print "retValue: ", retValue
        #print "bbbaa15"
        return "zzzuio"
        #return {}.get(key, default)

    def call_esxfcnt_on_obj(self, fnct_name='name', fnct_args=[]):
        """ call an esx function on this object """
        print "EsxVimVirtualMachine.call_esxfcnt_on_obj(%s,%s)" % (fnct_name, fnct_args)
        if self.localEsxUtil is None:
            return None
        utilOId = self.localEsxUtil.getObjectId()
        myParams = {\
            'admUtilEsxVim': self.localEsxUtil,
            'cmd': 'call_fcnt_on_obj',
            'perlRef': self.perlEsxObjRef,
            'fnct_name': fnct_name,
            'fnct_args': fnct_args,
            }
        globalEsxVimUtility.esxThread.getQueue(utilOId)['in'].put(myParams, True, 15)
        globalEsxVimUtility.esxThread.getQueue(utilOId)['in'].join()
        retValue = globalEsxVimUtility.esxThread.getQueue(utilOId)['out'].get(True, 15)
        print "call_esxfcnt_on_obj - retValue: ", retValue
        return retValue

    def values(self):
        '''See interface `IReadContainer`'''
        print "EsxVimVirtualMachine.values"
        return {}.values()

    def __len__(self):
        '''See interface `IReadContainer`'''
        print "EsxVimVirtualMachine.__len__"
        return len({})+1

    def items(self):
        '''See interface `IReadContainer`'''
        print "EsxVimVirtualMachine.items"
        return {}.items()

    def __contains__(self, key):
        '''See interface `IReadContainer`'''
        print "EsxVimVirtualMachine.__contains__(%s)" % key
        return {}.has_key(key)

    def shutdown(self):
        """
        shutdown this esx object to an internal object
        """
        print("EsxVimVirtualMachine.shutdown")

    def convertobj(self):
        """
        converts this esx object to an internal object
        """
        hostname = u"%s" % self.eval_on_obj('obj.name()')
        ip = u"%s" % self.eval_on_obj('obj.guest().ipAddress()')
        hardware = u"ESX virtual machine (%s MB)" % \
            self.eval_on_obj('obj.runtime().maxMemoryUsage()')
        uuid = u"%s" % self.eval_on_obj('obj.config().uuid()')
        netList = []
        index = 0
        while True:
            mac = self.eval_on_obj('obj.guest().net()[%s].macAddress()' % index)
            name = self.eval_on_obj('obj.guest().net()[%s].network()' % index)
            if type(mac) == type('') and \
                type(name) == type(''):
                ipList = []
                ipIndex = 0
                while True:
                    ip = self.eval_on_obj('obj.guest().net()[%s].ipAddress()[%s]' %\
                        (index, ipIndex))
                    if type(ip) == type(''):
                        ipList.append(u"%s" % ip)
                        ipIndex += 1
                    else:
                        break
            else:
                break
            net = {}
            net['index'] = index
            net['mac'] = u"%s" % mac
            net['name'] = u"%s" % name
            net['ips'] = ipList
            netList.append(net)
            index += 1
            if index > 10:
                break
        # name: 'cbw-ikomtrol01'
        # ip: '192.168.157.98'
        # hardware: 'ESX virtual machine (384 MB)'
        # uuid: '500c4d26-525f-ab35-b2ee-9f77842f65b9'
        # netList: [{'index': 0, 'mac': '00:50:56:8c:63:77', 'name': 'CBW Servers', 'ips': ['192.168.157.98']}]

        if len(netList) > 0 and len(netList[0]['ips']) > 0:
            firstIp = netList[0]['ips'][0]
            allNetworks = getAllNetworks()
            for network in allNetworks:
                if network.containsIp(firstIp):
                    print "create here:", network.ikName
                    dateNow = datetime.utcnow()
                    newHost = createObject(\
                        u'org.ict_ok.components.host.host.HostVMwareVm')
                    newHost.__post_init__()
                    notify(ObjectCreatedEvent(newHost))
                    network.__setitem__(newHost.getObjectId(), 
                                        newHost)
                    dcore = IZopeDublinCore(newHost, None)
                    #dcore.creators = [u'ikportscan']
                    newHost.ikComment += u"esx scanner: %s" % (dateNow)
                    #import pdb;pdb.set_trace()
                    newHost.__setattr__("ikName", hostname)
                    newHost.__setattr__("hostname", hostname)
                    dcore.title = hostname
                    newHost.__setattr__("hardware", hardware)
                    newHost.__setattr__("esxUuid", uuid)
                    newHost.__setattr__("genNagios", False)
                    dcore.created = dateNow
                    for interf in netList:
                        newInterface = createObject(\
                            u'org.ict_ok.components.interface.interface.Interface')
                        notify(ObjectCreatedEvent(newInterface))
                        newInterfaceId=u"If%s" % (interf['index'])
                        newHost.__setitem__(newInterfaceId, newInterface)
                        newInterface.__setattr__("description", interf['name'])
                        newInterface.__setattr__("ikName", newInterfaceId)
                        newInterface.ikComment += u"esx scanner: %s" % (dateNow)
                        newInterfaceDc = IZopeDublinCore(newInterface, None)
                        newInterfaceDc.title = newInterfaceId
                        newInterfaceDc.created = datetime.utcnow()
                        #newInterfaceDc.creators = [u'ikportscan']
                        newInterface.netType = "ethernet"
                        newInterface.mac = interf['mac']
                        #newInterface.ipv4List.append(interfaceDict['ipAddress'])
                        newInterface.ipv4List = interf['ips'][0]
                    return newHost
        return None
