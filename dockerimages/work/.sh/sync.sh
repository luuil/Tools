#!/bin/bash

function sync() {
  echo "[$1]: syncing..."
  rsync --exclude sync.sh -r . $1:~/.sh
  alter_or_not=`ssh $1 "cat ~/.bashrc | grep bashrc_append"`
  if [ -n "$alter_or_not" ]; then
    echo "[$1]: synced already"
  else
    ssh $1  "echo ""source /home/\`whoami\`/.sh/.bashrc_append"" >> ~/.bashrc"
  fi
}

ssh-copy-id -f -i ~/.ssh/id_rsa.pub ti1
ssh-copy-id -f -i ~/.ssh/id_rsa.pub ti2

sync nl1
sync nl2
sync gwk
sync cwk
sync ti1
sync ti2