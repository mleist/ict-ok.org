# -*- coding: utf-8 -*-
#
# Copyright (c) 2009, 
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E0213,W0232
#
"""Interface of PhysicalMedia"""


__version__ = "$Id$"

# zope imports
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.schema import Choice, Int, List, TextLine, Bool, Float, Datetime
from zope.app.folder.interfaces import IFolder

_ = MessageFactory('org.ict_ok')


class IPhysicalMedia(Interface):
    """A PhysicalMedia object."""

    capacity = Int(
        title = _(u'Capacity'),
        description = _(u"The number of bytes that can be read from or written to a Media."),
        required = False)
        
    cleanerMedia = Bool(
        title = _(u'Cleaner media'),
        description = _(u"Indicating that the PhysicalMedia is used for cleaning purposes and not data storage."),
        required = False)
        
    dualSided = Bool(
        title = _(u'Dual sided'),
        description = _(u"Indicating that the Media has two recording sides (TRUE) or only a single side (FALSE)."),
        required = False)
        
    maxMounts = Int(
        title = _(u'Max mounts'),
        description = _(u"For removable Media, the maximum number of times that the Media can be mounted before it should be retired. For cleaner Media, this is the maximum number of Drive cleans that can be performed. For nonremovable Media, such as hard disks, this property is not applicable and should be set to 0."),
        required = False)
        
    mediaSize = Float(
        title = _(u'Media size'),
        description = _(u"Size of the Media in inches."),
        required = False)
        
    mediaType = Choice(
        title = _(u'Media Type'),
        description = _(u"Specifies the type of the PhysicalMedia."),
        required = False,
        vocabulary = "PhysicalMediaMediaTypes")

    timeOfLastMount = Datetime(
        title = _(u'Time of last mount'),
        description = _(u"For removable or cleaner Media, the date and time that the Media was last mounted. For nonremovable Media, such as hard disks, this property has no meaning and is not applicable."),
        required = False)
        
    writeProtectOn = Bool(
        title = _(u'Write protect on'),
        description = _(u"Specifying whether the Media is currently write protected by some kind of physical mechanism, such as a protect tab on a floppy diskette."),
        required = False)
        
    labelFormat = Choice(
        title = _(u'Label Format'),
        description = _(u"The formats of each of the labels on a PhysicalMedia."),
        required = False,
        vocabulary = "PhysicalMediaLabelFormats")

    device = Choice(
        title = _(u'Device'),
        vocabulary = 'AllDevices',
        required = False)
        
    def trigger_online():
        """
        trigger workflow
        """


class IPhysicalMediaFolder(Interface):
    """Container for PhysicalMedia objects
    """


class IAddPhysicalMedia(Interface):
    """Interface for all Objects"""
    template = Choice(
        title = _("Template"),
        vocabulary="AllPhysicalMediaTemplates",
        required = False)
