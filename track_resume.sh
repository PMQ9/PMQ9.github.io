#!/bin/bash
# Double-click this to add tracking to your latest PDF resume.
cd "$(dirname "$0")"
/home/connor/.venv/pdf-tools/bin/python3 add_tracking_to_pdf.py "$@"
echo
read -p "Press Enter to close..."
