#!/usr/bin/env python3

import hashlib
from pathlib import Path

# File types supported by Nexterm
SCRIPT_EXTS = {".sh", ".bash", ".zsh", ".fish", ".ps1"}
SNIPPET_EXTS = {".txt", ".snippet", ".cmd"}
THEME_EXT = ".theme.css"

ROOT = Path(__file__).parent.resolve()
INDEX_FILE = ROOT / "NTINDEX"


def md5sum(filename):
    h = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


entries = []

for file in ROOT.rglob("*"):
    if not file.is_file():
        continue

    # Skip generated index and git files
    if file.name == "NTINDEX":
        continue

    if ".git" in file.parts:
        continue

    relpath = file.relative_to(ROOT).as_posix()

    if relpath.endswith(THEME_EXT):
        pass
    elif file.suffix.lower() in SCRIPT_EXTS:
        pass
    elif file.suffix.lower() in SNIPPET_EXTS:
        pass
    else:
        continue

    entries.append((relpath, md5sum(file)))

entries.sort()

with open(INDEX_FILE, "w", newline="\n") as f:
    f.write("# Nexterm Source Index\n")
    f.write("# Generated automatically\n\n")

    for path, digest in entries:
        f.write(f"{path}@{digest}\n")

print(f"Generated {INDEX_FILE}")
print(f"Indexed {len(entries)} files.")