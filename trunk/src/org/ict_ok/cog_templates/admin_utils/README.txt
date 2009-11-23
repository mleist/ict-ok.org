We will use cog from
http://www.nedbatchelder.com/code/cog/
for genereration of the source-code.

ok, let's look, what is to do:

1. svn checkout cog_templates
2. svn cp cog_templates/admin_utils admin_utils/[filename]
3. edit admin_utils/[filename]/props.py
4. make gen
5. rename admin_utils/[filename]/cog_template.py to admin_utils/[filename]/[filename].py
6. same for admin_utils/[filename]/browser/cog_template.py
7. test it
8. check in
