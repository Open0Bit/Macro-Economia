#!/bin/bash
# setup.sh
mkdir -p data/raw data/processed scripts notebooks figures output docs tests
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
