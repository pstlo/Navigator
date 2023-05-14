#!/bin/bash
cd "$(dirname "$0")"
pyinstaller -y --noconsole --windowed --add-data "../Assets":Assets --add-data "../gameRecords.txt":. --add-data "../Navigator.cpython-311-darwin.so":. -i=Icon.icns "Main.py"