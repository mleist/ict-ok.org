# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""implementation of a "esx_vim daemon" 
"""

#TODO delete Debug-Statements 

__version__ = "$Id$"

# phython imports

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.esx_vim.esx_vim_obj import EsxVimObj
from org.ict_ok.admin_utils.esx_vim.interfaces import \
     IEsxVimVirtualMachine
from org.ict_ok.admin_utils.esx_vim.esx_vim import globalEsxVimUtility


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
        print "bbbaa13"
        globalEsxVimUtility.esxThread.getQueue(utilOId)['in'].join()
        print "bbbaa14"
        #self.esxThread.queue1_in.put(localEsxUtil, True, 5)
        #self.esxThread.queue1_in.join()
        retValue = globalEsxVimUtility.esxThread.getQueue(utilOId)['out'].get(True, 15)
        print "retValue: ", retValue
        print "bbbaa15"
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
