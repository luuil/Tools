#!/bin/bash

# sync to 10.68.50.181 from local first,
# then sync to other machines from 10.68.50.181.

# version number, integer
if [[ $# -eq 0 ]] ; then
    echo 'You should supply model_version at least'
    exit 1
fi
model_version=$1


# sleep time interval: 3 minutes
interval="3m"


# shenzhen: 6
ips_sz=(
  "10.68.50.181"
  "10.68.50.180"
  "10.68.50.184"
  "10.68.50.186"
  "10.68.33.75"
  "10.68.32.228"
  )


# shanghai: 6
ips_sh=(
  "10.68.8.109"
  "10.68.8.108"
  "10.68.8.107"
  "10.68.8.106"
  "10.68.9.155"
  "10.68.9.210"
  )


################################################

function sleepawhile() {
  printf "\nsleep $1..\n"
  sleep $1
  printf "\ncontinue..\n\n"
}

function sync() {
  ip=$1
  model_version=$2
  printf "[$ip]: rsync -azP ~/$model_version.zip $ip:~/$model_version.zip\n"
  rsync -azP ~/$model_version.zip $ip:~/$model_version.zip
  ssh $ip "bash ~/.sh/ext_and_mv.sh $model_version"
}

function multisync() {
  model_version=$1 # Save first argument in a variable
  interval=$2      # Save second argument in a variable
  shift            # Shift all arguments to the left (original $1 gets lost)
  shift            # Shift all arguments to the left (original $1 and $2 gets lost)
  ips=("$@")       # Rebuild the array with rest of arguments
  counter=0
  for i in "${ips[@]}"; do
    sync $i $model_version
    let counter=counter+1
    if [ $counter -lt ${#ips[@]} ]; then
      sleepawhile $interval
    fi
  done
}

multisync $model_version $interval "${ips_sz[@]}" "${ips_sh[@]}"