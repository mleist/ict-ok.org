# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
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
from org.ict_ok.components.component import Component
from org.ict_ok.components.net.interfaces import INet


class Net(Component):
    """
    the template instance
    """

    implements(INet)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    ipv4 = FieldProperty(INet['ipv4'])

    def __init__(self, **data):
        """
        constructor of the object
        """
        Component.__init__(self, **data)
        # find our correct factory, is there a better solution?
        for (fact_name, fact_obj) in zapi.getFactoriesFor(INet):
            if (len(fact_name) > 11) and (fact_name[:11]=='org.ict_ok.'):
                self.myFactory = unicode(fact_name)
        print "INet.names(): ", list(INet.names())
        for (name, value) in data.items():
            if name in INet.names():
                setattr(self, name, value)
        self.ikRevision = __version__

def getAllNetworks():
    """ get a list of all Nets
    """
    retList = []
    uidutil = getUtility(IIntIds)
    for (myid, myobj) in uidutil.items():
        if INet.providedBy(myobj.object):
            retList.append(myobj.object)
    return retList
