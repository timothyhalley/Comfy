#!/bin/zsh

TARGET_DIR="/Volumes/MySSD/Project/Comfy/ComfyUI/models"

for dir in "$TARGET_DIR"/*/; do
  size=$(du -sh "$dir" | cut -f1)
  file_count=$(find "$dir" -type f | wc -l)
  echo "Directory: $dir"
  echo "Size: $size"
  echo "File Count: $file_count"
  echo "---------------------------"
done
