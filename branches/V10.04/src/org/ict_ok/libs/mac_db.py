# -*- coding: utf-8 -*-
#
# Copyright (c) 2009
#               Sebastian Napiorkowski
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# pylint: disable-msg=E1101
#
"""MacDB to get organization"""

__version__ = "$Id$"


from BTrees.IOBTree import IOBTree
import os
import re


class MacDB():
    def __init__(self):
        ouiPath = os.getenv("ICT_OUI_PATH")
        if ouiPath is not None:
            f = open(ouiPath, "r") #oui: http://standards.ieee.org/regauth/oui/oui.txt
        else:
            f = open("src/org/ict_ok/libs/oui.txt", "r") #oui: http://standards.ieee.org/regauth/oui/oui.txt
        self._data = IOBTree()
        last_mac = None
        EOF = False
        re_mac = re.compile(r"[A-F0-9]*\-[A-F0-9]*\-[A-F0-9]*")
        while not EOF:
            line = f.readline()
            if re.match(re_mac, line):
                last_mac = int(line[:8].replace("-", ""), 16)
                index = line.rfind("\t")+len("\t")
                org = line[index:].strip()
                self._data[last_mac] = {"short": org, "other":[]}
            elif last_mac != None:
                index = line.rfind("\t")
                if index != -1:
                    index += len("\t")
                    other = line[index:].strip()
                    self._data[last_mac]["other"].append(other)
                if (line == "\n"):
                    country_index = len(self._data[last_mac]["other"])-1 #last element
                    self._data[last_mac]["country"] = self._data[last_mac]["other"][country_index]
                    del self._data[last_mac]["other"][country_index]
            if line == '':
                EOF=True
        f.close()


    def getOrganization(self, mac_string):
        mac = mac_string[:8].replace(":", "")
        mac = mac.replace("-", "")
        int_mac = int(mac, 16)
        try:
            ret = self._data[int_mac]
        except KeyError:
            ret = None
        return ret


#macUtil = MacDB()
#mac_list = ["00:04:75:d5:2f:11 ", "00:11:2f:77:f6:ef", "00:11:2f:77:f6:ef", "00:50:56:c0:00:01", "00:0d:88:53:3a:4e", "00:1e:8c:7c:7c:97",  "00:1b:21:0f:f6:8e"]
#for mac in mac_list:
#    print macUtil.getOrganization(mac)
