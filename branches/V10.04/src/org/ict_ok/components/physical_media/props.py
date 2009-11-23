#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#

authors = [
   {r'name': r'Markus Leist',
    r'email': r'leist@ikom-online.de'},
    ]

filename = r'physical_media'
longpath = r'org.ict_ok.components'
longpath_interface = longpath + r'.%s.interfaces' % (filename)
longpath_file = longpath + r'.%s.%s' % (filename, filename)
longpath_browser_file = longpath + r'.%s.browser.%s' % (filename, filename)
additionalClassImports = []

moduletitle = r'Physical Media'
componentname = r'PhysicalMedia'
#servicename = r'Test'
#serviceport = 65533
#utilityname = r'AdmUtil' + modulename
#loggername = r'AdmUtil' + modulename
#servicetitle = r'%s Service' % servicename

purpose = r"""Physical media component

The PhysicalMedia class represents any type of documentation or
storage medium, such as tapes, CDROMs, etc.
"""

attrDict = {
    'attr1': 'TextLine',
    'attr2': 'Choice',
    'attr3': 'Date',
    }

attrTuples = [
    # (varName, schema, displayName, displayDescription)

    ('capacity', 'Int', u'Capacity', u'The number of bytes that can be read from or written to a Media.'),
    #Capacity	uint64	
    #Description	string	The number of bytes that can be read from or written to a Media. This property is not applicable to "Hard Copy" (documentation) or cleaner Media. Data compression should not be assumed, as it would increase the value in this property. For tapes, it should be assumed that no filemarks or blank space areas are recorded on the Media.
    #Units	string	Bytes
    #

    ('cleanerMedia', 'Bool', u'Cleaner media', u'Indicating that the PhysicalMedia is used for cleaning purposes and not data storage.'),
    #CleanerMedia	boolean	
    #Description	string	Boolean indicating that the PhysicalMedia is used for cleaning purposes and not data storage.
    #

    ('dualSided', 'Bool', u'Dual sided', u'Indicating that the Media has two recording sides (TRUE) or only a single side (FALSE).'),
    #DualSided	boolean	
    #Description	string	Boolean indicating that the Media has two recording sides (TRUE) or only a single side (FALSE). Examples of dual sided Media include DVD-ROM and some optical disks. Examples of single sided Media are tapes and CD-ROM.
    #

    ('maxMounts', 'Int', u'Max mounts', u'For removable Media, the maximum number of times that the Media can be mounted before it should be retired. For cleaner Media, this is the maximum number of Drive cleans that can be performed. For nonremovable Media, such as hard disks, this property is not applicable and should be set to 0.'),
    #MaxMounts	uint64	
    #Description	string	For removable Media, the maximum number of times that the Media can be mounted before it should be retired. For cleaner Media, this is the maximum number of Drive cleans that can be performed. For nonremovable Media, such as hard disks, this property is not applicable and should be set to 0.
    #
    #MediaDescription	string	
    #Description	string	Additional detail related to the MediaType enumeration. For example, if value 3 ("QIC Cartridge") is specified, this property could indicate whether the tape is wide or 1/4 inch, whether it is pre-formatted, whether it is Travan compatible, etc.
    #

    ('mediaSize', 'Float', u'Media size', u'Size of the Media in inches.'),
    #ModelCorrespondence	string	CIM_PhysicalMedia.MediaType
    #MediaSize	real32	
    #Description	string	Size of the Media in inches. For example, '3.5' would be entered for a 3.5 inch disk, or '12' would be entered for a 12 inch optical disk. On the other hand, '0.5' would be defined for a 1/2 inch tape.
    #Units	string	Inches
    #

    ('mediaType', 'Choice', u'Media Type', u'Specifies the type of the PhysicalMedia.'),
    #MediaType	uint16	
    #Description	string	Specifies the type of the PhysicalMedia, as an enumerated integer. The MediaDescription property is used to provide more explicit definition of the Media type, whether it is pre-formatted, compatability features, etc.
    #ModelCorrespondence	string	CIM_PhysicalMedia.MediaDescription
    #ValueMap	string	0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66
    #Values	string	Unknown, Other, Tape Cartridge, QIC Cartridge, AIT Cartridge, DTF Cartridge, DAT Cartridge, 8mm Tape Cartridge, 19mm Tape Cartridge, DLT Cartridge, Half-Inch Magnetic Tape Cartridge, Cartridge Disk, JAZ Disk, ZIP Disk, SyQuest Disk, Winchester Removable Disk, CD-ROM, CD-ROM/XA, CD-I, CD Recordable, WORM, Magneto-Optical, DVD, DVD-RW+, DVD-RAM, DVD-ROM, DVD-Video, Divx, Floppy/Diskette, Hard Disk, Memory Card, Hard Copy, Clik Disk, CD-RW, CD-DA, CD+, DVD Recordable, DVD-RW, DVD-Audio, DVD-5, DVD-9, DVD-10, DVD-18, Magneto-Optical Rewriteable, Magneto-Optical Write Once, Magneto-Optical Rewriteable (LIMDOW), Phase Change Write Once, Phase Change Rewriteable, Phase Change Dual Rewriteable, Ablative Write Once, Near Field Recording, MiniQic, Travan, 8mm Metal Particle, 8mm Advanced Metal Evaporate, NCTP, LTO Ultrium, LTO Accelis, 9 Track Tape, 18 Track Tape, 36 Track Tape, Magstar 3590, Magstar MP, D2 Tape, Tape - DST Small, Tape - DST Medium, Tape - DST Large
    #
    #MountCount	uint64	
    #Counter	boolean	true
    #Description	string	For removable or cleaner Media, the number of times that the Media has been mounted for data transfer or to clean a Drive. For nonremovable Media, such as hard disks, this property is not applicable and should be set to 0.
    #ModelCorrespondence	string	CIM_PhysicalMedia.MaxMounts
    #

    ('timeOfLastMount', 'Datetime', u'Time of last mount', u'For removable or cleaner Media, the date and time that the Media was last mounted. For nonremovable Media, such as hard disks, this property has no meaning and is not applicable.'),
    #TimeOfLastMount	datetime	
    #Description	string	For removable or cleaner Media, the date and time that the Media was last mounted. For nonremovable Media, such as hard disks, this property has no meaning and is not applicable.
    #
    #TotalMountTime	uint64	
    #Description	string	For removable or cleaner Media, the total time (in seconds) that the Media has been mounted for data transfer or to clean a Drive. For nonremovable Media, such as hard disks, this property is not applicable and should be set to 0.
    #Units	string	Seconds
    #

    ('writeProtectOn', 'Bool', u'Write protect on', u'Specifying whether the Media is currently write protected by some kind of physical mechanism, such as a protect tab on a floppy diskette.'),
    #WriteProtectOn	boolean	
    #Description	string	Boolean specifying whether the Media is currently write protected by some kind of physical mechanism, such as a protect tab on a floppy diskette.
    #

    ('labelFormat', 'Choice', u'Label Format', u'The formats of each of the labels on a PhysicalMedia.'),
    #LabelFormats	uint16[]	
    #ArrayType	string	Indexed
    #Description	string	An array of enumerated integers describing the formats of each of the labels on a PhysicalMedia. The Labels themselves are listed in the PhysicalLabels property. Note, each entry of this array is related to the entry in PhysicalLabels that is located at the same index.
    #ModelCorrespondence	string	CIM_PhysicalMedia.PhysicalLabels
    #ValueMap	string	0, 1, 2, 3, 4, 5
    #Values	string	Barcode, Radio Frequency Identification, OCR (Optical Character Recognition), MICR (Magnetic Ink Character Recognition), 7 Character Barcode, 9 Character Barcode
    #
    #LabelStates	uint16[]	
    #ArrayType	string	Indexed
    #Description	string	An array of enumerated integers describing the states of each of the labels on a PhysicalMedia. The Labels themselves are listed in the PhysicalLabels property. Note, each entry of this array is related to the entry in PhysicalLabels that is located at the same index.
    #ModelCorrespondence	string	CIM_PhysicalMedia.PhysicalLabels
    #ValueMap	string	0, 1, 2
    #Values	string	OK/Readable, Unreadable, Upside Down
    #
    #PhysicalLabels	string[]	
    #ArrayType	string	Indexed
    #Description	string	One or more strings on 'labels' on the PhysicalMedia. The format of the labels and their state (readable, unreadable, upside-down) are indicated in the LabelFormats and LabelStates array properties.
    #ModelCorrespondence	string	CIM_PhysicalMedia.LabelStates, CIM_PhysicalMedia.LabelFormats

    ]


