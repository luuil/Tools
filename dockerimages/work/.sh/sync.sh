#!/bin/bash

function sync() {
  printf "[$1]: syncing...\n"
  rsync -azP --exclude='~/.sh/sync.sh' ~/.sh/ $1:~/.sh
  rsync -azP ~/.ssh/config $1:~/.ssh/
  alter_or_not=`ssh -t $1 "cat ~/.bashrc | grep bashrc_append"`
  if [ -n "$alter_or_not" ]; then
    printf "[$1]: synced already\n\n"
  else
    printf "[$1]: append 'source ~/.sh/.bashrc_append' to '~/.bashrc'\n\n"
    ssh -t $1 "sed -i '\$a # my bashrc\nsource ~/.sh/.bashrc_append' ~/.bashrc"
  fi
}

# ssh-copy-id -i ~/.ssh/id_rsa.pub ti1
# ssh-copy-id -i ~/.ssh/id_rsa.pub ti2


# local: 3

sync ti1
sync ti2
sync 1060

# nolan: 2

sync nl1
sync nl2

# wukong test: 2

sync gwkt
sync cwkt

# shenzhen gpu: 6

sync gsz1
sync gsz2
sync gsz3
sync gsz4
sync gsz5
sync gsz6

# shanghai gpu: 6

sync gsh1
sync gsh2
sync gsh3
sync gsh4
sync gsh5
sync gsh6

# shenzhen cpu: 14

sync csz1
sync csz2
sync csz3
sync csz4
sync csz5
sync csz6
sync csz7
sync csz8
sync csz9
sync csz10
sync csz11
sync csz12
sync csz13
sync csz14

# shanghai cpu: 14

sync csh1
sync csh2
sync csh3
sync csh4
sync csh5
sync csh6
sync csh7
sync csh8
sync csh9
sync csh10
sync csh11
sync csh12
sync csh13
sync csh14
