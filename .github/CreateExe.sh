#!/bin/bash
pyinstaller -y --onefile --noconsole --add-data "../Navigator/Assets":Assets "../Navigator/Navigator.py"
