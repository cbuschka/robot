#!/bin/bash

SCRIPT_DIR=$(cd `dirname "$0"` && pwd -P)
SCRIPT=${SCRIPT_DIR}/$(basename "$0")

function get_server_pid() {
  ps -ef | grep -v ps | grep "python3" | grep "server.py" | awk '{ print $2 }'
}

case $1 in
  stop)
    pid=$(get_server_pid)
    if [ ! -z "${pid}" ]; then
      echo "Killing ${pid}."
      kill -TERM ${pid}
    fi
  ;;
  status)
    pid=$(get_server_pid)
    if [ ! -z "${pid}" ]; then
      echo "Running as pid ${pid}."
    else
      echo "Not running." 
    fi
  ;;
  run)
    ${SCRIPT} stop
    python3 server.py 8000
  ;;
  start|restart)
    ${SCRIPT} stop
    cd ${SCRIPT_DIR}
    python3 server.py 8000 &
  ;;
  *)
    echo "$0 status|start|stop|restart|run"
    exit 1
  ;;
esac
