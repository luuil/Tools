#!/bin/sh
usage() {
  echo 'usage: d(ocker) [p(ps)|a(attach)|l(logs)|t(ail_logs)|s(top)|r(estart)|i(nspect)]'
  echo '  ps'
  echo '  attach {id}'
  echo '  logs {id}'
  echo '  tail_logs {id}'
  echo '  stop {id}'
  echo '  restart {id}'
  echo '  inspect {id}'
}
if [ $# -eq 0 ]
then
  usage
elif [ "$1" = "p" -o "$1" = "ps" ]
then
  if [ $# -ge 2 ]
  then
    echo "docker ps $2"
    docker ps $2
  else
    echo "docker ps"
    docker ps
  fi
elif [ "$1" = "a" -o "$1" = "attach" ]
then
  echo "docker exec -i -t $2 //bin/bash"
  docker exec -i -t $2 //bin/bash
elif [ "$1" = "s" -o "$1" = "stop" ]
then
  echo "docker stop $2"
  docker stop $2
elif [ "$1" = "r" -o "$1" = "restart" ]
then
  echo "docker restart $2"
  docker restart $2
elif [ "$1" = 'l' -o "$1" = "logs" ]
then
  echo "docker logs $2"
  docker logs $2
elif [ "$1" = 't' -o "$1" = "tail_logs" ]
then
  echo "tail -f `docker inspect --format='{{.LogPath}}' $2`"
  tail -f `docker inspect --format='{{.LogPath}}' $2`
elif [ "$1" = 'i' -o "$1" = "inspect" ]
then
  echo "docker inspect --format='{{.LogPath}}' $2"
  docker inspect --format='{{.LogPath}}' $2
else
  # all arguments except the first one (in a bash script)
  # will support docker shortcut `dk`
  echo "docker ${@:1}"
  docker ${@:1}
fi
exit 0
