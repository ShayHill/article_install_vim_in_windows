"""Expand and collapse external-link markers in README.md.

Authoring external links inline makes the prose hard to read, so mark a term
with ``{{anchor}}`` instead. ``expand_markers`` turns every ``{{anchor}}`` into
a full ``[anchor](url)`` link using the ``_LINKS`` lookup table.
``collapse_links`` does the reverse, rewriting ``[anchor](url)`` back to
``{{anchor}}`` but *only* for an ``anchor: url`` pair that exists in the table,
so hand-written links that aren't in the table are left untouched.

:author: Shay Hill
:created: 2026-06-25
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

_README = Path("README.md")

# an unexpanded ``{{anchor}}`` link marker
_MARKER = re.compile(r"\{\{.+?\}\}")

# {anchor: url}. The anchor is both the marker name (``{{anchor}}``) and the
# visible link text (``[anchor](url)``), so the two functions round-trip.
# Anchors are lowercase; matching against README.md is case-insensitive.
_LINKS: dict[str, str] = {
    # ------------------------------------------------------------------ #
    #  sites and misc
    # ------------------------------------------------------------------ #
    "bram moolenaar": "https://en.wikipedia.org/wiki/Bram_Moolenaar",
    'install the latest version of "powershell 7"': (
        "https://learn.microsoft.com/en-us/powershell/scripting/whats-new"
        "/migrating-from-windows-powershell-51-to-powershell-7?view=powershell-7.4"
    ),
    "use command-line parameters to install visual studio": (
        "https://learn.microsoft.com/en-us/visualstudio/install"
        "/use-command-line-parameters-to-install-visual-studio"
        "?view=vs-2022#use-winget-to-install-or-modify-visual-studio"
    ),
    "package support": "https://vim-jp.org/vimdoc-en/repeat.html#packages",
    "tim pope": "https://github.com/tpope",
    "release dejavu-fonts-2.37 · dejavu-fonts/dejavu-fonts · github": (
        "https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37"
    ),
    "shayhill/vimfiles": "https://github.com/ShayHill/vimfiles",
    "tpope/dotfiles": "https://github.com/tpope/dotfiles",
    "defaults.vim": "https://github.com/vim/vim/blob/master/runtime/defaults.vim",
    "dejavusansmono.ttf": (
        "https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37"
    ),
    # ------------------------------------------------------------------ #
    #  Vim plugins
    # ------------------------------------------------------------------ #
    "lazygit": "https://github.com/jesseduffield/lazygit/",
    "minpac": "https://github.com/k-takata/minpac",
    "sirver/ultisnips: ultisnips": "https://github.com/SirVer/ultisnips",
    "copilot.vim": "https://github.com/github/copilot.vim",
    "ctrl-sf": "https://github.com/dyng/ctrlsf.vim",
    "easyjump.vim": "https://github.com/girishji/EasyJump.vim",
    "fugitive.vim": "https://github.com/tpope/vim-fugitive",
    "fuzzbox": "https://github.com/vim-fuzzbox/fuzzbox.vim",
    "github/copilot.vim": "https://github.com/github/copilot.vim",
    "llama_index": "https://github.com/run-llama/llama_index",
    "madox2/vim-ai": "https://github.com/madox2/vim-ai",
    "monkoose/vim9-stargate": "https://github.com/monkoose/vim9-stargate",
    "puremourning/vimspector": "https://github.com/puremourning/vimspector",
    "tpope/vim-dispatch": "https://github.com/tpope/vim-dispatch",
    "vim-ai": "https://github.com/madox2/vim-ai",
    "vim-dispatch": "https://github.com/tpope/vim-dispatch",
    "vim-easymotion": "https://github.com/easymotion/vim-easymotion",
    "vim-instant-markdown": "https://github.com/instant-markdown/vim-instant-markdown",
    "vim-obsession": "https://github.com/tpope/vim-obsession",
    "vim-prettier": "https://github.com/prettier/vim-prettier",
    "yegappan/lsp": "https://www.github.com/yegappan/lsp",
    # ------------------------------------------------------------------ #
    #  tools
    # ------------------------------------------------------------------ #
    "claude code": "https://www.anthropic.com/claude",
    "difftastic": "https://difftastic.wilfred.me.uk/",
    "git": "https://git-scm.com/",
    "github": "https://github.com",
    "lua": "https://www.lua.org/",
    "node": "https://nodejs.org/",
    "powershell 7": "https://github.com/PowerShell/PowerShell",
    "powershell": "https://github.com/PowerShell/PowerShell",
    "pre-commit": "https://pre-commit.com/",
    "pyright": "https://github.com/microsoft/pyright",
    "python.org": "https://www.python.org/downloads/",
    "ripgrep": "https://github.com/BurntSushi/ripgrep",
    "ruff": "https://docs.astral.sh/ruff/",
    "uv": "https://docs.astral.sh/uv/",
    "yarn": "https://yarnpkg.com/",
}


def expand_markers(text: str) -> str:
    """Replace every ``{{anchor}}`` with ``[anchor](url)`` from the table.

    Anchors match case-insensitively; the marker's original casing is kept as
    the visible link text.
    """
    for anchor, url in _LINKS.items():
        marker = re.compile(r"\{\{(?i:" + re.escape(anchor) + r")\}\}")
        text = marker.sub(lambda m, url=url: f"[{m.group()[2:-2]}]({url})", text)
    return text


def collapse_links(text: str) -> str:
    """Replace ``[anchor](url)`` with ``{{anchor}}`` for known pairs only.

    Anchors match case-insensitively; the link's original casing is kept inside
    the marker. The url must match exactly, so links pointing elsewhere are left
    untouched.
    """
    for anchor, url in _LINKS.items():
        link = re.compile(
            r"\[((?i:" + re.escape(anchor) + r"))\]\(" + re.escape(url) + r"\)"
        )
        text = link.sub(lambda m: f"{{{{{m.group(1)}}}}}", text)
    return text


def assert_no_markers(text: str) -> None:
    """Raise if any unexpanded ``{{anchor}}`` markers remain in *text*.

    The other scripts consume README.md as finished prose, so a leftover
    marker means a link was never expanded with ``expand_markers``.
    """
    markers = sorted(set(_MARKER.findall(text)))
    if markers:
        msg = f"unexpanded link markers in README.md: {', '.join(markers)}"
        raise AssertionError(msg)


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in {"expand", "collapse"}:
        print(f"usage: {Path(sys.argv[0]).name} [expand|collapse]", file=sys.stderr)
        print(sys.argv)
        return 1
    transform = expand_markers if sys.argv[1] == "expand" else collapse_links
    text = _README.read_text(encoding="utf-8")
    _README.write_text(transform(text), encoding="utf-8")
    print(f"{sys.argv[1]}ed link markers in {_README}")
    return 0


if __name__ == "__main__":
    import traceback

    try:
        returncode = main()
    except Exception:  # noqa: BLE001 - keep the console open to show the traceback
        traceback.print_exc()
        returncode = 1
    # when launched by double-click the window closes the instant the process
    # exits, so pause on failure to keep the error on screen.
    if returncode:
        input("\nPress Enter to close . . . ")
    sys.exit(returncode)
