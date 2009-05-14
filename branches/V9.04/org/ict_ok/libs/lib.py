# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0203,W0702,W0201
#
"""
iklib contains some often used functions from/for System
"""

__version__ = "$Id$"

# python imports
from socket import gethostbyname, gethostname
from time import time
from random import random
from md5 import md5

# zope imports
from zope.app import zapi
from zope.exceptions.interfaces import UserError
from zope.i18nmessageid import MessageFactory
from zope.app.catalog.interfaces import ICatalog
from zope.app.intid.interfaces import IIntIds
from zope.dublincore.interfaces import IZopeDublinCore
from zope.component import createObject
from zope.component import getUtility

# lovely imports
from lovely.relation.property import RelationPropertyIn
from lovely.relation.property import RelationPropertyOut

# ict_ok.org imports

_ = MessageFactory('org.ict_ok')


def generateOid(*args ):
    """
      Generates a universally unique ID.
      Any arguments only create more randomness.
    """
    t_time = long(time() * 1000 )
    t_rand = long(random() * 100000000000000000L )
    try:
        t_hostn = gethostbyname(gethostname() )
    except:
        # if we can't get a network address, just imagine one
        t_hostn = random() * 100000000000000000L
    data = str(t_time) + ' ' + str(t_rand) + ' ' + \
         str(t_hostn) #+ ' ' + str(args)
    data = md5(data).hexdigest()
    int_list = [int(i, 16) for i in data]
    crc = 0
    for i in int_list:
        crc ^= i # xor it
    return u"%s%x" % (data, crc)

def oidIsValid(arg_oid):
    """ check the arg_oid for valid oid string """
    try:
        oid = str(arg_oid)
        uid = oid[:-1]
        crc = oid[-1]
        icrc_cmp = 0
        int_list = [int(i, 16) for i in uid]
        for i in int_list:
            icrc_cmp ^= i
        crc_cmp = u"%x" % icrc_cmp
        if crc != crc_cmp:
            raise UserError(_("Oid is not correct."))
    except:
        raise UserError(_("Oid is not correct."))
    return True


def convertSystemUptime2String(uptime_sec):
    """
    simple convert of seconds since epoc to text-string
    """
    seconds = int(uptime_sec)
    stru = [0, 0, 0, 0]
    stru[0] = seconds / 86400
    seconds -= stru[0] * 86400
    stru[1] = seconds / 3600
    seconds -= stru[1] * 3600
    stru[2] = seconds / 60
    seconds -= stru[2] * 60
    stru[3] = seconds
    if stru[0] == 0:
        upstr = ""
    elif stru[0] == 1: upstr = "1 day, "
    else: upstr = "%d days, " % stru[0]
    upstr += "%02d:%02d:%02d" % (stru[1], stru[2], stru[3])
    return upstr

class RingBuffer:
    """ Ringbuffer class for history """
    def __init__(self, size_max):
        self.max = size_max
        self.data = []
    def append(self, item):
        """append an element at the end of the buffer"""
        self.data.append(item)
        if len(self.data) == self.max:
            self.cur = 0
            self.__class__ = RingBufferFull
    def get(self):
        """ return a list of elements from the oldest to the newest"""
        return self.data


class RingBufferFull:
    """ Instance of RingBuffer will be change the __class__ to
    RingBufferFull when size_max is reached"""
    def __init__(self, arg_n):
        raise Exception, "you should use RingBuffer"
    def append(self, item):
        """append means rotate"""
        self.data[self.cur] = item
        self.cur = (self.cur + 1) % self.max
    def get(self):
        """ return a list of elements from the oldest to the newest"""
        return self.data[self.cur:] + self.data[:self.cur]

def _helperNodeIsUnder(underObj, upperObj):
    #print "_helperNodeIsUnder(%s,%s)" % (underObj, upperObj)
    if underObj.__parent__ == None:
        return False
    elif underObj.__parent__ == upperObj:
        return True
    else:
        return _helperNodeIsUnder(underObj.__parent__, upperObj)

def nodeIsUnder(underNodeOid, upperNodeOid):
    """ checks if the underNode is contained in the upperNode """
    #print "nodeIsUnder(%s, %s)" % (underNodeOid, upperNodeOid)
    if underNodeOid is None:
        return False
    if upperNodeOid is None:
        return False
    if not oidIsValid(underNodeOid):
        return False
    if not oidIsValid(upperNodeOid):
        return False
    underObj = None
    upperObj = None
    my_catalog = zapi.getUtility(ICatalog)
    res = my_catalog.searchResults(oid_index=underNodeOid)
    if len(res) > 0:
        underObj = iter(res).next()
    res = my_catalog.searchResults(oid_index=upperNodeOid)
    if len(res) > 0:
        upperObj = iter(res).next()
    if underObj is not None and \
       upperObj is not None:
        return _helperNodeIsUnder(underObj, upperObj)

def getFirstObjectFor(interf):
    uidutil = getUtility(IIntIds)
    for (oid, oobj) in uidutil.items():
        if interf.providedBy(oobj.object):
            return oobj.object
    return None
            

def oid2dcTitle(arg_oid):
    """ converts an oid into the object dc title """
    if arg_oid is None:
        return "Oid is None"
    if not oidIsValid(arg_oid):
        return "Oid is not valid"
    my_catalog = zapi.getUtility(ICatalog)
    res = my_catalog.searchResults(oid_index=arg_oid)
    if len(res) > 0:
        return iter(res).next().getDcTitle()
    return "Oid not found"

def getRefAttributeNames(arg_class):
    """return a string list of attribute names with
    RelationPropertyIn- or RelationPropertyOut-type
    """
    retList = []
    for attrName, attrValue in arg_class.__dict__.items():
        if type(attrValue)==RelationPropertyIn or \
           type(attrValue)==RelationPropertyOut:
            retList.append(attrName)
    return retList
    
def ensureComponentFolderOnBootstrap(interface, folderName, factoryId,
                                     root_folder, siteManager):
    allSubFolders = [folder for folder in root_folder.values()
                     if interface.providedBy(folder)]
    utils = [ util for util in siteManager.registeredUtilities()
              if util.provided.isOrExtends(IIntIds)]
    instUtilityIIntIds = utils[0].component
    if len(allSubFolders) < 1: # there is no subfolder
        newFolder = createObject(factoryId)
        root_folder[folderName] = newFolder
        dcore = IZopeDublinCore(newFolder, None)
        #dcore.creators = [u'ikportscan']
        #newFolder.ikComment += u"scanner: %s" % (dateNow)
        newFolder.__setattr__("ikName", folderName)
        dcore.title = folderName
        instUtilityIIntIds.register(newFolder)
    else:
        for obj in allSubFolders:
            instUtilityIIntIds.register(obj)

from zope.interface import implementedBy
from z3c.form.field import Fields

def fieldsForFactory(factory, omitFields, additionalInterfaces=[]):
    """return z3c.form fields for the given ict-factory
    """
    interfaceList = [i for i in implementedBy(factory)
                     if i.__identifier__[:10] == 'org.ict_ok']
    interfaceList.reverse()
    interfaceList.extend(additionalInterfaces)
    return Fields(*interfaceList).omit(*omitFields)

def fieldsForInterface(interface_s, omitFields):
    """return z3c.form fields for the given ict-interface
    """
    if type(interface_s) == type(list):
        interfaceList = [i for i in interface_s
                         if i.__identifier__[:10] == 'org.ict_ok']
    else:
        interfaceList = [interface_s]
    return Fields(*interfaceList).omit(*omitFields)
