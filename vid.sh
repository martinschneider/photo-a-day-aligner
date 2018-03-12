#!/bin/bash

#ls -1 ./aligned/* > filtered.txt
#for i in $(ls *.jpg); do exiv2 -r '%Y-%m-%d_%H-%M-%S.:basename:' rename $i; done

OUT_FOLDER=/run/media/iomihai/dashcam2/timelapse/face_lapse

rsync -av --ignore-existing /mnt/nfs/diverse/camera/mihai/ $OUT_FOLDER/input_large
for file in $OUT_FOLDER/input_large/*.jpg; do
    filename=$(basename $file)
    if [ ! -f $OUT_FOLDER/input/$filename ]; then
        echo 'resize '$filename
    	convert $OUT_FOLDER/input_large/$filename -resize 1600x1200 -gravity center -background black -extent 1600x1200 $OUT_FOLDER/input/$filename
    fi
done
source ./venv/bin/activate
./pada.py align
deactivate
ffmpeg -y -threads 6 -loglevel error -framerate 15/1 -i $OUT_FOLDER/aligned/%08d.jpg -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart -r 30 $OUT_FOLDER/out/face_lapse_15.mp4
ffmpeg -y -threads 6 -loglevel error -framerate 10/1 -i $OUT_FOLDER/aligned/%08d.jpg -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart -r 30 $OUT_FOLDER/out/face_lapse_10.mp4
ffmpeg -y -threads 6 -loglevel error -framerate 5/1 -i $OUT_FOLDER/aligned/%08d.jpg -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart -r 30 $OUT_FOLDER/out/face_lapse_5.mp4
printf "file '%s'\n" $OUT_FOLDER/input/*.jpg > $OUT_FOLDER/input.txt
ffmpeg -y -threads 6 -loglevel error -f concat -safe 0 -i $OUT_FOLDER/input.txt -r 15/1 -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart -r 30 $OUT_FOLDER/out/face_lapse_input.mp4
