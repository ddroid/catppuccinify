#!/usr/bin/env python3
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_ZIP = os.path.join(ROOT, "catppuccinify.zip")

FILES_TO_PACK = [
    "color.ini",
    "user.css",
    "theme.js",
    "manifest.json",
    "spotikit.json",
    "preview.png",
    "discord-icon.png",
    "README.md",
    "LICENSE.txt",
    "install.sh",
    "install.ps1",
    "assets/flavor-showcase.png",
    "assets/preview-mocha.png",
    "assets/preview-macchiato.png",
    "assets/preview-frappe.png",
    "assets/preview-latte.png",
]

print(f"📦 Packaging Catppuccinify release zip -> {OUTPUT_ZIP}...")

missing = [f for f in FILES_TO_PACK if not os.path.isfile(os.path.join(ROOT, f))]
if missing:
    print(f"❌ Error: Missing files to package: {missing}", file=sys.stderr)
    sys.exit(1)

with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
    for filename in FILES_TO_PACK:
        filepath = os.path.join(ROOT, filename)
        zf.write(filepath, arcname=filename)
        print(f"  + Added: {filename}")

print(f"✅ Successfully created {OUTPUT_ZIP} ({os.path.getsize(OUTPUT_ZIP)} bytes)")
