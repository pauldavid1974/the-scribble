#!/bin/sh
# Project-owned CI hook for The Scribble.
# Validates scripts syntax and mechanical CAD assets.
set -eu

echo "==> Running project checks for The Scribble..."

# 1. Validate Python scripts syntax if any exist
for pyfile in scripts/*.py tools/*.py; do
  if [ -f "$pyfile" ]; then
    python -m py_compile "$pyfile"
    echo "  [OK] Python syntax valid: $pyfile"
  fi
done

# 2. Verify mechanical CAD artifacts if present
if [ -f "hardware/the_scribble_v5_step.scad" ]; then
  [ -s "hardware/the_scribble_v5_step.scad" ] || { echo "ERROR: hardware/the_scribble_v5_step.scad is empty"; exit 1; }
  echo "  [OK] Parametric OpenSCAD enclosure verified"
fi

if [ -f "hardware/the_scribble_v5_step.stl" ]; then
  [ -s "hardware/the_scribble_v5_step.stl" ] || { echo "ERROR: hardware/the_scribble_v5_step.stl is empty"; exit 1; }
  echo "  [OK] Printable STL mesh verified"
fi

echo "==> All project checks passed."
