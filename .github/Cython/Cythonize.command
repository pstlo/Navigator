#!/bin/bash
cd "$(dirname "$0")"
python3 setupCython.py build_ext --inplace