#!/bin/bash

python3 slides.py
while inotifywait -e close_write ./*.py; do uv run slides.py; done
