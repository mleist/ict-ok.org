# [[[cog
#    import cog
#    cog.out("# Copyright (c) ")
# ]]]
# Copyright (c) 
# [[[end]]]

# [[[cog
#    import handyxml
#    for p in handyxml.xpath('host_nagios.xpdl', '//WorkflowProcesses/WorkflowProcess'):
#         cog.outl("WorkflowProcess:")
#         cog.outl("  ID: %s," % p.Id)
#         cog.outl("  Name: %s," % p.Name)
#         cog.outl("")
# ]]]
WorkflowProcess:
  ID: host_nagios1,
  Name: HostNagios,

# [[[end]]]

# [[[cog
#    import handyxml
#    for p in handyxml.xpath('host_nagios.xpdl', '//Applications/Application'):
#         cog.outl("Application:")
#         cog.outl("  ID: %s," % p.Id)
#         cog.outl("")
# ]]]
Application:
  ID: ict_ok_initialize,

Application:
  ID: ict_ok_start,

Application:
  ID: ict_ok_stop,

Application:
  ID: nagios_check,

Application:
  ID: nagios_trigger_online,

Application:
  ID: nagios_trigger_offline,

Application:
  ID: nagios_trigger_notif1,

# [[[end]]]

# [[[cog
#    import handyxml
#    for p in handyxml.xpath('host_nagios.xpdl', '//WorkflowProcesses/WorkflowProcess/Participants/Participant'):
#         cog.outl("Participant:")
#         cog.outl("  ID: %s," % p.Id)
#         cog.outl("  Name: %s," % p.Name)
#         cog.outl("")
# ]]]
Participant:
  ID: host_nagios1_par1,
  Name: ict_ok,

Participant:
  ID: host_nagios1_par2,
  Name: Nagios,

# [[[end]]]


# [[[cog
#    import handyxml
#    for p in handyxml.xpath('host_nagios.xpdl', '//WorkflowProcesses/WorkflowProcess/Activities/Activity'):
#         cog.outl("Activity:")
#         cog.outl("  ID: %s," % p.Id)
#         cog.outl("  Name: %s," % p.Name)
#         #cog.outl("  dir1: %s," % dir(p))
#         #cog.outl("  dir2: %s," % dir(p.node))
#         #cog.outl("  dir3: %s," % dir(p.childElements))
#         activity = p.node
#         implementation = activity.getElementsByTagName('Implementation')[:1]
#         if implementation:
#             tool = implementation[0].getElementsByTagName('Tool')[:1]
#             if tool:
#                 cog.outl("    Tool-Id: %s," % tool[0].getAttribute('Id'))
#                 cog.outl("    Tool-Type: %s," % tool[0].getAttribute('Type'))
#         performer = activity.getElementsByTagName('Performer')[:1]
#         if performer:
#             cog.outl("  Performer: %s" % performer[0]._get_firstChild()._get_nodeValue())
#         cog.outl("")
# ]]]
Activity:
  ID: initialize,
  Name: initialize,
    Tool-Id: ict_ok_initialize,
    Tool-Type: APPLICATION,
  Performer: host_nagios1_par1

Activity:
  ID: host_nagios1_act1,
  Name: Start Host,
    Tool-Id: ict_ok_start,
    Tool-Type: APPLICATION,
  Performer: host_nagios1_par1

Activity:
  ID: host_nagios1_act2,
  Name: Nagios Check,
    Tool-Id: nagios_check,
    Tool-Type: APPLICATION,
  Performer: host_nagios1_par2

Activity:
  ID: host_nagios1_act11,
  Name: Stop Host,
    Tool-Id: ict_ok_stop,
    Tool-Type: APPLICATION,
  Performer: host_nagios1_par1

Activity:
  ID: host_nagios1_act4,
  Name: Trigger online,
    Tool-Id: nagios_trigger_online,
    Tool-Type: APPLICATION,
  Performer: host_nagios1_par2

Activity:
  ID: host_nagios1_act5,
  Name: Trigger offline,
    Tool-Id: nagios_trigger_offline,
    Tool-Type: APPLICATION,
  Performer: host_nagios1_par2

Activity:
  ID: host_nagios1_act6,
  Name: Trigger notification1,
    Tool-Id: nagios_trigger_notif1,
    Tool-Type: APPLICATION,
  Performer: host_nagios1_par2

# [[[end]]]

