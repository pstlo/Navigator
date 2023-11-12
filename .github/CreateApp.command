#!/bin/bash
cd "$(dirname "$0")"
pyinstaller -y --noconsole --add-data "../Navigator/Assets":Assets -i=Icon.icns "../Navigator/Navigator.py"
