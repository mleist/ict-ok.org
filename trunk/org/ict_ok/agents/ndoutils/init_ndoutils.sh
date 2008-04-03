#!/bin/sh
#
# description: Starts and stops the Nagios Scanner
#

set -e

# Source LSB init functions
. /lib/lsb/init-functions

DAEMON=/opt/ict_ok.org/inst/lib/python/org/ict_ok/agents/ndoutils/ndoutils.sh
NAME=ndoutils
DESC="Nagios ndo daemon for ict-ok.org"
PIDFILE=/var/run/$NAME.pid

# Check whether the binary is still present:
test -f "$DAEMON" || exit 0




#test -x /opt/ndoutils/sbin/ndoutilsd || {
#	echo "Nagios not properly installed"
#	exit 1
#	}

#RETVAL=0


#start() {
#        KIND="Nessus"
#	echo -n $"Starting Nagios : "
#	/opt/ndoutils/sbin/ndoutilsd -D -q
#	echo "."
#	return 0
#}	

#stop() {
#	echo -n $"Shutting down Nagios : "
#	test -f /opt/ndoutils/var/ndoutils/ndoutilsd.pid && kill `cat /opt/ndoutils//var/ndoutils/ndoutilsd.pid`
#	echo "."
#	return 0
#}	

#restart() {
#	stop
#	sleep 3
#	start
#}	


case "$1" in
  start)
    log_daemon_msg "Starting $DESC" $NAME
    set +e
    pidofproc "$NAME" > /dev/null
    STATUS=$?
    set -e
    if [ "$STATUS" = 0 ]
    then
        log_progress_msg "already running"
        log_end_msg $STATUS
        exit $STATUS
    fi
    set +e
    start-stop-daemon --background --start --quiet --exec $DAEMON --oknodo \
        --pidfile $PIDFILE \
        | logger -p daemon.notice -t $NAME
    STATUS=$?
    set -e
    log_end_msg $STATUS
    exit $STATUS
    ;;
  stop)
    log_daemon_msg "Shutting down $DESC" $NAME

    set +e
    start-stop-daemon --oknodo --stop --quiet --pidfile /var/run/$NAME.pid --signal 15
    STATUS=$?
    set -e

    if [ "$STATUS" = 0 ]
    then
        rm -f $PIDFILE
    fi

    log_end_msg $STATUS
    exit $STATUS
    ;;
  restart)
	# Restart service (if running) or start service
	$0 stop
	$0 start
	;;
  *)
	echo $"Usage: $0 {start|stop|restart}"
	exit 1
esac

exit $?
