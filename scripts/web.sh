#!/bin/bash

gunicorn -w 4 --timeout 1800 -b 0.0.0.0:5443 youtube_timeline_generator.main:app