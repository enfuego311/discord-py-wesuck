#!/bin/sh

python3 -m venv venv --system-site-packages
. venv/bin/activate
pip3 install -r txt/requirements.txt
