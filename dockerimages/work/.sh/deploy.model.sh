#!/bin/bash

function sync() {
  printf "[$1]: rsync -azP ~/modelx/$2.zip $1:~/$2.zip\n"
  rsync -azP ~/modelx/$2.zip $1:~/$2.zip
  printf "\n"
}

# version number, integer
model_version=$1

# sync to 10.68.50.181 from local first,
# then sync to other machines from 10.68.50.181

sync gsz1 $model_version
# sync gsz2 $model_version
# sync gsz3 $model_version
# sync gsz4 $model_version
# sync gsz5 $model_version
# sync gsh1 $model_version
# sync gsh2 $model_version
# sync gsh3 $model_version
# sync gsh4 $model_version
# sync gsh5 $model_version
