#!/usr/bin/env bash
usage() {
    echo 'avi2mp4 video_path [[video_path2]...]'
}

convert_one() {
    video_path=$1
    ffmpeg -y -i $video_path -vcodec libx264 "$video_path.mp4"  && rm -f $video_path
}

if [ $# -eq 0 ]; then
    usage
else  # support more than one to be convert
    set -x # echo on

    for path in "$@"
    do
        convert_one $path
    done

    set +x # echo off
fi