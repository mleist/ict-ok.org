# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1111,E0611,W0613
#
"""implementation of an usermanagement 
"""

__version__ = "$Id$"

# phython imports
import logging
from persistent.dict import PersistentDict

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.security.interfaces import IPrincipal
from zope.annotation.interfaces import IAnnotations

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.usermanagement.interfaces import \
     IAdmUtilUserManagement

logger = logging.getLogger("AdmUtilUserManagement")

KEY = "org.ict_ok.admin_utils.usermanagement"

class MappingProperty(object):
    """
    helper class for properties
    """
    def __init__(self, name):
        self.name = name
        
    def __get__(self, inst, class_=None):
        return inst.mapping[self.name]
    
    def __set__(self, inst, value):
        inst.mapping[self.name] = value

class AdmUtilUserManagement(Supernode):
    """Implementation of local UserManagement Utility"""

    implements(IAdmUtilUserManagement)
    adapts(IPrincipal)

    def __init__(self, context):
        Supernode.__init__(self)
        annotations = IAnnotations(context)
        mapping = annotations.get(KEY)
        if mapping is None:
            blank = { 'email': u''}
            mapping = annotations[KEY] = PersistentDict(blank)
        self.mapping = mapping
        self.ikRevision = __version__
            
    email = MappingProperty('email')
