#!/bin/bash
cd "$(dirname "$0")"
pyinstaller -y --name=Navigator --noconsole --windowed --add-data "../../Navigator/Assets":Assets --add-data *.so:. -i=Icon.icns "cMain.py"
