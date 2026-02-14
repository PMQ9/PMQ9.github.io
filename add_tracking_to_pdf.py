#!/home/connor/.venv/pdf-tools/bin/python3
"""
Add tracked word-slug links to PDF resumes.

This script:
1. Finds the most recently modified PDF in your Resume folder
2. Picks a random clean English word (3-4 letters) as the tracking slug
3. Rewrites pmq9.github.io links in the PDF to pmq9.github.io/#<word>
4. Updates resume_lookup.json so you know which word = which PDF
5. Your site's script.js detects the slug, fires GoatCounter, and cleans the URL

No word is ever reused. With ~9,000 clean words you won't run out.

Usage:
    ./add_tracking_to_pdf.py                # interactive, auto-find latest PDF
    ./add_tracking_to_pdf.py -y             # auto-confirm
    ./add_tracking_to_pdf.py path/to.pdf    # specify a PDF directly
    ./add_tracking_to_pdf.py -y path/to.pdf # both

Example result: pmq9.github.io/#oak  (looks like a normal section anchor)

Setup (one-time):
    python3 -m venv ~/.venv/pdf-tools
    ~/.venv/pdf-tools/bin/pip install pymupdf
"""

import sys
import json
import random
import urllib.request
from pathlib import Path
from datetime import datetime

# ── Configuration ──────────────────────────────────────────────
RESUME_FOLDER = Path("/media/connor/New Volume/Resume")
SITE_ROOT = Path(__file__).resolve().parent
LOOKUP_FILE = SITE_ROOT / "resume_lookup.json"
SITE_DOMAIN = "pmq9.github.io"
WORD_LIST_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
# ───────────────────────────────────────────────────────────────

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF not installed. Run: pip install pymupdf")
    sys.exit(1)

# Words to exclude: offensive, confusing, or clashing with site sections
BLOCKED_WORDS = {
    # Offensive / inappropriate
    "ass", "cum", "damn", "dick", "dumb", "fag", "fags", "fuck", "gay",
    "gays", "hell", "hoe", "hoes", "homo", "jap", "japs", "jew", "jews",
    "kike", "nig", "nigs", "piss", "porn", "puke", "rape", "shit", "slut",
    "spic", "tit", "tits", "twat", "wank", "whore", "anus", "arse",
    "bitch", "boob", "butt", "cock", "coon", "crap", "dyke", "jizz",
    "knob", "milf", "muff", "pedo", "pimp", "poop", "puss", "scum",
    "slag", "smut", "snot", "suck", "turd", "whor",
    # Site section names (would conflict with navigation)
    "home", "about", "skills", "contact",
    # Other confusing slugs
    "help", "blog", "docs", "api", "app", "login", "log", "admin",
    "test", "null", "none", "void", "undefined",
}


def download_word_list() -> list[str]:
    """Download and filter the English word list."""
    print("Downloading word list...")
    response = urllib.request.urlopen(WORD_LIST_URL)
    raw = response.read().decode('utf-8')
    words = []
    for w in raw.splitlines():
        w = w.strip().lower()
        if len(w) < 3 or len(w) > 4:
            continue
        if not w.isalpha():
            continue
        if w in BLOCKED_WORDS:
            continue
        words.append(w)
    return words


def load_lookup() -> dict:
    """Load the lookup table from JSON."""
    if LOOKUP_FILE.exists():
        return json.loads(LOOKUP_FILE.read_text())
    return {"available": [], "entries": {}}


def save_lookup(data: dict):
    """Save the lookup table to JSON."""
    LOOKUP_FILE.write_text(json.dumps(data, indent=2) + "\n")


def initialize_pool(lookup: dict) -> dict:
    """Download words, shuffle, remove already-used ones, save."""
    words = download_word_list()
    used = set(lookup.get("entries", {}).keys())
    available = [w for w in words if w not in used]
    random.shuffle(available)
    lookup["available"] = available
    print(f"Initialized word pool: {len(available)} words available")
    return lookup


def pick_word(lookup: dict) -> str:
    """Pop the next word from the shuffled pool."""
    if not lookup.get("available"):
        lookup = initialize_pool(lookup)
    if not lookup["available"]:
        print("Error: No words left! All 9,000+ words have been used.")
        sys.exit(1)
    return lookup["available"].pop()


def find_most_recent_pdf(folder: Path) -> Path | None:
    """Find the most recently modified PDF in folder and subfolders."""
    pdfs = list(folder.rglob("*.pdf"))
    if not pdfs:
        return None
    return max(pdfs, key=lambda p: p.stat().st_mtime)


def rewrite_pdf_links(pdf_path: str, slug: str) -> int:
    """Rewrite pmq9.github.io links in the PDF to use the hash slug."""
    doc = fitz.open(pdf_path)
    modified_count = 0

    for page_num, page in enumerate(doc):
        links = page.get_links()
        for link in links:
            uri = link.get('uri', '')
            if SITE_DOMAIN not in uri:
                continue

            new_url = f"https://{SITE_DOMAIN}/#{slug}"

            if uri == new_url:
                print(f"  Skipping (already set): {uri}")
                continue

            link['uri'] = new_url
            page.delete_link(link)
            page.insert_link(link)
            print(f"  Page {page_num + 1}: {uri}")
            print(f"         → {new_url}")
            modified_count += 1

    if modified_count > 0:
        doc.save(pdf_path, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        print(f"\nModified {modified_count} link(s)")
    else:
        print(f"\nNo {SITE_DOMAIN} links found to modify.")

    doc.close()
    return modified_count


def main():
    auto_confirm = '-y' in sys.argv or '--yes' in sys.argv
    args = [a for a in sys.argv[1:] if a not in ('-y', '--yes')]

    # Find the PDF
    if args:
        pdf_path = Path(args[0]).resolve()
        if not pdf_path.exists():
            print(f"Error: File not found: {args[0]}")
            sys.exit(1)
    else:
        pdf_path = find_most_recent_pdf(RESUME_FOLDER)
        if not pdf_path:
            print(f"No PDF files found in {RESUME_FOLDER}")
            sys.exit(1)

    modified_time = datetime.fromtimestamp(pdf_path.stat().st_mtime)
    lookup = load_lookup()

    # Initialize pool on first run
    if not lookup.get("available"):
        lookup = initialize_pool(lookup)

    slug = pick_word(lookup)

    print(f"PDF:      {pdf_path.name}")
    print(f"Modified: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Slug:     {slug}")
    print(f"URL:      https://{SITE_DOMAIN}/#{slug}")
    print(f"Pool:     {len(lookup['available'])} words remaining")
    print()

    if not auto_confirm:
        response = input("Add tracking to this file? [Y/n]: ").strip().lower()
        if response and response != 'y':
            # Put the word back
            lookup["available"].append(slug)
            save_lookup(lookup)
            print("Cancelled.")
            sys.exit(0)

    # 1. Rewrite links inside the PDF
    rewrite_pdf_links(str(pdf_path), slug)

    # 2. Update lookup table
    lookup["entries"][slug] = {
        "pdf": pdf_path.name,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_lookup(lookup)

    print(f"\nUpdated resume_lookup.json ({len(lookup['entries'])} used, {len(lookup['available'])} remaining)")
    print()
    print(f"Share: https://{SITE_DOMAIN}/#{slug}")
    print(f"Track: https://pmq9.goatcounter.com")


if __name__ == '__main__':
    main()
