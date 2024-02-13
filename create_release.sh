#!/bin/bash

cwd=$(pwd)

cmd="pyinstaller --onefile $cwd/dash_app.py --distpath $cwd/release/"
echo "Running command: $cmd"
$cmd
echo "Release created at $cwd/release"