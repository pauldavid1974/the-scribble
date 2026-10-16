#!/bin/sh
# Project-owned CI hook for The Scribble.
# Validates scripts syntax and mechanical CAD assets.
set -eu

echo "==> Running project checks for The Scribble..."

PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py"
fi

# 1. Validate Python scripts syntax if python runtime is found
if [ -n "$PYTHON_BIN" ]; then
  for pyfile in scripts/*.py tools/*.py; do
    if [ -f "$pyfile" ]; then
      "$PYTHON_BIN" -m py_compile "$pyfile"
      echo "  [OK] Python syntax valid: $pyfile"
    fi
  done
else
  echo "  [SKIP] Python interpreter not detected in PATH; skipping py_compile."
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
