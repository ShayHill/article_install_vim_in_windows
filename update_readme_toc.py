"""Overwrite the table of contents under the `# Table of Contents` header.

Scan the README.md file for 1st- and 2nd-level headings (``#`` and ``##``),
skipping the "Table of Contents" header itself, then rewrite the list that
follows the `# Table of Contents` header. Links use GitHub's anchor-slug
rules.


:author: Shay Hill
:created: 2026-06-14
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_README = Path("README.md")

_TOC_HEADER = "# Table of Contents"

# a fenced code block: ``` ... matching close fence
_CODE_BLOCK = re.compile(r"^(`{3,}).*?^\1.*?$", re.MULTILINE | re.DOTALL)

# a 1st- or 2nd-level heading line
_HEADING = re.compile(r"^(#{1,2})[ \t]+(.+?)[ \t]*#*$", re.MULTILINE)

# the TOC header and everything up to (not including) the next 1st-level heading
_TOC_SECTION = re.compile(
    r"^" + re.escape(_TOC_HEADER) + r"[ \t]*$.*?(?=^# )",
    re.MULTILINE | re.DOTALL,
)

# the indent for 2nd-level headings in the TOC list
_TAB = "  "

def _slugify(text: str) -> str:
    """Convert heading text to a GitHub anchor slug."""
    slug = re.sub(r"[^\w\s-]", "", text.strip().lower())
    return re.sub(r"\s+", "-", slug)


def _build_toc(text: str) -> str:
    """Delete code blocks, then find headings and build a markdown list of links."""
    no_code = _CODE_BLOCK.sub("", text)
    entries: list[str] = []
    for hashes, heading in _HEADING.findall(no_code):
        if heading.strip() == _TOC_HEADER.lstrip("# "):
            continue
        indent = _TAB * (len(hashes) - 1)
        entries.append(f"{indent}- [{heading}](#{_slugify(heading)})")
    return "\n".join(entries)


def _replace_toc(text: str) -> str:
    """Replace the list under the `# Table of Contents` header."""
    if not _TOC_SECTION.search(text):
        msg = f"could not find a {_TOC_HEADER!r} section"
        raise ValueError(msg)
    replacement = f"{_TOC_HEADER}\n\n{_build_toc(text)}\n\n"
    return _TOC_SECTION.sub(lambda _: replacement, text, count=1)


def main() -> int:
    text = _README.read_text(encoding="utf-8")
    try:
        new_text = _replace_toc(text)
    except ValueError as e:
        print(e, file=sys.stderr)
        return 1
    _README.write_text(new_text, encoding="utf-8")
    print(f"updated table of contents in {_README}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
