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
"""Configuration adapter for smokeping-config files
"""

__version__ = "$Id$"

# python imports
import codecs

# zope imports
from zope.interface import implements
from zope.component import adapts, getUtility
from zope.component.interface import ComponentLookupError

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.admin_utils.generators.smokeping.interfaces import \
     IGenSmokePing, IAdmUtilGeneratorSmokePing
from org.ict_ok.components.component import IComponent


class GenSmokePing(object):
    """adapter implementation of Superclass -> smokeping
    """
    
    implements(IGenSmokePing)
    adapts(ISuperclass)
    
    # modification of this attributes will trigger an new generation of
    # the config file
    attrList = []
    
    def __init__(self, context):
        #print "SuperclassGenSmokePing.__init__"
        self.fileName = None
        self.fpCfg = None
        self.parentAdapter = None
        self.starttimeCfg = None
        self.context = context
        self.ikRevision = __version__
        self.genOutput = True
        
    def fileOpen(self):
        """will open a filehandle to the specific object
        """
        if self.genOutput:
            self.fpCfg = codecs.open(u'/opt/smokeping/etc/ict_ok/ict.cfg', 'a',
                                     encoding='utf-8')
            self.write(u"\n\n# %s: '%s'\n" % (self.context.myFactory,
                                        self.context.ikName))
    
    def fileClose(self):
        """will close the filehandle to the specific object
        """
        if self.genOutput and \
           self.fpCfg is not None:
            self.fpCfg.close()
            try:
                utilSmokePing = getUtility(IAdmUtilGeneratorSmokePing)
                utilSmokePing.touchLastConfigFile()
            except ComponentLookupError:
                pass

    def write(self, text_arg):
        """will write the text_arg into the configuration file
        """
        if self.genOutput and \
           self.fpCfg is not None:
            self.fpCfg.write(text_arg)

    def traverse4smokepingGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            self.write(u"%s## Pre (%s,%d) - SuperclassGenSmokePing" % \
                       ("\t" * level, self.context.ikName, level))
        return False # no real values changed

    def traverse4smokepingGeneratorPost(self, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            self.write(u"%s## Post (%s,%d) - SuperclassGenSmokePing" % \
                       ("\t" * level, self.context.ikName, level))
        return False # no real values changed

    def traverse4smokepingGeneratorBody(self, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            self.write(u"%s## Body (%s,%d) - SuperclassGenSmokePing" % \
                       ("\t" * level, self.context.ikName, level))
        return False # no real values changed

    def traverse4smokepingGenerator(self, level=0, comments=True):
        """Configuration generator
        
        level: indent-level
        comments: should there comments are in the output?

        """
        valueChanged = False
        if IComponent.providedBy(self.context):
            self.fileOpen()
            if self.traverse4smokepingGeneratorPre(level, comments):
                valueChanged = True
            if self.traverse4smokepingGeneratorBody(level, comments):
                valueChanged = True
            if self.traverse4smokepingGeneratorPost(level, comments):
                valueChanged = True
            self.fileClose()
        return valueChanged
        
    def smokepingConfigFileOut(self, forceOutput=False, event=None):
        """SmokePing-Filegenerator
        
        will produce the smokeping configuration files
        
        forceOutput: False will check for a relevant attribute change
        True will alway generate a new config file
        
        event: None or the zope event from lifecycle
        """
        valueChanged = False
        if forceOutput:
            if self.traverse4smokepingGenerator(0, False):
                valueChanged = True
        else:
            if self.eventModifiesCfgFile(event):
                valueChanged = True
                self.traverse4smokepingGenerator(0, False)
        return valueChanged
    
    def eventModifiesCfgFile(self, event):
        """check for attribute changes
        """
        if event is not None and \
           len(event.descriptions) > 0:
            attrInst = list(event.descriptions)[0]
            modAttributes = set(attrInst.attributes)
            adapterAttributes = set(self.attrList)
            return len(modAttributes.intersection(adapterAttributes)) > 0
        else:
            return False
