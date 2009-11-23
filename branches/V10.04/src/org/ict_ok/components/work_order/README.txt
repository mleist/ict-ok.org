We will use cog from
http://www.nedbatchelder.com/code/cog/
for genereration of the source-code.

ok, let's look, what is to do:

1. svn checkout cog_templates
2. svn cp org/ict_ok/cog_templates/components/template org/ict_ok/components/[filename]
3. edit org/ict_ok/components/[filename]/props.py
4. make rename
5. make gen
6. test it
7. make cogclean
8. check in
