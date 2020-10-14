# Photo-a-day Aligner 

A tool to create time-lapse videos from daily self portraits. Forked from and based (almost entirely) on [Matthew Earl's work](https://matthewearl.github.io/2016/01/22/portrait-timelapse/).

## Requirements

 * Python 3 + opencv-python, dlib and exifread libraries
 * ImageMagick
 * ffmpeg

## Setup
 * `chmod a+x process.sh`

## Usage
 * Put all photos inside a new directory
 * Run `process.sh` from within that directory, for example `~/path/to/photo-day-aligner/process.sh`
 * A video file called `out.mp4` will be created in the same directory.

## Options
 * Image width, height and resolution can be passed as arguments, for example `process.sh -h 1536 -w 2046 -r 300`