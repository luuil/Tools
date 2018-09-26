#!/bin/bash

function sync() {
  printf "[$1]: syncing...\n"
  rsync -azP --exclude='~/.sh/sync.sh' ~/.sh/ $1:~/.sh
  alter_or_not=`ssh -t $1 "cat ~/.bashrc | grep bashrc_append"`
  if [ -n "$alter_or_not" ]; then
    printf "[$1]: synced already\n\n"
  else
    printf "[$1]: append 'source ~/.sh/.bashrc_append' to '~/.bashrc'\n\n"
    ssh -t $1 "sed -i '\$a # my bashrc\nsource ~/.sh/.bashrc_append' ~/.bashrc"
  fi
}

ssh-copy-id -i ~/.ssh/id_rsa.pub ti1
ssh-copy-id -i ~/.ssh/id_rsa.pub ti2

sync nl1
sync nl2
sync gwk
sync cwk
sync ti1
sync ti2