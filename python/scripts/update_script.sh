#!/bin/bash

git config --global alias.up '!git remote update -p; git merge --ff-only @{u}'
cd /opt/filing13F_searcher/python && git checkout main && git up

source /home/robo/venv/bin/activate

python /opt/filing13F_searcher/python/setup.py install

supervisorctl restart