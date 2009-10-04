We will use cog from
http://www.nedbatchelder.com/code/cog/
for genereration of the source-code.

ok, let's look, what is to do:

1. svn checkout cog_templates
2. svn cp org/ict_ok/cog_templates/components/service org/ict_ok/components/service/special/[filename]
3. edit org/ict_ok/components/service/special/[filename]/props.py
4. make gen
5. test it
6. make clean
7. check in
