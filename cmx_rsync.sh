#!/usr/bin/bash

# /usr/bin/su

PORT="-p nnn"
PORT=""
SOURCE="/.../CumulusMX/web/"
SERVER="account@your.hosting.com"
DEST="/target/server/dir"

/usr/bin/rsync -a -e "ssh ${PORT}" ${SOURCE} ${SERVER}:${DEST} 2> /dev/null > /dev/null
# /usr/bin/rsync -v -a -e "ssh ${PORT}" ${SOURCE} ${SERVER}:${DEST} >> ${LOG} 2>&1

exit






# Knowing CumulusMX is running under root, I tried invoking this command as:
#     DailyProgram=su
#     ExternalParams=-c "/home/pi/cmxaux/cmx_rsync.sh" - pi > /dev/null
#
# Which resulting tons of these in journalctl:
#   Dec 26 19:13:00 wx-pi su[11943]: (to pi) root on none
#   Dec 26 19:13:00 wx-pi su[11943]: pam_unix(su-l:session): session opened for user pi by (uid=0)
#   Dec 26 19:14:00 wx-pi su[11967]: (to pi) root on none
#   Dec 26 19:14:00 wx-pi su[11967]: pam_unix(su-l:session): session opened for user pi by (uid=0)
#   Dec 26 19:15:00 wx-pi su[11998]: (to pi) root on none
#   Dec 26 19:15:00 wx-pi su[11998]: pam_unix(su-l:session): session opened for user pi by (uid=0)
# I could not find a way to silence these.
#
#
# The alternative was to run ssh-keypass under root, and add the public key to the server.
# Probably not the most secure
# After that, this seems to work fine:
#     DailyProgram=/home/pi/cmxaux/cmx_rsync.sh
#     ExternalParams=
#


