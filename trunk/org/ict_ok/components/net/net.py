# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0142
#
"""implementation of Net

Net does ....

"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds

# ict_ok.org imports
from org.ict_ok.schema.IPy import IP
from org.ict_ok.components.component import Component
from org.ict_ok.components.net.interfaces import INet, IEventIfEventNet


class Net(Component):
    """
    the template instance
    """

    implements(INet, IEventIfEventNet)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    ipv4 = FieldProperty(INet['ipv4'])

    eventInpObjs_inward_relaying_shutdown = FieldProperty(\
        IEventIfEventNet['eventInpObjs_inward_relaying_shutdown'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        print "INet.names(): ", list(INet.names())
        for (name, value) in data.items():
            if name in INet.names():
                setattr(self, name, value)
        self.eventInpObjs_inward_relaying_shutdown = set([])
        self.ikRevision = __version__

    def containsIp(self, ipString):
        """ is ip(String) part of this network?
        """
        myIp = IP(self.ipv4)
        testIp = IP(ipString)
        return testIp in myIp

    def eventInp_inward_relaying_shutdown(self, eventMsg=None):
        """
        forward the event to all objects in this container through the signal filter
        """
        #eventMsg.stopit(self, "Net.eventInp_inward_relaying_shutdown")
        print "Net.eventInp_inward_relaying_shutdown (%s)       " \
        "       ############## <-" % (self.ikName)
        for name, obj in self.items():
            print "-> ", obj
            try:
                obj.eventInp_shutdown(eventMsg)
            except AttributeError:
                print "Dont find method"
            #for attrName in obj.__dict__:
                #print "attr:   %s" % (attrName)
                #if attrName.find("eventInp_shutdown") == 0: # attribute name starts with ...
                    #fnct = getattr(obj, "eventInp_shutdown", None)
                    #if fnct is not None:
                        #fnct(eventMsg)

def getAllNetworks():
    """ get a list of all Nets
    """
    retList = []
    uidutil = getUtility(IIntIds)
    for (myid, myobj) in uidutil.items():
        if INet.providedBy(myobj.object):
            retList.append(myobj.object)
    return retList
