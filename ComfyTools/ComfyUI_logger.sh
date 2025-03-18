#!/bin/bash

# Default log file path
DEFAULT_LOGFILE=~/Projects/ComfyUI/user/comfyui_8000.log

# Check if a log file is provided as an argument, otherwise use the default
LOGFILE=${1:-$DEFAULT_LOGFILE}

# Display the last 20 lines of the log file and follow it in real time
echo "Showing the last 20 lines of $LOGFILE"
tail -n 20 -f "$LOGFILE"