#!/bin/bash
pyinstaller -y --onefile --noconsole --add-data "../Assets":Assets "../Navigator.py"