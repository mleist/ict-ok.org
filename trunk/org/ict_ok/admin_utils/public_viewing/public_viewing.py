# -*- coding: utf-8 -*-
#
# Copyright (c) 2007,
#               Thomas Richter <thomas.richter at xwml.de>,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1111,E1101,E0611,W0613,W0231
#
"""implementation of an usermanagement 
"""

__version__ = "$Id$"

# python imports
import logging

# zope imports
from zope.interface import implements
from zope.app.container.interfaces import IObjectModifiedEvent
from zope.component import adapter

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.public_viewing.interfaces import \
     IAdmUtilPublicViewing

logger = logging.getLogger("AdmUtilPublicViewing")


class AdmUtilPublicViewing(Supernode):
    """Implementation of local PublicViewing Utility"""

    implements(IAdmUtilPublicViewing)

    def __init__(self):
        Supernode.__init__(self)
        self.ikRevision = __version__

class ShadowObject(Supernode):
    """ """

@adapter(ISuperclass, IObjectModifiedEvent)
def notifyModifiedEvent(instance, event):
    """
    Node was modified
    """
    #import pdb; pdb.set_trace()
    #print "AdmUtilPublicViewing.notifyModifiedEvent"
