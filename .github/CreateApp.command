#!/bin/bash
cd "$(dirname "$0")"
pyinstaller -y --noconsole --add-data "../Assets":Assets -i=Icon.icns "../Navigator.py"
