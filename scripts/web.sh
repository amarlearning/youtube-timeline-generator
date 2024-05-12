#!/bin/bash

gunicorn -w 4 --timeout 90 llm_video_timeline_description.main:app