#!/bin/bash

project_path=$(dirname "$0")
cd $project_path
pipenv run python3 src/main.py

