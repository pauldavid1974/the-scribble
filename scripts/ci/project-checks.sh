#!/bin/sh
# Project-owned CI hook for The Scribble.
# Validates scripts syntax and mechanical CAD assets.
set -eu

echo "==> Running project checks for The Scribble..."

PYTHON_BIN=""
for cmd in python py python3; do
  if command -v "$cmd" >/dev/null 2>&1; then
    if "$cmd" -c "import sys" >/dev/null 2>&1; then
      PYTHON_BIN="$cmd"
      break
    fi
  fi
done

# 1. Validate Python scripts syntax if a working python runtime is found
if [ -n "$PYTHON_BIN" ]; then
  for pyfile in scripts/*.py tools/*.py; do
    if [ -f "$pyfile" ]; then
      "$PYTHON_BIN" -m py_compile "$pyfile"
      echo "  [OK] Python syntax valid: $pyfile"
    fi
  done
else
  echo "  [SKIP] Working Python interpreter not detected; skipping py_compile."
fi

# 2. Verify mechanical CAD artifacts
if [ -f "hardware/the_scribble_v5_step.scad" ]; then
  [ -s "hardware/the_scribble_v5_step.scad" ] || { echo "ERROR: hardware/the_scribble_v5_step.scad is empty"; exit 1; }
  echo "  [OK] Parametric OpenSCAD enclosure verified"
fi

if [ -f "hardware/the_scribble_v5_step.stl" ]; then
  [ -s "hardware/the_scribble_v5_step.stl" ] || { echo "ERROR: hardware/the_scribble_v5_step.stl is empty"; exit 1; }
  echo "  [OK] Printable STL mesh verified"
fi

echo "==> All project checks passed."
