format xpdl-file:

this will make the xpdl-file from JPEd more human readable:
  xmllint --loaddtd --valid --format --output host_nagios_clean.xpdl host_nagios.xpdl

this will produce the python-file from xpdl:
  cog.py -r cog_host_nagios_xpdl.py
