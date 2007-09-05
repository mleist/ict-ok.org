# -*- coding: utf-8 -*-
#
# Copyright (c) 2004, 2005, 2006, 2007,
#               Markus Leist <leist@ikom-online.de>
# See also LICENSE.txt or http://www.ict-ok.org/LICENSE
# This file is part of ict-ok.org.
#
# $Id$
#
# no_pylint: disable-msg=E1101,E0611,C0301
#
"""Configuration adapter for demo1-config files
"""

__version__ = "$Id$"

# phython imports
from pprint import pprint

# zope imports
from zope.interface import implements

# ict_ok.org imports
from org.ict_ok.admin_utils.netscan.scanner import \
     Scanner
from org.ict_ok.admin_utils.netscan.demo1.interfaces import \
     IAdmUtilDemo1


class AdmUtilDemo1(Scanner):
    """Implementation of demo1 scanner wrapper
    """

    implements(IAdmUtilDemo1)

    def __init__(self):
        Scanner.__init__(self)
        self.ikRevision = __version__

    def buildDataDict( self):
        """
        fill our data dictonary
        """
        resultList = [
            # host 1
            {
                'hostname': u'win-xp-1',
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.',
                        'ipAddressType': u'ipv4',
                        'services': [
                            # port p22
                            {
                                'port': u'p22',
                                'service': u'ssh',
                            }
                            ],
                    }
                    ],

                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ]
         },

            # Router
            {
                'hostname': u'router01',
                'description': u'Router',
                'manufacturer': u'Cisco',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'Zentrale',
                'hardware': u'Cisco 2800',
                'user': u'',
                'inv_id': u'1441213',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.1',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Server (Linux) virtual Machines 1
            {
                'hostname': u'srv1',
                'description': u'Server (Linux) virtual Machines 1',
                'manufacturer': u'IBM',
                'vendor': u'IBM Deutschland GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.2',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Nameserver (Linux) auf Server virtual Machines 1
            {
                'hostname': u'dns1',
                'description': u'Nameserver (Linux) auf Server virtual Machines 1',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.20',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Mailserver (Linux) auf Server virtual Machines 1
            {
                'hostname': u'mail1',
                'description': u'Mailserver (Linux) auf Server virtual Machines 1',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.21',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Fileserver (Linux) auf Server virtual Machines 1
            {
                'hostname': u'file1',
                'description': u'Fileserver (Linux) auf Server virtual Machines 1',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.22',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Oracle-DB (Linux) auf Server virtual Machines 1
            {
                'hostname': u'ora1',
                'description': u'Oracle-DB (Linux) auf Server virtual Machines 1',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.23',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # SQL-DB (Linux) auf Server virtual Machines 1
            {
                'hostname': u'db1',
                'description': u'SQL-DB (Linux) auf Server virtual Machines 1',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.24',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # HTTP-Server (Linux) auf Server virtual Machines 1
            {
                'hostname': u'web1',
                'description': u'HTTP-Server (Linux) auf Server virtual Machines 1',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.25',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Applikationserver (Linux) auf Server virtual Machines 1
            {
                'hostname': u'app1',
                'description': u'Applikationserver (Linux) auf Server virtual Machines 1',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.26',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Server (Linux) virtual Machines 2
            {
                'hostname': u'srv2',
                'description': u'Server (Linux) virtual Machines 2',
                'manufacturer': u'IBM',
                'vendor': u'IBM Deutschland GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.3',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Nameserver (Linux) auf Server virtual Machines 2
            {
                'hostname': u'dns2',
                'description': u'Nameserver (Linux) auf Server virtual Machines 2',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.30',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Mailserver (Linux) auf Server virtual Machines 2
            {
                'hostname': u'mail2',
                'description': u'Mailserver (Linux) auf Server virtual Machines 2',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.31',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Fileserver (Linux) auf Server virtual Machines 2
            {
                'hostname': u'file2',
                'description': u'Fileserver (Linux) auf Server virtual Machines 2',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.32',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Oracle-DB (Linux) auf Server virtual Machines 2
            {
                'hostname': u'ora2',
                'description': u'Oracle-DB (Linux) auf Server virtual Machines 2',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.33',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # SQL-DB (Linux) auf Server virtual Machines 2
            {
                'hostname': u'db2',
                'description': u'SQL-DB (Linux) auf Server virtual Machines 2',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.34',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # HTTP-Server (Linux) auf Server virtual Machines 2
            {
                'hostname': u'web2',
                'description': u'HTTP-Server (Linux) auf Server virtual Machines 2',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.35',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Applicationserver (Linux) auf Server virtual Machines 2
            {
                'hostname': u'app2',
                'description': u'Applicationserver (Linux) auf Server virtual Machines 2',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.36',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
            
            # Server (Linux) virtual Machines 3
            {
                'hostname': u'srv3',
                'description': u'Server (Linux) virtual Machines 3',
                'manufacturer': u'IBM',
                'vendor': u'IBM Deutschland GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.4',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Nameserver (Linux) auf Server virtual Machines 3
            {
                'hostname': u'name3',
                'description': u'Nameserver (Linux) auf Server virtual Machines 3',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.40',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Mailserver (Linux) auf Server virtual Machines 3
            {
                'hostname': u'mail3',
                'description': u'Mailserver (Linux) auf Server virtual Machines 3',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.41',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Fileserver (Linux) auf Server virtual Machines 3
            {
                'hostname': u'file3',
                'description': u'Fileserver (Linux) auf Server virtual Machines 3',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.42',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Oracle-DB (Linux) auf Server virtual Machines 3
            {
                'hostname': u'ora3',
                'description': u'Oracle-DB (Linux) auf Server virtual Machines 3',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.43',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # SQL-DB (Linux) auf Server virtual Machines 3
            {
                'hostname': u'db3',
                'description': u'SQL-DB (Linux) auf Server virtual Machines 3',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.44',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # HTTP-Server (Linux) auf Server virtual Machines 3
            {
                'hostname': u'web3',
                'description': u'HTTP-Server (Linux) auf Server virtual Machines 3',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.45',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Applicationserver (Linux) auf Server virtual Machines 3
            {
                'hostname': u'app3',
                'description': u'Applicationserver (Linux) auf Server virtual Machines 3',
                'manufacturer': u'VmWare',
                'vendor': u'VmWare',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.46',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Speicherserver (Linux)
            {
                'hostname': u'san1',
                'description': u'Speicherserver (Linux)',
                'manufacturer': u'IBM',
                'vendor': u'IBM Deutschland GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.5',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Thermometer 1
            {
                'hostname': u'therm1',
                'description': u'Thermometer 1',
                'manufacturer': u'Allnet',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.6',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Thermometer 2
            {
                'hostname': u'therm2',
                'description': u'Thermometer 2',
                'manufacturer': u'Allnet',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.7',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Luftfeuchtigkeitsmesser 1
            {
                'hostname': u'hygro1',
                'description': u'Luftfeuchtigkeitsmesser 1',
                'manufacturer': u'Allnet',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.8',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Luftfeuchtigkeitsmesser 2
            {
                'hostname': u'hygro2',
                'description': u'Luftfeuchtigkeitsmesser 2',
                'manufacturer': u'Allnet',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.9',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # HP 4250 N Laserdrucker
            {
                'hostname': u'hp-4250-a1',
                'description': u'HP 4250 N Laserdrucker',
                'manufacturer': u'HP',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Hauptgebäude',
                'room': u'A1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.10',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # HP 5550 DN Farblaserdrucker
            {
                'hostname': u'hp-5550-a1',
                'description': u'HP 5550 DN Farblaserdrucker',
                'manufacturer': u'HP',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Hauptgebäude',
                'room': u'A1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.11',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
            
            # HP 4250 N Laserdrucker
            {
                'hostname': u'hp-4250-b22',
                'description': u'HP 4250 N Laserdrucker',
                'manufacturer': u'HP',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Produktion',
                'room': u'B22',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.12',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                        
            # HP 4250 N Laserdrucker
            {
                'hostname': u'hp-4250-a4',
                'description': u'HP 4250 N Laserdrucker',
                'manufacturer': u'HP',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Service-Center',
                'room': u'A4',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.13',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                        
            # HP 4250 N Laserdrucker
            {
                'hostname': u'hp-4250-b1',
                'description': u'HP 4250 N Laserdrucker',
                'manufacturer': u'HP',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 1 Service Center',
                'room': u'B1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.14',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                        
            # HP 4250 N Laserdrucker
            {
                'hostname': u'hp-4250-b2',
                'description': u'HP 4250 N Laserdrucker',
                'manufacturer': u'HP',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 2 Service Center',
                'room': u'B2',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.15',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                        
            # HP 4250 N Laserdrucker
            {
                'hostname': u'hp-4250-b3',
                'description': u'HP 4250 N Laserdrucker',
                'manufacturer': u'HP',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 3 Service Center',
                'room': u'B3',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.16',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                        
            # HP 4250 N Laserdrucker
            {
                'hostname': u'hp-4250-b4',
                'description': u'HP 4250 N Laserdrucker',
                'manufacturer': u'HP 4250 N Laserdrucker',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 4 Service Center',
                'room': u'B4',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.17',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                        
            # Cisco Telefonanlage
            {
                'hostname': u'cisco-e1',
                'description': u'Cisco Telefonanlage',
                'manufacturer': u'Cisco',
                'vendor': u'Mercateo',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.18',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Alarmzentrale
            {
                'hostname': u'securita',
                'description': u'Alarmzentrale',
                'manufacturer': u'Securita',
                'vendor': u'Securita GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.19',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Klimaanlage
            {
                'hostname': u'klima',
                'description': u'Klimaanlage',
                'manufacturer': u'Sutzenbach GmbH',
                'vendor': u'Sutzenbach GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Hauptgebäude technische Zentrale',
                'room': u'E1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.51',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
            
            # Workstation 1 Windows XP
            {
                'hostname': u'win-xp-1',
                'description': u'Workstation 1 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Hauptgebäude',
                'room': u'A1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.100',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 2 Windows XP
            {
                'hostname': u'win-xp-2',
                'description': u'Workstation 2 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Hauptgebäude',
                'room': u'A1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.101',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 3 Windows XP
            {
                'hostname': u'win-xp-3',
                'description': u'Workstation 3 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Hauptgebäude',
                'room': u'A1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.102',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 4 Windows XP
            {
                'hostname': u'win-xp-4',
                'description': u'Workstation 4 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Produktion',
                'room': u'B22',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.103',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 5 Windows XP
            {
                'hostname': u'win-xp-5',
                'description': u'Workstation 5 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Produktion',
                'room': u'B22',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.104',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 6 Windows XP
            {
                'hostname': u'win-xp-6',
                'description': u'Workstation 6 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Service-Center',
                'room': u'A4',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.105',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 7 Windows XP
            {
                'hostname': u'win-xp-7',
                'description': u'Workstation 7 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Sekretariat Service-Center',
                'room': u'A4',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.106',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 8 Windows XP
            {
                'hostname': u'win-xp-8',
                'description': u'Workstation 8 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 1 Service Center',
                'room': u'B1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.107',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 9 Windows XP
            {
                'hostname': u'win-xp-9',
                'description': u'Workstation 9 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 1 Service Center',
                'room': u'B1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.108',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 10 Windows XP
            {
                'hostname': u'win-xp-10',
                'description': u'Workstation 10 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 1 Service Center',
                'room': u'B1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.109',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 11 Windows XP
            {
                'hostname': u'win-xp-11',
                'description': u'Workstation 11 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 1 Service Center',
                'room': u'B1',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.110',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 12 Windows XP
            {
                'hostname': u'win-xp-12',
                'description': u'Workstation 12 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 2 Service Center',
                'room': u'B2',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.111',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 13 Windows XP
            {
                'hostname': u'win-xp-13',
                'description': u'Workstation 13 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 2 Service Center',
                'room': u'B2',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.112',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 14 Windows XP
            {
                'hostname': u'win-xp-14',
                'description': u'Workstation 14 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 2 Service Center',
                'room': u'B2',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.113',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 15 Windows XP
            {
                'hostname': u'win-xp-15',
                'description': u'Workstation 15 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 2 Service Center',
                'room': u'B2',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.114',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 16 Windows XP
            {
                'hostname': u'win-xp-16',
                'description': u'Workstation 16 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 3 Service Center',
                'room': u'B3',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.115',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 17 Windows XP
            {
                'hostname': u'win-xp-17',
                'description': u'Workstation 17 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 3 Service Center',
                'room': u'B3',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.116',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 18 Windows XP
            {
                'hostname': u'win-xp-18',
                'description': u'Workstation 18 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 3 Service Center',
                'room': u'B3',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.117',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 19 Windows XP
            {
                'hostname': u'win-xp-19',
                'description': u'Workstation 19 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 3 Service Center',
                'room': u'B3',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.118',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 20 Windows XP
            {
                'hostname': u'win-xp-20',
                'description': u'Workstation 20 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 4 Service Center',
                'room': u'B4',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.119',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 21 Windows XP
            {
                'hostname': u'win-xp-21',
                'description': u'Workstation 21 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 4 Service Center',
                'room': u'B4',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.120',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 22 Windows XP
            {
                'hostname': u'win-xp-22',
                'description': u'Workstation 22 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 4 Service Center',
                'room': u'B4',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.121',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },
                
            # Workstation 23 Windows XP
            {
                'hostname': u'win-xp-23',
                'description': u'Workstation 23 Windows XP',
                'manufacturer': u'DeLL',
                'vendor': u'HTP Computer GmbH',
                'workinggroup': u'',
                'hardware': u'',
                'user': u'',
                'inv_id': u'',
                'building': u'Team 4 Service Center',
                'room': u'B4',
                'oss': [
                    {
                        'type': u'os_type',
                        'vendor': u'os_vendor',
                        'osfamily': u'os_family',
                        'osgen': u'os_gen',
                        'accuracy': u'os_accuracy',
                        },
                    ],
                'interfaces': [
                    {
                        'nbr': u'01',
                        'name': u'Port 01',
                        'netType': u'ethernet',
                        'macAddress': u'00:08:00:01:02:01',
                        'ipAddress': u'192.168.0.122',
                        'ipAddressType': u'ipv4',
                        'services': [
                            ],
                    }
                    ],
         },

        
        ]
        return resultList
        
        
        
        
        
        
    def startScan(self, networkObj):
        """
        fills the network object with data
        """
        #ipAddress = networkObj.ipv4
        dataDict = self.buildDataDict()
        self.createObjects( dataDict, networkObj)
        pprint( dataDict)
