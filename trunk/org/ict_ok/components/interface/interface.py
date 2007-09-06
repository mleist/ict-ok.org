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
"""implementation of Interface

Interface does ....

"""

__version__ = "$Id$"

# phython imports

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.components.interface.interfaces import IInterface


class Interface(Supernode):
    """
    the template instance
    """

    implements(IInterface)
    # for ..Contained we have to:
    __name__ = __parent__ = None
    netType = FieldProperty(IInterface['netType'])
    mac = FieldProperty(IInterface['mac'])
    ipv4List = FieldProperty(IInterface['ipv4List'])
    
    def __init__(self, **data):
        """
        constructor of the object
        """
        Supernode.__init__(self, **data)
        # find our correct factory, is there a better solution?
        for (fact_name, fact_obj) in zapi.getFactoriesFor(IInterface):
            if (len(fact_name) > 11) and (fact_name[:11]=='org.ict_ok.'):
                self.myFactory = unicode(fact_name)
        for (name, value) in data.items():
            if name in IInterface.names():
                setattr(self, name, value)
        self.ikRevision = __version__
