#!/bin/bash

function sync() {
  printf "[$1]: rsync -azP ~/modelx/$2.zip $1:~/$2.zip\n"
  rsync -azP ~/modelx/$2.zip $1:~/$2.zip
  printf "\n"
}

# version number, integer
model_version=$1

sync gsz1 $model_version
sync gsz2 $model_version
sync gsz3 $model_version
sync gsz4 $model_version
sync gsh1 $model_version
sync gsh2 $model_version
sync gsh3 $model_version
sync gsh4 $model_version
