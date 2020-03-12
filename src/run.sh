#!/bin/sh

python get_data.py

git add ..

git commit -m "$(date +%F)"
#git push

