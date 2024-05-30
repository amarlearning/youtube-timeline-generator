#!/bin/bash

gunicorn -w 4 --timeout 1800 llm_video_timeline_description.main:app