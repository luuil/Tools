#!/bin/bash

function ext_and_mv() {
  printf "unzip ~/$1.zip -d ~/$1 && sudo mv ~/$1 /data2/cv/modelx/"
  unzip ~/$1.zip -d ~/$1 && sudo mv ~/$1 /data2/cv/modelx/
}

# version number, integer
model_version=$1

ext_and_mv $model_version