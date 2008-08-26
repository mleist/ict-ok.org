# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007, 2008,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101,E0611,W0612
#
"""implementation of IP valid schema
"""

__version__ = "$Id$"

# python imports

# zope imports
from zope.component import adapts

# z3c imports
from z3c.form.converter import DatetimeDataConverter
from z3c.form import interfaces

# ict_ok.org imports
from org.ict_ok.schema.interfaces import IIctDatetime


class IctDatetimeDataConverter(DatetimeDataConverter):
    """A special ict data converter for datetimes."""
    adapts(IIctDatetime, interfaces.IWidget)
    type = 'dateTime'
    length = 'full'

    def __init__(self, field, widget):
        super(IctDatetimeDataConverter, self).__init__(field, widget)
        #locale = self.widget.request.locale
        #self.formatter = locale.dates.getFormatter(self.type, self.length)

    def toWidgetValue(self, value):
        """See interfaces.IDataConverter"""
        from pytz import timezone
        if value is self.field.missing_value:
            return u''
        if value.utcoffset() is None:
            berlinTZ = timezone('Europe/Berlin')
            tmpValue = berlinTZ.fromutc(value)
            return self.formatter.format(tmpValue)
        return self.formatter.format(value)
