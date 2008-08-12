# -*- coding: utf-8 -*-
#
# CopyrightPhysicalQuantityc) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id: interfaces.py 145 2008-02-15 20:41:04Z markusleist $
#
# pylint: disable-msg=W0232
#
"""Physical quantities for ict-ok.org
"""

__version__ = "$Id: host.py 174 2008-03-05 17:51:14Z markusleist $"

# phython imports
from Scientific.Physics.PhysicalQuantities import \
     PhysicalUnit, \
     _addUnit, _addPrefixed, _prefixes
from Scientific.Physics import PhysicalQuantities


class PhysicalQuantity(PhysicalQuantities.PhysicalQuantity):
    """
    """
    _addUnit('event', PhysicalUnit("event", 1.0, [0,0,0,0,0,0,0,0,1] ))
    _prefixes.append(('Ki', 2**10) )
    _prefixes.append(('Mi', 2**20) )
    _prefixes.append(('Gi', 2**30) )
    _prefixes.append(('Ti', 2**40) )
    _prefixes.append(('Pi', 2**50) )
    _prefixes.append(('Ei', 2**60) )
    _prefixes.append(('Zi', 2**70) )
    _addUnit('bit', PhysicalUnit(None, 1.0, [0,0,0,0,0,0,0,1,0]))
    _addPrefixed( 'bit')
    _addUnit('byte', '8*bit')
    _addPrefixed( 'byte')
    _addUnit('cnt', 'event')
