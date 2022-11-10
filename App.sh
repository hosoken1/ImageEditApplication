#!/bin/bash
export DISPLAY = :0
printenv DISPLAY
cd /home/hosoya/ドキュメント/app/ImageEditApplication
python3 main.py
python3 -m tkinter
exit 0
