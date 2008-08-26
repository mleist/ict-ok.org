# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0611
#
"""Adapter implementation of name chooser
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.component import adapts
from zope.i18nmessageid import MessageFactory
from zope.app.container.interfaces import INameChooser
from zope.app.container.contained import NameChooser
from zope.app.folder.interfaces import IRootFolder

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.libs.lib import generateOid, oidIsValid

# ict_ok.org imports
#from org.ict_ok.components.superclass.interfaces import ISuperclass
#from org.ict_ok.libs.iklib import generateOid, oidIsValid

_ = MessageFactory('org.ict_ok')


class SuperclassNameChooser(NameChooser):
    """INameChooser adapter."""

    implements(INameChooser)
    adapts(ISuperclass)

    def chooseName(self, name=None, arg_object=None):
        """
        return a good name for the generation of the object
        """
        if name:
            self.checkName(name, arg_object)
            return name
        try:
            retVal = arg_object.getObjectId()
            if not retVal:
                retVal = unicode(generateOid(self, name, arg_object))
        except Exception, err:
            retVal = unicode(generateOid(self, name, arg_object))
        self.checkName(retVal, arg_object)
        return retVal

    def checkName(self, name, arg_object):
        """
        object name ok?
        """
        oidIsValid(name)
        NameChooser.checkName(self, name, arg_object)

class ZRootFolderNameChooser(NameChooser):
    """INameChooser adapter."""

    implements(INameChooser)
    adapts(IRootFolder)

    def chooseName(self, name=None, arg_object=None):
        """
        return a good name for the generation of the object
        """
        if name:
            self.checkName(name, arg_object)
            return name
        try:
            retVal = arg_object.getObjectId()
            if not retVal:
                retVal = unicode(generateOid(self, name, arg_object))
        except Exception, err:
            retVal = unicode(generateOid(self, name, arg_object))
        self.checkName(retVal, arg_object)
        return retVal

    def checkName(self, name, arg_object):
        """
        object name ok?
        """
        oidIsValid(name)
        NameChooser.checkName(self, name, arg_object)
