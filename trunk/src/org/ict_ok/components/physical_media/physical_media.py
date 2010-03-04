# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,W0142
#
"""implementation of PhysicalMedia"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

# lovely imports
from lovely.relation.property import RelationPropertyIn

# ict_ok.org imports
from org.ict_ok.components.component import getRefAttributeNames
from org.ict_ok.components.physical_media.interfaces import IPhysicalMedia
from org.ict_ok.components.physical_media.interfaces import IPhysicalMediaFolder
from org.ict_ok.components.physical_media.interfaces import IAddPhysicalMedia
from org.ict_ok.components.component import ComponentFolder
from org.ict_ok.components.component import \
    AllComponents, AllComponentTemplates, AllUnusedOrSelfComponents
from org.ict_ok.components.physical_component.physical_component import \
    PhysicalComponent
from org.ict_ok.components.device.device import Devices_PhysicalMedia_RelManager

def AllPhysicalMediaTemplates(dummy_context):
    return AllComponentTemplates(dummy_context, IPhysicalMedia)

def AllPhysicalMedia(dummy_context):
    return AllComponents(dummy_context, IPhysicalMedia,
                         additionalAttrNames=['device'])

def AllUnusedOrUsedDevicePhysicalMedia(dummy_context):
    return AllUnusedOrSelfComponents(dummy_context, IPhysicalMedia, 'device')

def PhysicalMediaMediaTypes(dummy_context):
    terms = []
    for (gkey, gname) in {
         0: u"Unknown", 
         1: u"Other",
         2: u"Tape Cartridge", 
         3: u"QIC Cartridge", 
         4: u"AIT Cartridge", 
         5: u"DTF Cartridge", 
         6: u"DAT Cartridge", 
         7: u"8mm Tape Cartridge", 
         8: u"19mm Tape Cartridge", 
         9: u"DLT Cartridge", 
        10: u"Half-Inch Magnetic Tape Cartridge", 
        11: u"Cartridge Disk", 
        12: u"JAZ Disk", 
        13: u"ZIP Disk", 
        14: u"SyQuest Disk", 
        15: u"Winchester Removable Disk", 
        16: u"CD-ROM", 
        17: u"CD-ROM/XA", 
        18: u"CD-I", 
        19: u"CD Recordable", 
        20: u"WORM", 
        21: u"Magneto-Optical", 
        22: u"DVD", 
        23: u"DVD-RW+", 
        24: u"DVD-RAM", 
        25: u"DVD-ROM", 
        26: u"DVD-Video", 
        27: u"Divx", 
        28: u"Floppy/Diskette", 
        29: u"Hard Disk", 
        30: u"Memory Card", 
        31: u"Hard Copy", 
        32: u"Clik Disk", 
        33: u"CD-RW", 
        34: u"CD-DA", 
        35: u"CD+", 
        36: u"DVD Recordable", 
        37: u"DVD-RW", 
        38: u"DVD-Audio", 
        39: u"DVD-5", 
        40: u"DVD-9", 
        41: u"DVD-10", 
        42: u"DVD-18", 
        43: u"Magneto-Optical Rewriteable", 
        44: u"Magneto-Optical Write Once", 
        45: u"Magneto-Optical Rewriteable (LIMDOW)", 
        46: u"Phase Change Write Once", 
        47: u"Phase Change Rewriteable", 
        48: u"Phase Change Dual Rewriteable", 
        49: u"Ablative Write Once", 
        50: u"Near Field Recording", 
        51: u"MiniQic", 
        52: u"Travan", 
        53: u"8mm Metal Particle", 
        54: u"8mm Advanced Metal Evaporate", 
        55: u"NCTP", 
        56: u"LTO Ultrium", 
        57: u"LTO Accelis", 
        58: u"9 Track Tape", 
        59: u"18 Track Tape", 
        60: u"36 Track Tape", 
        61: u"Magstar 3590", 
        62: u"Magstar MP", 
        63: u"D2 Tape", 
        64: u"Tape - DST Small", 
        65: u"Tape - DST Medium", 
        66: u"Tape - DST Large"
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)

def PhysicalMediaLabelFormats(dummy_context):
    terms = []
    for (gkey, gname) in {
          0: u"Barcode", 
          1: u"Radio Frequency Identification",
          2: u"OCR (Optical Character Recognition)",
          3: u"MICR (Magnetic Ink Character Recognition)",
          4: u"7 Character Barcode",
          5: u"9 Character Barcode"
        }.items():
        terms.append(SimpleTerm(gkey, str(gkey), gname))
    return SimpleVocabulary(terms)


class PhysicalMedia(PhysicalComponent):
    """
    the template instance
    """
    implements(IPhysicalMedia)
    shortName = "physical_media"
    # for ..Contained we have to:
    __name__ = __parent__ = None

    capacity = FieldProperty(IPhysicalMedia['capacity'])
    cleanerMedia = FieldProperty(IPhysicalMedia['cleanerMedia'])
    dualSided = FieldProperty(IPhysicalMedia['dualSided'])
    maxMounts = FieldProperty(IPhysicalMedia['maxMounts'])
    mediaSize = FieldProperty(IPhysicalMedia['mediaSize'])
    mediaType = FieldProperty(IPhysicalMedia['mediaType'])
    timeOfLastMount = FieldProperty(IPhysicalMedia['timeOfLastMount'])
    writeProtectOn = FieldProperty(IPhysicalMedia['writeProtectOn'])
    labelFormat = FieldProperty(IPhysicalMedia['labelFormat'])
    device = RelationPropertyIn(Devices_PhysicalMedia_RelManager)

    fullTextSearchFields = []
    fullTextSearchFields.extend(PhysicalComponent.fullTextSearchFields)
        

    def __init__(self, **data):
        """
        constructor of the object
        """
        PhysicalComponent.__init__(self, **data)
        refAttributeNames = getRefAttributeNames(PhysicalMedia)
        for (name, value) in data.items():
            if name in IPhysicalMedia.names() and \
               name not in refAttributeNames:
                setattr(self, name, value)
        self.ikRevision = __version__

    def getRefAttributeNames(self):
        return getRefAttributeNames(PhysicalMedia)

    def store_refs(self, **data):
        PhysicalComponent.store_refs(self, **data)
        refAttributeNames = self.getRefAttributeNames()
        for (name, value) in data.items():
            if name in refAttributeNames:
                setattr(self, name, value)


class PhysicalMediaFolder(ComponentFolder):
    implements(IPhysicalMediaFolder,
               IAddPhysicalMedia)
    contentFactory = PhysicalMedia
    shortName = "physical_media folder"

    def __init__(self, **data):
        """
        constructor of the object
        """
        ComponentFolder.__init__(self, **data)
