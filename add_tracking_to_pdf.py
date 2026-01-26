#!/home/connor/.venv/pdf-tools/bin/python3
"""
Add tracking parameters to PDF hyperlinks.

This script finds the most recently modified PDF in your Resume folder
and appends a ?ref=<filename> parameter to pmq9.github.io links for
GoatCounter analytics tracking.

Usage:
    ./add_tracking_to_pdf.py        # interactive confirmation
    ./add_tracking_to_pdf.py -y     # auto-confirm

Setup (one-time):
    python3 -m venv ~/.venv/pdf-tools
    ~/.venv/pdf-tools/bin/pip install pymupdf
"""

import sys
import re
from pathlib import Path
from datetime import datetime

# Configure your Resume folder here
RESUME_FOLDER = Path("/media/connor/New Volume/Resume")

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)


def find_most_recent_pdf(folder: Path) -> Path | None:
    """Find the most recently modified PDF in folder and subfolders."""
    pdfs = list(folder.rglob("*.pdf"))
    if not pdfs:
        return None
    return max(pdfs, key=lambda p: p.stat().st_mtime)


def sanitize_filename_for_ref(filename: str) -> str:
    """Convert filename to a clean ref parameter value."""
    # Remove .pdf extension
    name = Path(filename).stem
    # Replace spaces and special chars with underscores
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    # Collapse multiple underscores
    name = re.sub(r'_+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    # Lowercase for consistency
    return name.lower()


def add_tracking_to_url(url: str, ref_value: str) -> str:
    """Add ref parameter to a pmq9.github.io URL."""
    # Only modify pmq9.github.io links
    if 'pmq9.github.io' not in url:
        return url

    # Check if URL already has a ref parameter
    if 'ref=' in url:
        print(f"  Skipping (already has ref): {url}")
        return url

    # Add ref parameter
    separator = '&' if '?' in url else '?'
    return f"{url}{separator}ref={ref_value}"


def process_pdf(pdf_path: str) -> int:
    """Process a PDF file, adding tracking to links. Returns count of modified links."""
    path = Path(pdf_path)

    if not path.exists():
        print(f"Error: File not found: {pdf_path}")
        sys.exit(1)

    if path.suffix.lower() != '.pdf':
        print(f"Error: Not a PDF file: {pdf_path}")
        sys.exit(1)

    ref_value = sanitize_filename_for_ref(path.name)
    print(f"Processing: {path.name}")
    print(f"Ref value: {ref_value}")

    doc = fitz.open(pdf_path)
    modified_count = 0

    for page_num, page in enumerate(doc):
        links = page.get_links()

        for link in links:
            if link.get('uri'):
                original_url = link['uri']
                new_url = add_tracking_to_url(original_url, ref_value)

                if new_url != original_url:
                    # Update the link
                    link['uri'] = new_url
                    page.delete_link(link)
                    page.insert_link(link)
                    print(f"  Page {page_num + 1}: {original_url}")
                    print(f"         → {new_url}")
                    modified_count += 1

    if modified_count > 0:
        # Save in-place
        doc.save(pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        print(f"\nModified {modified_count} link(s) in {path.name}")
    else:
        print(f"\nNo pmq9.github.io links found to modify.")

    doc.close()
    return modified_count


def main():
    auto_confirm = '-y' in sys.argv or '--yes' in sys.argv

    # Find the most recently modified PDF
    recent_pdf = find_most_recent_pdf(RESUME_FOLDER)

    if not recent_pdf:
        print(f"No PDF files found in {RESUME_FOLDER}")
        sys.exit(1)

    # Show which file was found
    modified_time = datetime.fromtimestamp(recent_pdf.stat().st_mtime)
    print(f"Most recently modified PDF:")
    print(f"  {recent_pdf.name}")
    print(f"  Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if not auto_confirm:
        response = input("Add tracking to this file? [Y/n]: ").strip().lower()
        if response and response != 'y':
            print("Cancelled.")
            sys.exit(0)

    process_pdf(str(recent_pdf))


if __name__ == '__main__':
    main()
