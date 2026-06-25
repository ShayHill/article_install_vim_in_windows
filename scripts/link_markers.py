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
_LINKS: dict[str, str] = {
    # ------------------------------------------------------------------ #
    #  external links already present in README.md
    # ------------------------------------------------------------------ #
    "Bram Moolenaar": "https://en.wikipedia.org/wiki/Bram_Moolenaar",
    'install the latest version of "PowerShell 7"': (
        "https://learn.microsoft.com/en-us/powershell/scripting/whats-new"
        "/migrating-from-windows-powershell-51-to-powershell-7?view=powershell-7.4"
    ),
    "monkoose/vim9-stargate": "https://github.com/monkoose/vim9-stargate",
    "yegappan/lsp": "https://www.github.com/yegappan/lsp",
    r"Download Python \| Python.org": "https://www.python.org/downloads/",
    "vim-instant-markdown": "https://github.com/instant-markdown/vim-instant-markdown",
    "ctrl-sf": "https://github.com/dyng/ctrlsf.vim",
    "copilot.vim": "https://github.com/github/copilot.vim",
    "Yarn (yarnpkg.com)": "https://yarnpkg.com/",
    "vim-prettier": "https://github.com/prettier/vim-prettier",
    "Yarn": "https://yarnpkg.com/",
    "llama_index": "https://github.com/run-llama/llama_index",
    "Use command-line parameters to install Visual Studio": (
        "https://learn.microsoft.com/en-us/visualstudio/install"
        "/use-command-line-parameters-to-install-visual-studio"
        "?view=vs-2022#use-winget-to-install-or-modify-visual-studio"
    ),
    "Lazygit": "https://github.com/jesseduffield/lazygit/",
    "Difftastic, a structural diff (wilfred.me.uk)": "https://difftastic.wilfred.me.uk/",
    "Difftastic": "https://difftastic.wilfred.me.uk/",
    "vim-ai": "https://github.com/madox2/vim-ai",
    "package support": "https://vim-jp.org/vimdoc-en/repeat.html#packages",
    "minpac": "https://vim-jp.org/vimdoc-en/repeat.html#packages",
    "github/copilot.vim": "https://github.com/github/copilot.vim",
    "madox2/vim-ai": "https://github.com/madox2/vim-ai",
    "Minpac": "https://github.com/k-takata/minpac",
    "SirVer/ultisnips: UltiSnips": "https://github.com/SirVer/ultisnips",
    "puremourning/vimspector": "https://github.com/puremourning/vimspector",
    "Tim Pope": "https://github.com/tpope",
    "vim-easymotion": "https://github.com/easymotion/vim-easymotion",
    "easyjump.vim": "https://github.com/girishji/EasyJump.vim",
    "vim-dispatch": "https://github.com/tpope/vim-dispatch",
    "fugitive.vim": "https://github.com/tpope/vim-fugitive",
    "vim-obsession": "https://github.com/tpope/vim-obsession",
    "Release dejavu-fonts-2.37 · dejavu-fonts/dejavu-fonts · GitHub": (
        "https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37"
    ),
    "tpope/vim-dispatch": "https://github.com/tpope/vim-dispatch",
    "fuzzbox": "https://github.com/vim-fuzzbox/fuzzbox.vim",
    "ShayHill/vimfiles": "https://github.com/ShayHill/vimfiles",
    "tpope/dotfiles": "https://github.com/tpope/dotfiles",
    # ------------------------------------------------------------------ #
    #  tools and plugins mentioned without a link
    # ------------------------------------------------------------------ #
    "Git": "https://git-scm.com/",
    "Ripgrep": "https://github.com/BurntSushi/ripgrep",
    "Lua": "https://www.lua.org/",
    "Node": "https://nodejs.org/",
    "PowerShell": "https://github.com/PowerShell/PowerShell",
    "GnuWin32": "https://gnuwin32.sourceforge.net/",
    "UV": "https://docs.astral.sh/uv/",
    "Ruff": "https://docs.astral.sh/ruff/",
    "Pyright": "https://github.com/microsoft/pyright",
    "vim-claude-code": "https://github.com/rishi-opensource/vim-claude-code",
    "Claude Code": "https://docs.claude.com/en/docs/claude-code/overview",
    "pre-commit": "https://pre-commit.com/",
}


def expand_markers(text: str) -> str:
    """Replace every ``{{anchor}}`` with ``[anchor](url)`` from the table."""
    for anchor, url in _LINKS.items():
        text = text.replace(f"{{{{{anchor}}}}}", f"[{anchor}]({url})")
    return text


def collapse_links(text: str) -> str:
    """Replace ``[anchor](url)`` with ``{{anchor}}`` for known pairs only."""
    for anchor, url in _LINKS.items():
        text = text.replace(f"[{anchor}]({url})", f"{{{{{anchor}}}}}")
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
        return 1
    transform = expand_markers if sys.argv[1] == "expand" else collapse_links
    text = _README.read_text(encoding="utf-8")
    _README.write_text(transform(text), encoding="utf-8")
    print(f"{sys.argv[1]}ed link markers in {_README}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
