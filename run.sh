#!/bin/bash

project_path=$(dirname "$0")
cd $project_path
/usr/local/bin/pipenv run python3 src/main.py

