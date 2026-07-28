# Missing Windows / Vim Tribal Knowledge

## 1. `shellxquote` for pwsh

Windows defaults `shellxquote` to `"` (for cmd.exe compatibility). With `shell=pwsh` this
double-quotes shell commands and breaks `:!` and `:term`. Add alongside the other pwsh settings:

```vim
set shellxquote=
```

## 2. `grepformat` is missing alongside `grepprg`

`grepprg=rg\ --vimgrep\ --no-heading` is set but `grepformat` is left at its default, which
doesn't correctly parse ripgrep's `file:line:col:match` output. Add:

```vim
set grepformat=%f:%l:%c:%m,%f:%l:%m
```

## 3. CRLF / line endings

The single most common Windows text-editor surprise. Vim can silently add `^M` characters when
editing files that originated on Linux. `set fileformats=unix,dos` tells Vim to prefer LF but
tolerate CRLF. This belongs near the top of the vimrc.

## 4. `set encoding=utf-8`

Windows Vim can default to `cp1252` or another Windows encoding. Setting `encoding=utf-8` near
the top of the vimrc (before any plugins) prevents garbled characters and is standard practice
on Windows specifically.

## 5. Windows Defender exclusions

Defender's real-time scanning scans every file Vim touches on open/write/swap. Adding
`C:\Program Files\Vim`, `~\vimfiles`, and project directories to Defender's exclusion list is
a common first fix when Vim "feels slow" on Windows.

## 6. Persistent undo + undodir

`set undofile` is a Vim quality-of-life feature, but the default `undodir` scatters `.un~`
files next to source files. On Windows it's worth pointing to a dedicated directory:

```vim
set undofile
set undodir=$HOME/vimfiles/.undo//
```

The trailing `//` makes filenames unique by encoding the full path.

## 7. vimfiles inside OneDrive

`~/Documents` on Windows 11 is often silently synced to OneDrive. Vim's swap files and lock
files conflict badly with OneDrive's own file locking. `~/vimfiles` should be outside the
OneDrive-synced tree (e.g., `~/AppData/Local/vimfiles` or just `~/vimfiles` if `~` maps
outside Documents).

## 8. Windows long-path limit

The 260-character path limit bites plugin managers (minpac clones nested repos) and Python's
`.venv` trees. One line of tribal knowledge, run in Admin PowerShell:

```powershell
git config --system core.longpaths true
```

---

The biggest practical impact in day-to-day use: `shellxquote` (#1) breaks `:!` commands
silently, `grepformat` (#2) makes `:grep` results un-jumpable, and CRLF (#3) causes confusing
diffs. Those three are the most likely to bite someone following this guide.
