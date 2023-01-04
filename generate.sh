#!/bin/bash

#Change directory to script directory
dir=$(cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
cd "$dir"

#Source python virtual environment
. venv/bin/activate
python generator.py
