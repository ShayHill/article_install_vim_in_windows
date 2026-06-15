"""Convert README.md to an article for shayallenhill.com.

The README is the canonical, version-controlled source. The blog post is the
same content wrapped for Jekyll/kramdown:

* a YAML front-matter block, a ``<style>`` block, and a link back to this
  repository are prepended;
* every heading *below* h1 (``##`` and deeper) is followed by a ``{:.no_toc}``
  line so kramdown's auto-generated table of contents lists only the h1
  section titles;
* the ``# Table of Contents`` section (an h1, but excluded from the TOC with
  its own ``{:.no_toc}``) has its hand-written link list replaced by the
  kramdown ``{:toc}`` marker.

:author: Shay Hill
:created: 2026-06-14
"""

from __future__ import annotations

import sys
from pathlib import Path

_README = Path("README.md")

# where the generated post lives
_ARTICLE = Path(
    r"C:\Users\shaya\GitHub\Jekyll\blog_articles\_posts\2024-09-22-vim-in-windows.md"
)

# the heading text of the table-of-contents section (an h1)
_TOC_HEADING = "Table of Contents"

# the kramdown "exclude from table of contents" marker
_NO_TOC = "{:.no_toc}"

# front matter, styles, and the source link, prepended ahead of the README body
_HEADER = """\
---
layout: post
title: "Install and Configure Vim in Windows"
date: 2024-09-21 17:13:21 -0600
tags:
categories: [programming]
author: Shay Hill
excerpt: Install Vim in Windows and configure it for a nice experience.
post_image: "https://shayallenhill.com/assets/img/blog/vim-in-windows/chemistry_set_with_logo.png"
---

<style type="text/css">
    p.toc-head,
    p.toc-subhead {
        margin-bottom: 0px;
    }
    p.toc-subhead {
        margin-left: 2em;
    }
</style>

If you intend to work your way through this article, go [here](https://github.com/ShayHill/article_install_vim_in_windows/tree/main) for the version-controlled source."""

# the lines that replace the hand-written table-of-contents link list
_TOC_BLOCK = [
    f"# {_TOC_HEADING}",
    _NO_TOC,
    "",
    f"* {_TOC_HEADING}",
    "{:toc}",
    "",
    "",
]


def _fence(line: str) -> str | None:
    """Return the ``` or ~~~ run that opens/closes a code fence, else None."""
    stripped = line.lstrip()
    for char in ("`", "~"):
        run = char * (len(stripped) - len(stripped.lstrip(char)))
        if len(run) >= 3:
            return run
    return None


def _heading(line: str) -> tuple[int, str] | None:
    """Return (level, text) for an ATX heading line, else None."""
    if not line.startswith("#"):
        return None
    hashes = len(line) - len(line.lstrip("#"))
    rest = line[hashes:]
    if hashes > 6 or not rest[:1].isspace():
        return None
    return hashes, rest.strip().rstrip("#").strip()


def _convert(readme: str) -> str:
    """Wrap the README body as the Jekyll post."""
    lines = readme.splitlines()
    out: list[str] = []
    open_fence: str | None = None
    i = 0
    while i < len(lines):
        line = lines[i]

        # inside a code block: copy verbatim, watching for the closing fence
        if open_fence is not None:
            out.append(line)
            fence = _fence(line)
            if fence is not None and fence[0] == open_fence[0] and len(fence) >= len(
                open_fence
            ):
                open_fence = None
            i += 1
            continue

        fence = _fence(line)
        if fence is not None:
            open_fence = fence
            out.append(line)
            i += 1
            continue

        heading = _heading(line)
        if heading is None:
            out.append(line)
            i += 1
            continue

        level, text = heading
        if level == 1 and text == _TOC_HEADING:
            # replace the hand-written link list with the kramdown marker, then
            # skip the old list up to (not including) the next h1 heading
            out.extend(_TOC_BLOCK)
            i += 1
            while i < len(lines):
                following = _heading(lines[i])
                if following is not None and following[0] == 1:
                    break
                i += 1
        elif level == 1:
            out.append(line)
            i += 1
        else:
            out.append(line)
            out.append(_NO_TOC)
            i += 1

    body = "\n".join(out)
    return f"{_HEADER}\n\n{body}\n"


def main() -> int:
    if not _README.is_file():
        print(f"could not find {_README}", file=sys.stderr)
        return 1

    article = _convert(_README.read_text(encoding="utf-8"))
    _ARTICLE.write_text(article, encoding="utf-8")
    print(f"wrote {_ARTICLE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
