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
"""Configuration adapter for nagios-config files
"""

__version__ = "$Id$"

# phython imports
import logging
from datetime import datetime
from pytz import timezone
import codecs

# zope imports
from zope.interface import implements
from zope.component import adapts, getUtility
from zope.component.interface import ComponentLookupError

# ict_ok.org imports
from org.ict_ok.components.superclass.interfaces import ISuperclass
from org.ict_ok.admin_utils.generators.nagios.interfaces import \
     IGenNagios, IAdmUtilGeneratorNagios
from org.ict_ok.version import getIkVersion
from org.ict_ok.components.component import IComponent
logger = logging.getLogger("SuperclassGenNagios")


class GenNagios(object):
    """adapter implementation of Superclass -> nagios
    """
    
    implements(IGenNagios)
    adapts(ISuperclass)
    
    # modification of this attributes will trigger an new generation of
    # the config file
    attrList = []
    
    def __init__(self, context):
        #print "SuperclassGenNagios.__init__"
        self.fileName = None
        self.fpCfg = None
        self.parentAdapter = None
        self.starttimeCfg = None
        self.context = context
        self.ikRevision = __version__
        
    def fileOpen(self):
        """will open a filehandle to the specific object
        """
        berlinTZ = timezone('Europe/Berlin')
        self.starttimeCfg = datetime.now(berlinTZ)
        if self.fileName is None:
            self.fileName = u'/opt/nagios/etc/ict_ok/Misc/%s.cfg' % \
                self.context.getObjectId()
        self.fpCfg = codecs.open(self.fileName, 'w', encoding='utf-8')
        self.write(u"# %s\n" % self.fileName)
        self.write(u"# %s: '%s'\n" % (self.context.myFactory,
                                    self.context.ikName))
        self.write(u"# generated by ict-ok.org Ver. %s (%s)\n\n" %
                   (getIkVersion(), self.starttimeCfg))
    
    def fileClose(self):
        """will close the filehandle to the specific object
        """
        if self.fpCfg is not None:
            berlinTZ = timezone('Europe/Berlin')
            self.write(u"\n\n# ok, generated in %s\n" %
                       (datetime.now(berlinTZ) - self.starttimeCfg))
            self.fpCfg.close()
            try:
                utilNagios = getUtility(IAdmUtilGeneratorNagios)
                utilNagios.touchLastConfigFile()
            except ComponentLookupError:
                pass

    def write(self, text_arg):
        """will write the text_arg into the configuration file
        """
        if self.fpCfg is not None:
            self.fpCfg.write(text_arg)

    def wantsCheck(self):
        """object is configured to be checked?
        """
        return False

    def traverse4nagiosGeneratorPre(self, level=0, comments=True):
        """graphviz configuration preamble
        """
        if comments:
            self.write(u"%s## Pre (%s,%d) - SuperclassGenNagios" % \
                       ("\t" * level, self.context.ikName, level))

    def traverse4nagiosGeneratorPost(self, level=0, comments=True):
        """graphviz configurations text after object
        """
        if comments:
            self.write(u"%s## Post (%s,%d) - SuperclassGenNagios" % \
                       ("\t" * level, self.context.ikName, level))

    def traverse4nagiosGeneratorBody(self, level=0, comments=True):
        """graphviz configuration data of/in object
        """
        if comments:
            self.write(u"%s## Body (%s,%d) - SuperclassGenNagios" % \
                       ("\t" * level, self.context.ikName, level))

    def traverse4nagiosGenerator(self, level=0, comments=True):
        """Configuration generator
        
        level: indent-level
        comments: should there comments are in the output?

        """
        if IComponent.providedBy(self.context):
            self.fileOpen()
            self.traverse4nagiosGeneratorPre(level, comments)
            self.traverse4nagiosGeneratorBody(level, comments)
            self.traverse4nagiosGeneratorPost(level, comments)
            self.fileClose()
        
    def nagiosConfigFileOut(self, forceOutput=False, event=None):
        """Nagios-Filegenerator
        
        will produce the nagios configuration files
        
        forceOutput: False will check for a relevant attribute change
        True will alway generate a new config file
        
        event: None or the zope event from lifecycle
        """
        if forceOutput:
            self.traverse4nagiosGenerator(0, False)
        else:
            if self.eventModifiesCfgFile(event):
                self.traverse4nagiosGenerator(0, False)

    def nagiosConfigFileRemove(self):
        """remove old nagios configuration file for this object
        """
        pass
    
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
