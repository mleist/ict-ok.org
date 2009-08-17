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
"""implementation of the graphviz-utility 
"""

__version__ = "$Id$"

# python imports
import os, logging

# zope imports
from zope.app import zapi
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# ict_ok.org imports
from org.ict_ok.admin_utils.graphviz.interfaces import \
     IAdmUtilGraphviz, IGenGraphvizDot
from org.ict_ok.components.supernode.supernode import Supernode
from org.ict_ok.components.supernode.interfaces import ISupernode

logger = logging.getLogger("AdmUtilGraphviz")

def graphvizOutputTypes(dummy_context):
    """Which types of graphviz output can be generated
    """
    prefixes = [u'dot', u'neato', u'twopi', u'circo', u'fdp']
    terms = [SimpleTerm(i, str(i), i) for i in prefixes]
    return SimpleVocabulary(terms)


class AdmUtilGraphviz(Supernode):
    """Implementation of Graphviz picture generator
    """

    implements(IAdmUtilGraphviz)

    def __init__(self):
        Supernode.__init__(self)
        self.graphviz_type = u'dot'
        self.ikRevision = __version__

    def fillDotFile(self, oobj, dotFile):
        """generate the dot file
        """
        print >> dotFile, '// GraphViz DOT-File'
        print >> dotFile, 'graph "%s" {' % (zapi.getRoot(self).__name__)
        print >> dotFile, '\tgraph [bgcolor="#E5FFF9"];'
        print >> dotFile, '\tedge [style = "setlinewidth(2)", color = gray];'
        print >> dotFile, '\trankdir = LR;'
        #for (dummy_name, oobj) in objList:
            #if ISupernode.providedBy(oobj):
                #try:
        adapterGenGraphvizDot = IGenGraphvizDot(oobj)
        if adapterGenGraphvizDot:
            #adapterGenGraphvizDot.setParent(oobj)
            adapterGenGraphvizDot.traverse4DotGenerator(\
                dotFile,
                level=1,
                comments=False)
                #except TypeError, err:
                    #logger.error("TypeError in fillDotFile() [%s]" % err)
        print >> dotFile, '}'
        dotFile.flush()
            
    def getPngFile(self, root_obj):
        """get dot file and convert to png
        """
        #its = root_obj.items()
        dotFileName = '/tmp/dotFile_%s.dot' % os.getpid()
        outFileName = '/tmp/dotFile_%s.out' % os.getpid()
        dotFile = open(dotFileName, 'w')
        #self.fillDotFile(its, dotFile)
        self.fillDotFile(root_obj, dotFile)
        dotFile.close()
        os.system("%s -Tpng -o %s %s" % (self.graphviz_type, 
                                         outFileName, 
                                         dotFileName))
        #print "self.graphviz_type: %s" % self.graphviz_type
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