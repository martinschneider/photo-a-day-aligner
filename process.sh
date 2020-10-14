#!/bin/bash
dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# defaults
width=1536
height=2046
res=300

while getopts ":h:w:r:" opt; do
  case $opt in
    h) height="$OPTARG"
    ;;
    w) width="$OPTARG"
    ;;
    r) res="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

echo "Copying photos..."
mkdir input
mv * input ; cp -r input/* .
cp $dir/pada.conf .
echo "Resizing images..."
convert 'input/IMG_*.jpg' -auto-orient -density $res -units PixelsPerInch 'jpg:input/resized%03d.jpg' &&
mogrify input/resized*.jpg[${width}x${height}] &&

echo "Aligning images..." &&
python3 $dir/pada.py align &&

echo "Creating video..." &&
cat aligned/*.jpg | ffmpeg -y -f image2pipe -r 20 -vcodec mjpeg -i - -vcodec libx264 out.mp4
