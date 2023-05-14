#!/bin/bash
cd "$(dirname "$0")"
pyinstaller -y --noconsole --windowed --add-data "../Assets":Assets --add-data "../gameRecords.txt":. -i=Icon.icns "../Navigator.py"
