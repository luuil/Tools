#!/bin/bash

function ext_and_mv() {
  printf "~/$1.zip: extracting..\n"
  unzip ~/$1.zip -d ~/$1

  printf "~/$1/: moving to /data2/cv/modelx/\n"
  sudo mv ~/$1 /data2/cv/modelx/
}

model_version=20

ext_and_mv $model_version