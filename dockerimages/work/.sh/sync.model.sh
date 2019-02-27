#!/bin/bash

function sync() {
  printf "[$1]: rsync -azP ~/modelx/$2.zip $1:~/$2.zip\n"
  rsync -azP ~/$2.zip $1:~/$2.zip
  printf "\n"
}

# version number, integer
model_version=$1

# shenzhen: 6

# sync to 10.68.50.181 from local first,
# then sync to other machines from 10.68.50.181

sync 10.68.50.181 $model_version
sync 10.68.50.180 $model_version
sync 10.68.50.184 $model_version
sync 10.68.50.186 $model_version
sync 10.68.33.75 $model_version
sync 10.68.32.228 $model_version

# shanghai: 6

sync 10.68.8.109 $model_version
sync 10.68.8.108 $model_version
sync 10.68.8.107 $model_version
sync 10.68.8.106 $model_version
sync 10.68.9.126 $model_version
sync 10.68.9.210 $model_version