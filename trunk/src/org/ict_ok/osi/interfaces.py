# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,E0211,W0232
#
"""Interface for osi objects"""

__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('org.ict_ok')


class IPhysicalLayer(Interface):
    """Interface of OSI-Layer 1
    """


class IDataLinkLayer(Interface):
    """Interface of OSI-Layer 2
    """


class INetworkLayer(Interface):
    """Interface of OSI-Layer 3
    """


class ITransportLayer(Interface):
    """Interface of OSI-Layer 4
    """


class ISessionLayer(Interface):
    """Interface of OSI-Layer 5
    """


class IPresentationLayer(Interface):
    """Interface of OSI-Layer 6
    """


class IApplicationLayer(Interface):
    """Interface of OSI-Layer 7
    """


class IOSIModel(Interface):
    """Interface of OSI-Adapter
    """
    def connectedComponentsOnLayer1(targets, searchDepth):
        """returns a set of components which are connected on layer 1

        targets: list of connected components
        searchDepth: searchDepth will be decreased on every recursive step
        """

    def connectedComponentsOnLayer(layerTuple, targets, searchDepth):
        """returns a set of components which are connected on
        some special layers

        layerTuple: tuple of Layer-Interfaces
        targets: list of connected components
        searchDepth: searchDepth will be decreased on every recursive step
        """