# '1'-part of the '1..n'-relation 
connInTuples = []

# 'n'-part of the '1..n'-relation 
connOutTuples = []

#connOutTuples.append(('contactItems', u'Contact Items', 'ContactItem')) # other mul
connInTuples.append(('device', u'Device', 'Device'))  # mul 1


# '1'-part of the '1..n'-relation 
#additionalClassImports.append('from org.ict_ok.components.interface.interface import Interface_IpAddresses_RelManager')
#additionalClassImports.append('from org.ict_ok.components.interface.interfaces import IInterface')
#additionalClassImports.append('from org.ict_ok.components.ipnet.ipnet import IpNet_IpAddresses_RelManager')
#additionalClassImports.append('from org.ict_ok.components.ipnet.interfaces import IIpNet')
additionalClassImports.append('from org.ict_ok.components.device.device import Devices_PhysicalMedia_RelManager')
additionalClassImports.append('from org.ict_ok.components.device.interfaces import IDevice')


# 'n'-part of the '1..n'-relation 
#additionalClassImports.append('from org.ict_ok.components.patchpanel.interfaces import IPatchPanel')
#additionalClassImports.append('from org.ict_ok.components.contact_item.interfaces import IContactItem')

copyrights = [2009]

if __name__=="__main__":
    print filename + ".py"
