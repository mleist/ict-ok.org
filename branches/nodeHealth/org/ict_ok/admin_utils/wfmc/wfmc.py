# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101, E0611
#
"""implementation of the wfmc-utility 
"""

__version__ = "$Id$"

# phython imports
import os, logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# ict_ok.org imports
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.admin_utils.wfmc.interfaces import \
     IAdmUtilWFMC, IGenWFMCDot

# ict_ok.org imports
#from org.ict_ok.admin_utils.wfmc.interfaces import \
     #IAdmUtilWFMC, IIKGenWFMCDot
#from org.ict_ok.components.supernode.interfaces import ISupernode
#from org.ict_ok.admin_utils.wfmc.interfaces import IIKGenWFMCDot


logger = logging.getLogger("AdmUtilWFMC")

def graphvizOutputTypes(dummy_context):
    """Which types of graphviz output can be generated
    """
    prefixes = [u'dot', u'neato', u'twopi', u'circo', u'fdp']
    terms = [SimpleTerm(i, str(i), i) for i in prefixes]
    return SimpleVocabulary(terms)


class AdmUtilWFMC(Supernode):
    """Implementation of WFMC picture generator
    """

    implements(IAdmUtilWFMC)
    wf_pd_dict = {}
    
    def __init__(self):
        Supernode.__init__(self)
        self.graphviz_type = u'dot'
        self.ikRevision = __version__

    def fillDotFile(self, pdId, dotFile, mode=None):
        """generate the dot file
        """
        print >> dotFile, '// GraphViz DOT-File'
        print >> dotFile, 'digraph "%s" {' % (zapi.getRoot(self).__name__)
        if mode and mode.lower() == "fview":
            print >> dotFile, '\tgraph [bgcolor="#E5FFF9", dpi="100.0"];'
        else:
            print >> dotFile, '\tgraph [bgcolor="#E5FFF9", size="6.2,5.2",' +\
            ' splines="true", ratio = "auto", dpi="100.0"];'
        print >> dotFile, '\tedge [style = "setlinewidth(2)", color = gray];'
        print >> dotFile, '\trankdir = LR;'
        if AdmUtilWFMC.wf_pd_dict.has_key(pdId):
            procd = AdmUtilWFMC.wf_pd_dict[pdId]
            for i in procd.activities:
                adapterGenDot = IGenWFMCDot(procd.activities[i])
                if adapterGenDot:
                    adapterGenDot.traverse4DotGenerator(\
                        dotFile,
                        level=1, 
                        comments=True)
            for i in procd.transitions:
                adapterGenDot = IGenWFMCDot(i)
                if adapterGenDot:
                    adapterGenDot.traverse4DotGenerator(\
                        dotFile,
                        level=1, 
                        comments=True)
        print >> dotFile, '}'
        dotFile.flush()
            
    def getIMGFile(self, imgtype, pdId, mode=None):
        """get dot file and convert to png
        """
        #its = root_obj.items()
        dotFileName = '/tmp/dotFile_%s.dot' % os.getpid()
        outFileName = '/tmp/dotFile_%s.out' % os.getpid()
        dotFile = open(dotFileName, 'w')
        self.fillDotFile(pdId, dotFile, mode)
        dotFile.close()
        os.system("%s -T%s -o %s %s" % (self.graphviz_type,
                                        imgtype,
                                        outFileName, 
                                        dotFileName))
        pic = open(outFileName, "r")
        picMem = pic.read()
        pic.close()
        return picMem

    def getCmapxText(self, root_obj):
        """get dot file and convert to client side image map
        """
        its = root_obj.items()
        dotFileName = '/tmp/dotFile_%s.dot' % os.getpid()
        outFileName = '/tmp/dotFile_%s.out' % os.getpid()
        dotFile = open(dotFileName, 'w')
        self.fillDotFile(its, dotFile)
        dotFile.close()
        os.system("%s -Tcmapx -o %s %s" % (self.graphviz_type, 
                                           outFileName, 
                                           dotFileName))
        mymap = open(outFileName, "r")
        mapMem = mymap.read()
        mymap.close()
        return mapMem
