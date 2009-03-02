# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
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

# python imports

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.osi.interfaces import IOSIModel

class OSIModel(object):
    """ISized adapter."""

    implements(IOSIModel)

    linkedObjects = {}

    def __init__(self, context):
        self.context = context
        
#    def connectedComponentsOnLayer1(self, targetSet, searchDepth):
#        """returns a set of components which are connected on layer 1
#
#        targetSet: set of connected components
#        searchDepth: searchDepth will be decreased on every recursive step
#        """
#        print "%s -> connectedComponentsOnLayer1(%s, %s) " % (self.context.ikName, targetSet, searchDepth)
##        import pdb
##        pdb.set_trace()
#        if searchDepth < 0:
#            raise Exception
#        if self.context not in targetSet:
#            print "add(%s)" % (self.context.ikName)
#            targetSet.add(self.context)
#            for obj in self.context.links:
#                nextOSIModelAdapter = IOSIModel(obj)
#                if nextOSIModelAdapter:
#                    nextOSIModelAdapter.connectedComponentsOnLayer1(targetSet, searchDepth-1)

    def connectedComponentsOnLayer(self, layerTuple, targets, searchDepth):
        """returns a set of components which are connected on
        some special layers

        layerTuple: tuple of Layer-Interfaces
        targets: set of connected components
        searchDepth: searchDepth will be decreased on every recursive step
        """
        if searchDepth < 0:
            raise Exception
        layersMatch = [layerInterface for layerInterface in layerTuple
                       if layerInterface.providedBy(self.context)]
        if self.context not in targets and \
            len(layersMatch) > 0:
            targets.append(self.context)
            for relationLayer, relationNames in self.linkedObjects.items():
                for relationName in relationNames:
                    if relationLayer in layerTuple:
                        relations = getattr(self.context, relationName)
                        for obj in relations:
                            nextAdapter = IOSIModel(obj)
                            if nextAdapter:
                                nextAdapter.connectedComponentsOnLayer(
                                   layerTuple, targets, searchDepth-1)
