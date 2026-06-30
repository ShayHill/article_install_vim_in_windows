# Introduction

The traditional ethos of Vim has been "Vim is my text editor; my OS is my IDE", meaning Vim users would write or edit a program in Vim then use git, grep, sed, awk, find, build, etc., etc., etc. through each application's command-line interface instead of a graphical *interface to an interface* built into an IDE.

This isn't enforced. Some *interfaces to interfaces* have been built into Vim over the years, and others have become popular through plugins, but the *interfaces to interfaces* are generally much thinner that what you'd find in an IDE. If asked, "How do you commit and push your changes in Vim?", many Vim users would say, "I don't".

This ethos is a little more straightforward in Linux, because Linux typically comes with pre-installed *git, grep, sed, awk, find, build, etc., etc., etc.*. Windows does not.

At the same time, the ethos has expanded to "Vim is my text editor; my OS *and various APIs* are my IDE", because a lot of us want LSPs and AI. The Vim community have written *interfaces to APIs* as plugins, and they have reduced the complexity as far as reasonably possible, but you will have to do a small bit of configuration.

In truth, you'll have to do "a small bit of configuration" in any editor or IDE. At some point, and it won't be long, you will have to hack through json files and dig through menus and fall back to native interfaces for missing *interface-to-interface* features. The difference in Vim is that you'll have to do more of it up front.

There's nothing difficult about putting this all together, but there are a few pitfalls and "unknown unknowns" if you haven't done it before. This guide will start from a stock Windows 11 install and take you all the way to a Python development environment with completion, snippets, LSPs, debugging, AI, etc. The end result will be heavy in features, but light in customization. From there, you can start exploring.

## copy and paste

There is a lot of code in this guide that you may wish to copy and paste into your Vim files. If you are very new to Vim, this is how you copy to and from the Windows clipboard:

- Select text then `"+y` to copy to the Windows clipboard.
- `"+p` to paste from the Windows clipboard.

So, to copy code from this guide, just copy the code in Windows, then enter Normal mode (press `<ESC>`) then `"+p` to paste the code into Vim.

If you're using gVim, you can copy and paste by right clicking and selecting copy or paste, the same way you would in almost any Windows gui.

### paste commands

In addition to configuration text, which can be pasted into files in Vim as above, there are a few long commands (e.g., `:call append('.', 'set guifont=' .. &guifont)`) which you may want to copy and paste into vim as well.

In Windows Terminal applications (including Vim) `Control-Shift-v` will paste from the Windows clipboard **as keystrokes**. This can be useful, because a string starting with `:`, `/`, or `?` will be interpreted as a Vim command. In the [Install Vim](#install-vim) section, I have included a mapping for `Control-Shift-v` to dupicate this behavior in gVim.

# Table of Contents

- [Introduction](#introduction)
  - [copy and paste](#copy-and-paste)
- [Install Vim](#install-vim)
  - [create a vimrc](#create-a-vimrc)
- [Install Cross-Platform PowerShell](#install-cross-platform-powershell)
  - [configuration](#configuration)
  - [termguicolors](#termguicolors)
  - [options](#options)
  - ["missing" shortcuts](#missing-shortcuts)
- [Install Python](#install-python)
- [Install Git](#install-git)
  - [configure git from PowerShell](#configure-git-from-powershell)
  - [other things that come with git](#other-things-that-come-with-git)
- [Install Ripgrep](#install-ripgrep)
  - [tell Vim to use ripgrep](#tell-vim-to-use-ripgrep)
- [Install Node](#install-node)
  - [install yarn](#install-yarn)
- [Install Visual Studio Build Tools](#install-visual-studio-build-tools)
- [Install Lazygit](#install-lazygit)
  - [difftastic](#difftastic)
- [Install GNU zip and unzip](#install-gnu-zip-and-unzip)
- [Install Vim Plugins](#install-vim-plugins)
  - [enable Vim built-In plugins](#enable-vim-built-in-plugins)
  - [external plugins](#external-plugins)
- [LSP](#lsp)
- [Artificial Intelligence](#artificial-intelligence)
  - [Copilot](#copilot)
  - [Chat](#chat)
  - [Claude Code](#claude-code)
- [Snippets](#snippets)
  - [create a snippet](#create-a-snippet)
- [Debugging](#debugging)
  - [.vimspector.json](#vimspectorjson)
  - [run Vimspector](#run-vimspector)
- [Fuzzy Finding](#fuzzy-finding)
- [The Usual Suspects](#the-usual-suspects)
- [Vim Configuration](#vim-configuration)
- [gVim Configuration](#gvim-configuration)
  - [set gVim guifont](#set-gvim-guifont)
  - [updating the terminal font](#updating-the-terminal-font)
  - [renderoptions](#renderoptions)
  - [window size](#window-size)
- [The Vim ftplugin Directory](#the-vim-ftplugin-directory)
  - [configure Vim for Python files](#configure-vim-for-python-files)
  - [configure the aichat window](#configure-the-aichat-window)
- [The Vim compiler Directory](#the-vim-compiler-directory)
  - [asynchronous pre-commit](#asynchronous-pre-commit)
- [More](#more)
- [TL;DR?](#tldr)

# Install Vim

This is an obvious first step, and it's an easy one, because we're not going to compile Vim. But there are some tricks if you aren't familiar with Windows.

In this guide, we're going to use `winget`.

```powershell
winget install vim.vim --source winget
```

The installer will not add `vim` and `gvim` to your Path environment variable. You can add them now ...

### but first!

You can easily break things when altering your environment variables. Run this in [PowerShell](https://github.com/PowerShell/PowerShell) to export your current values to a json file.

```powershell
[System.Environment]::GetEnvironmentVariables().GetEnumerator() |
ForEach-Object { [PSCustomObject]@{ Name = $_.Key; Value = $_.Value } } |
ConvertTo-Json -Depth 3 |
Set-Content -Path "env_variables.json"
```

### now

I have to give two commands, because, as I write this, Vim is using two different installation paths. `winget install vim.vim` will create a system-wide install of Vim in `C:\Program Files`; `winget install vim.vim.vightly` will perform a user install into `~\AppData\Local\Programs`.

Open [PowerShell](https://github.com/PowerShell/PowerShell) and enter (If you've installed Vim 9.2)

```powershell
[Environment]::SetEnvironmentVariable("PATH", "$($env:PATH);C:\Program Files\Vim\vim92", [EnvironmentVariableTarget]::User)
```

or

```powershell
[Environment]::SetEnvironmentVariable("PATH", "$($env:PATH);$HOME\AppData\Local\Programs\Vim", [EnvironmentVariableTarget]::User)
```

Environment variables are read when applications are opened, so changes to environment variables will not take effect until you open a new terminal window. There are other ways, but that's the easy way.

## create a vimrc

If you open gVim now, you will have a fairly nice experience. Filetype detection and syntax highlighting will work, backspace will behave as you expect it to, and commands will autocomplete.

However, once you create your own configuration in

```
~\vimfiles\vimrc
```

Vim gets (arguably) worse! This is because [Bram Moolenaar](https://en.wikipedia.org/wiki/Bram_Moolenaar) and others configured some nice default behaviors in `$VIMRUNTIME/defaults.vim`

But these defaults aren't, strictly speaking, defaults, because this is not how Vim will look and behave with *no* configuration. `devaults.vim` is a sample configuration. When you create your own `vimrc` file, Vim reads *your* `vimrc` *instead of* [defaults.vim](https://github.com/vim/vim/blob/master/runtime/defaults.vim), so you get true "out of the box" Vim behavior: no filetype detection, no syntax highlighting, and 1970s-style backspace behavior.

This is all we'll configure for now. Open gVim (not Vim itself. Wait until we have a better shell to run it in) from the Windows menu. Then run this command:

```
:e ~\vimfiles\vimrc
```

and create a simple `vimrc` with this content:

```
vim9script

# nice defaults from Bram and the The Vim Project
source $VIMRUNTIME/defaults.vim

# small enhancements based on filetype,
# including indentation styles for Python.
filetype plugin indent on

# Set tab width for Vim files to make posting
# out of this guide easier.
autocmd FileType vim setlocal expandtab
autocmd FileType vim setlocal tabstop=2
autocmd FileType vim setlocal softtabstop=2
autocmd FileType vim setlocal shiftwidth=2

# ---------------------------------------------------------------------------- #
#
#  Put clipboard as keystrokes, for replicating <C-S-v> terminal-Vim behavior
#  in gVim. The <C-S-v> mapping will never reach Windows Terminal Vim, because
#  the Windows Terminal will intercept it.
#
# ---------------------------------------------------------------------------- #

nnoremap <C-S-v> :call feedkeys(getreg('+'), 't')<CR>
inoremap <C-S-v> <C-r>+
cnoremap <C-S-v> <C-r>+
```

`source $VIMRUNTIME/defaults.vim` will preserve the nice defaults. The `vim9script` is optional, but the rest of this guide will assume you have it set.

The autocmd lines will set an indentation style for `*.vim` files. We're setting it here to make it cleaner to paste in other code from this guide.

The mappings will give you `Control-Shift-v` in gVim, which is the same as `Control-Shift-v` in Windows Terminal Vim. This is a convenience for putting (pasting) text from the Windows clipboard into Vim. If you put these keystrokes from Normal mode, Vim will put command strings (start with `:`) into the Vim command line.

# Install Cross-Platform PowerShell

There are two versions of PowerShell: Windows PowerShell 5 (blue icon) and cross-platform [PowerShell 7](https://github.com/PowerShell/PowerShell) (black icon). Windows comes with blue-icon PowerShell pre-installed, but if you open it, you will see a prompt to [Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindowswwin](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/migrating-from-windows-powershell-51-to-powershell-7?view=powershell-7.4). Ignore the link and run the following command in blue-icon PowerShell to install black-icon [PowerShell 7](https://github.com/PowerShell/PowerShell).

```powershell
winget install Microsoft.PowerShell --source winget
```

Once installed, [PowerShell 7](https://github.com/PowerShell/PowerShell) will be the default when you run Windows Terminal. You can run Windows Terminal by searching for it in the start menu or by holding the `windows key`, pressing `x`, then releasing both keys and pressing `i`. When I use the name "[PowerShell](https://github.com/PowerShell/PowerShell)" from here on, I am referring to cross-platform, black-icon, [PowerShell 7](https://github.com/PowerShell/PowerShell).

If [PowerShell 7](https://github.com/PowerShell/PowerShell) is not the default, or if you don't see black-icon [PowerShell](https://github.com/PowerShell/PowerShell) as a choice when adding a tab with the Windows Terminal down arrow in the tab bar, it's safe to go to

```
~\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState
```

and delete `settings.json` and `state.json`. They will almost instantly regenerate, leaving your Windows Terminal in a default configuration (which should include [PowerShell 7](https://github.com/PowerShell/PowerShell)). Of course, you'll lose any configuration you've done, but it was probably broken anyway. Make a backup if you're worried about it.

## configuration

If you don't already have a [PowerShell](https://github.com/PowerShell/PowerShell) config, create one by running

```powershell
new-item $profile -itemtype file
```

from [PowerShell](https://github.com/PowerShell/PowerShell). This will create a [PowerShell](https://github.com/PowerShell/PowerShell) profile at one of

```
~\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
~\OneDrive\Documents\PowerShell\Microsoft.Powershell_profile.ps1
```

### open a new PowerShell tab in the same directory

When you open a new tab in [PowerShell](https://github.com/PowerShell/PowerShell), that tab will be open to a system folder or your home directory, depending on how you have it configured. If you're working on a project in Vim, and you want to open a tab to run git or pre-commit or something else, then you probably want to open a new tab in the project directory.

[This page](https://learn.microsoft.com/en-us/windows/terminal/tutorials/new-tab-same-directory) explains how to configure PowerShell to open a new tab in the same directory as the current tab. It explains a few-dozen other approaches as well, so I'll excerpt the relevant information here.

Copy this code into your [PowerShell](https://github.com/PowerShell/PowerShell) profile:

```powershell
function prompt {
  $loc = $executionContext.SessionState.Path.CurrentLocation;

  $out = ""
  if ($loc.Provider.Name -eq "FileSystem") {
    $out += "$([char]27)]9;9;`"$($loc.ProviderPath)`"$([char]27)\"
  }
  $out += "PS $loc$('>' * ($nestedPromptLevel + 1)) ";
  return $out
}
```

Now, close and reopen [PowerShell](https://github.com/PowerShell/PowerShell), then press `Ctrl+Shift+D` (D for Duplicate) in [PowerShell](https://github.com/PowerShell/PowerShell) to to open a new tab in the same directory as the current tab.

### tell vim about PowerShell

Start [PowerShell](https://github.com/PowerShell/PowerShell) (`winkey+x` then `i`), open Vim inside [PowerShell](https://github.com/PowerShell/PowerShell), then add this to `~\vimfiles\vimrc`.

```
if has("win32")
  set shell=pwsh
  set termguicolors  # PowerShell is capable of TrueColor
  &t_8u = "\e[58:2::%lu:%lu:%lum"  # kludge for https://github.com/vim/vim/issues/20413
endif
```

... to let Vim know to open terminals in cross-platform [PowerShell](https://github.com/PowerShell/PowerShell). The options `shell=pwsh` and `shell=powershell` are not the same. The latter is for Windows (blue-icon) PowerShell, which may not be as nice an experience.

## termguicolors

Vim colorschemes usually define colors in three formats:

- `term`, a style name for monochrome terminals
- `ctermfg`, a color index for up to 256 color terminals
- `guifg`, a 24-bit (e.g., #008181) color definition for true-color terminals

If `termguicolors` is set, [PowerShell](https://github.com/PowerShell/PowerShell) will read the 24-bit color definition instead of looking for a color index. You'll really only notice this when plugins like [monkoose/vim9-stargate](https://github.com/monkoose/vim9-stargate) don't set `ctermfg`, because they assume you're on a TrueColor terminal. The `set termguicolors` line above will cover you either way.

### &t_8u

Vim uses an x-term escape sequence to set some terminal colors. Windows Terminal doesn't support this escape sequence. This line fixes every issue I've encountered with that. It's important, because it will break error formatting when we install [yegappan/lsp](https://www.github.com/yegappan/lsp) later in this guide.

## options

Vim is a terminal program, so options set in the terminal or shell will effect Vim. Open [PowerShell](https://github.com/PowerShell/PowerShell) in Windows Terminal (`win+x i`), press `Ctrl+,` for settings, and select [PowerShell](https://github.com/PowerShell/PowerShell) under `Profiles` in the left menu.

You may want to come back and select a different font after installing new fonts in the  [gVim Configuration](*gvim_configuration) section.

## "missing" shortcuts

Windows and Windows terminal will intercept some shortcuts before they reach Vim. For instance `ctrl-c`, `ctrl-v`, `ctrl-tab`, and `f11`. Some of this can be changed in configuration, but there are workarounds. `ctrl-v` in Vim is usually "blockwise Visual mode", but Windows users can use `ctrl-q` to get identical behavior. If you don't mind developing a little OS-specific muscle memory, `ctrl-shift-c` and `ctrl-shift-v` will copy and paste to the Windows clipboard, even in Vim. Be aware however, that this will *not* work in gVim without configuration.

To see if a shortcut is being intercepted before it gets to Vim, run `:echo getcharstr()` in Vim, then press the shortcut. If you see something like `^D` or `^Z`, then Vim is receiving the shortcut. If you see nothing, then it's being intercepted by Windows or Windows Terminal.

# Install Python

If you're reading this guide, you likely already have Python installed, but let's cover one straightforward way to do it.

```powershell
winget install Python.Python.3.13 --source winget
```

Winget will install Python and put both `~\AppData\Local\Programs\Python313` and `~\AppData\Local\Programs\Python313\Scripts\` in your path. Last time I checked, downloading and running the executable from [Python.org](https://www.python.org/downloads/) did not.

You may want to install other versions of Python, though this is becoming less common with tools like UV that can build an environment from any version of Python whether you have it installed on your system or not. Bear in mind that as you install other versions of Python, your "User variables" Path environment variable will find the latest (by install date, not by verision number) Python version first.

To avoid surprises, point Vim explicitly to the installed version you want to use. Add the following to `~\vimfiles\vimrc`:

```
if has("win32")
  set shell=pwsh
  set termguicolors  # PowerShell is capable of TrueColor
  &t_8u = "\e[58:2::%lu:%lu:%lum"  # kludge for https://github.com/vim/vim/issues/20413

  # ------------ new content
  var local_programs = expand('$LOCALAPPDATA/Programs')

  execute 'set pythonthreehome=' .. local_programs .. "/Python/Python313"
  execute 'set pythonthreedll=' .. local_programs .. "/Python/Python313/python313.dll"
  # ------------ / new content
endif
```

From Vim, run the command `:py3 print("test")` to make sure you have it set up correctly.

You may find that Vim and all your plugins "just work" without setting `pythonthreehome` and `pythonthreedll`. Vim knows where to look for a typical Python install. However, that could break at any time if you install a version of Python that Vim or one of your plugins does not support.

# Install Git

```powershell
winget install Git.Git --source winget
```

## configure git from PowerShell

Open [PowerShell](https://github.com/PowerShell/PowerShell) and run the following commands, replacing your user information.

```powershell
git config --global user.email "your@email.com"
git config --global user.name "Your Name"
git config --global core.editor "vim -f -i NONE"
git config --global merge.tool vimdiff
git config --global diff.tool vimdiff
git config --global core.excludesFile "$Env:USERPROFILE\.gitignore"
git config --global init.defaultBranch main
git config --global credential.https://github.com.username YourGitUsername
```

Don't let the `--global` flag misinform you. These are settings for one user. These commands update a file in your home directory called `.gitconfig`. You can edit this file later or re-run the commands if you don't like what I've put here, but these are the standard settings for Vim users.

You can also name your default branch whatever you like. If you don't configure it here, you'll get the default `master`. Git uses default `master`. [GitHub](https://github.com) uses default `main`. So, if you're using [GitHub](https://github.com), you'll save a bit of work by matching what they use there and setting it to `main`.

## other things that come with git

The installer will add `git` to your "System environment" Path (not your "User variables" Path). You will be able to run it from [PowerShell](https://github.com/PowerShell/PowerShell), so the distinction may not matter to you.

The Git installer also provides Curl and Bash. Curl will be on your path for plugins like [vim-instant-markdown](https://github.com/instant-markdown/vim-instant-markdown). You can add bash to your path or just create an alias in your [PowerShell](https://github.com/PowerShell/PowerShell) profile. It's not necessary for Vim, but it's convenient and already installed if you know Bash. Add this to your [PowerShell](https://github.com/PowerShell/PowerShell) profile.

```powershell
Set-Alias -Name bash -Value 'C:\Program Files\Git\bin\bash.exe'
```

# Install Ripgrep

"Grepping" is a big part of navigating through projects. In Windows, Vim will try to use a grep alternative. I don't remember the name. It works in cmd, but it freezes [PowerShell](https://github.com/PowerShell/PowerShell), so we don't want it. [Ripgrep](https://github.com/BurntSushi/ripgrep) is a nice alternative.

```powershell
winget install BurntSushi.ripgrep.MSVC --source winget
```

## tell Vim to use ripgrep

Add the following to your `~\vimfiles\vimrc` file. This will tell Vim to use [Ripgrep](https://github.com/BurntSushi/ripgrep) when you use the `:grep` command.

```
if has("win32")
  set shell=pwsh
  set termguicolors  # PowerShell is capable of TrueColor
  &t_8u = "\e[58:2::%lu:%lu:%lum"  # kludge for https://github.com/vim/vim/issues/20413

  var local_programs = expand('$LOCALAPPDATA/Programs')

  execute 'set pythonthreehome=' .. local_programs .. "/Python/Python313"
  execute 'set pythonthreedll=' .. local_programs .. "/Python/Python313/python313.dll"

  # ------------ new content
  if executable('rg')
    set grepprg=rg\ --vimgrep\ --no-heading
  else
    echoerr "rg not found. Install ripgrep to use :grep"
  endif
  # ------------ / new content
endif
```

Once you get everything set up, consider the [ctrl-sf](https://github.com/dyng/ctrlsf.vim) plugin, which will make use of your newly installed and nicely linked [ripgrep](https://github.com/BurntSushi/ripgrep).

# Install Node

This step is optional. If you need [Node](https://nodejs.org/) for [copilot.vim](https://github.com/github/copilot.vim) or another plugin, this is a good time to install it. There's not much to it, but it is a JavaScript runtime environment, and some people don't want that weight. Unless you're coming from something extraordinarily light, the editor you were using most likely installed [Node](https://nodejs.org/) without asking you. Your choice.

```powershell
winget install OpenJS.NodeJS.LTS --source winget
```

Run ...

```powershell
node -v
```

... in [PowerShell](https://github.com/PowerShell/PowerShell) to check the install.

## install yarn

Now that you have [Node](https://nodejs.org/) installed, optionally install the [Yarn](https://yarnpkg.com/) package manager if you want to run [vim-prettier](https://github.com/prettier/vim-prettier) or other tools that require [Yarn](https://yarnpkg.com/). You can skip this installation for now and come back to it if you need [Yarn](https://yarnpkg.com/) later. It's not necessary for any Python dev tasks, as far as I recall, but you may need to go deeper into the [Node](https://nodejs.org/) ecosystem if you end up working with common Python-adjacent filetypes like `html`, `css`, `markdown`, etc.

Start `Administrator:PowerShell`. You may have been starting [PowerShell](https://github.com/PowerShell/PowerShell) with `Winkey-x i`. Start `Administrator:PowerShell` with `Winkey-x a`. That is, hold `Winkey` and `x`, release both, then press `a`.

Enter the following command:

```powershell
corepack enable
```

Now, you can exit `Administrator:PowerShell` and open standard [PowerShell](https://github.com/PowerShell/PowerShell). Enter the following command:

```powershell
yarn -v
```

You will be prompted to allow `corepack` to install [Yarn](https://yarnpkg.com/). Allow this, and [PowerShell](https://github.com/PowerShell/PowerShell) will install [Yarn](https://yarnpkg.com/) then print a version number in the terminal window.

# Install Visual Studio Build Tools

This step is optional. It's a fairly big install, but you will need this for some Python libraries like [llama_index](https://github.com/run-llama/llama_index). If you're into things like that, you're going to need it at some point. You can start off by running

```powershell
winget install Microsoft.VisualStudio.2022.BuildTools --source winget
```

This takes several minutes, but only installs the Visual Studio Installer. Once that's done, run the Visual Studio Installer from the Windows menu.

- Click `Modify`.
- Select "Desktop development with C++".
- Click `Modify` again.

You could *probably* go into "Individual Components" and install "C++ CMake tools for Windows" and "Windows 11 SDK" only, but the entire "Workload" is only 1.75GB and it's not worth the hassle to figure out what you need and what you don't.

There's also a way, I'm sure, to [Use command-line parameters to install Visual Studio](https://learn.microsoft.com/en-us/visualstudio/install/use-command-line-parameters-to-install-visual-studio?view=vs-2022#use-winget-to-install-or-modify-visual-studio), but I'm not too proud to use the gui installer.

# Install Lazygit

This step is optional, but [Lazygit](https://github.com/jesseduffield/lazygit/) is fun and cool and useful. Like all Git interfaces, it's got [issues](https://github.com/jesseduffield/lazygit/issues)&mdash;as I write this, 666 open issues&mdash;but don't let the open issues put you off. As I said (and if you'll excuse a little fun with the coincidence), it's *the nature of the interface beast*&mdash;which may be a big part of the reason you're installing Vim in the first place (fewer interfaces).

```powershell
winget install JesseDuffield.lazygit --source winget
```

Close and restart your Windows Terminal, navigate to a Git project, and type [lazygit](https://github.com/jesseduffield/lazygit/) to have a look.

## difftastic

[Lazygit](https://github.com/jesseduffield/lazygit/) can be enhanced with [Difftastic](https://difftastic.wilfred.me.uk/), a Git diff viewer that will suppress many formatting-only diffs.

```powershell
winget install Wilfred.difftastic --source winget
```

Tell [Lazygit](https://github.com/jesseduffield/lazygit/) to use [Difftastic](https://difftastic.wilfred.me.uk/) by opening your [Lazygit](https://github.com/jesseduffield/lazygit/) config

```powershell
vim $env:LOCALAPPDATA\lazygit\config.yml
```

... and adding

```yaml
git:
  paging:
    externalDiffCommand: difft --color=always --display=inline --syntax-highlight=off
```

# Install GNU zip and unzip

[PowerShell](https://github.com/PowerShell/PowerShell) has `zip` and `unzip` equivalents, and Vim will use them if you have your shell set to 'pwsh', but not all file-browser plugins will. GNU-style `zip` and `unzip` are the standard and are slightly more powerful anyway.

To allow your Vim to browse and edit zip directories in (probably) any plugin ...

```powershell
winget install GnuWin32.Zip GnuWin32.UnZip --source winget
```

The installer will not add these to your Path. Add `C:\Program Files (x86)\GnuWin32\bin` to your user Path environment variable:

```
[Environment]::SetEnvironmentVariable("PATH", "$($env:PATH);C:\Program Files (x86)\GnuWin32\bin", [EnvironmentVariableTarget]::User)
```

# Install Vim Plugins

## enable Vim built-In plugins

Vim comes with a few packages, disabled by default, that you can optionally enable and use. A subset of these will be our first packages. Add the following to your `vimrc`:

```vim
# load Vim internal plugins
packadd! matchit  # jump between html tags with %
packadd! comment  # (un)comment lines with gc, gcc
```

Vim has a few more disabled-by-default packages, but each one is non-default for a reason. For instance, the built-in-but-disabled-by-default plugin `nohlsearch` *will* break [vim-ai](https://github.com/madox2/vim-ai) and other plugins.

## external plugins

Vim comes with [package support](https://vim-jp.org/vimdoc-en/repeat.html#packages), but not a package *manager*. I won't go into the nuances of that distinction. For now, it's easier to use a package manager, and you have plenty of choices.

We'll install [minpac](https://github.com/k-takata/minpac) to manage plugins through Vim's built-in [package support](https://vim-jp.org/vimdoc-en/repeat.html#packages), because it's simple and easy to install. From your `~/vimfiles` directory.

```powershell
git clone https://github.com/k-takata/minpac.git $env:USERPROFILE\vimfiles\pack\minpac\opt\minpac
```

Use the command above, not the `git clone` command from the [minpac](https://github.com/k-takata/minpac) GitHub page, because `%USERPROFILE%` (from the plugin README) doesn't mean anything to [PowerShell](https://github.com/PowerShell/PowerShell).

Now, add this to your `vimrc` file.

```vim
def PackInit(): void
  packadd minpac

  minpac#init()
  minpac#add('k-takata/minpac', {'type': 'opt'})
enddef

command! PackUpdate source $MYVIMRC | PackInit() | minpac#update()
command! PackClean  source $MYVIMRC | PackInit() | minpac#clean()
command! PackStatus packadd minpac | minpac#status()
```

Save and `:source %` your `vimrc` file, then `:PackUpdate` to check that everything is working.

# LSP

Add this plugin to the `PackInit` function you just created in your `vimrc`.

```vim
  # -------- language server protocol
  minpac#add('yegappan/lsp')
```

Here, we'll configure [Ruff](https://docs.astral.sh/ruff/) and [basedpyright](https://docs.basedpyright.com/) for Python files. Install these in whatever Python install you have set up for Vim.

```powershell
~\AppData\Local\Programs\Python\Python313\Scripts\pip install ruff basedpyright
```

Save your `vimrc` then run `:PackUpdate` to install the plugins. We're going to configure it before we test it. The paths will be simple (see config lines starting with `path:`) if the `Scripts` folder of your Python install is on your Path (it will be if you're following this guide). Add this to your `vimrc` file:

```vim
# -------------------------------------
# configure lsp
# -------------------------------------

nmap <leader>gd :LspGotoDefinition<CR>
nmap <leader>gr :LspShowReferences<CR>
nmap <leader>rn :LspRename<CR>
nmap <leader>gg :LspDiag current<CR>
nmap [g :LspDiag prevWrap<CR>
nmap ]g :LspDiag nextWrap<CR>
nmap K :LspHover<CR>

def g:RemoveBgFromLspGutterSymbols(): void
  hi LspDiagSignErrorText    guibg=NONE
  hi LspDiagSignWarningText  guibg=NONE
  hi LspDiagSignInfoText     guibg=NONE
  hi LspDiagSignHintText     guibg=NONE
enddef

augroup ClearLspGutterSymbolBackgrounds
  autocmd!
  autocmd ColorScheme * call g:RemoveBgFromLspGutterSymbols()
  autocmd User LspAttached call g:RemoveBgFromLspGutterSymbols()
  autocmd User LspDiagsUpdated call g:RemoveBgFromLspGutterSymbols()
augroup END

def RegisterLspServers(): void
  var lspOptions = {
    diagSignErrorText: '❌',
    diagSignWarningText: '🔶',
    diagSignInfoText: '🔵',
    diagSignHintText: '💡',
    semanticHighlight: 1,
  }
  lsp#options#OptionsSet(lspOptions)

  var lspServers = [
    {
      name: 'basedpyright',
      filetype: ['python'],
      path: 'basedpyright-langserver',
      args: ['--stdio'],
      workspaceConfig: {python: {pythonPath: exepath('python')}}
    },
    {
      name: 'ruff',
      filetype: ['python'],
      path: 'ruff.exe',
      args: ['server'],
      features: {hover: false}
    }
  ]
  lsp#lsp#AddServer(lspServers)

  g:RemoveBgFromLspGutterSymbols()
enddef

autocmd User LspSetup call RegisterLspServers()
```

My goal is not to specify shortcuts and specific configuration for each plugin, but [yegappan/lsp](https://www.github.com/yegappan/lsp) settings are particular about order, and I want to give you this one working example as a guide.

Restart Vim, open a Python file, and type `:LspShowAllServers` to confirm that both `basedpyright` and `ruff` are running.

You should see something like this:

```
Filetype Information
====================
Filetype: 'python'
Server Name: 'basedpyright'
Server Path: 'basedpyright-langserver'
Status: Running

Filetype: 'python'
Server Name: 'ruff'
Server Path: 'ruff.exe'
Status: Running

Buffer Information
==================
Buffer: 'my_file.py'
Server Path: 'pyright-langserver'
Status: Running
Server Path: 'ruff.exe'
Status: Running
```

# Artificial Intelligence

These services cost money.

Return again to the `PackInit` function in your `vimrc` and add three more plugins.

```vim
  # -------- ai completion and chat
  minpac#add('ShayHill/copilot.vim')
  minpac#add('madox2/vim-ai', {do: '!python -m pip install "openai>=0.27"'})
  minpac#add('rishi-opensource/vim-claude-code')
```

I will refer you to the plugin pages for instructions on registering the first two and setting the required environment variables. The instructions on each are simple and clear. I couldn't improve them.

- [github/copilot.vim](https://github.com/github/copilot.vim)
- [madox2/vim-ai](https://github.com/madox2/vim-ai)

Each provides several commands you can type at the command line or create a mapping for. That is the usual process in Vim: review the many available commands and create mappings for the ones you use most frequently. You can browse these commands by typing `:Copilot<space><tab>` or `:AI<tab>` in Vim.

## Copilot

Why `ShayHill/copilot.vim` and not `github/copilot.vim`? I forked the original and reverted to 1.41.0, the last version that works with Vim + Windows + [PowerShell 7](https://github.com/PowerShell/PowerShell).

## Chat

Have a close look at the `minpac#add` line for [vim-ai](https://github.com/madox2/vim-ai). [Minpac](https://github.com/k-takata/minpac) will install the `openai` library in whatever Python Vim is using. You may be able to avoid that, but you're going to need a more elaborate hook and some configuration elsewhere. That's up to you, but I wanted to draw your attention to it.

## Claude Code

Install [Claude Code](https://www.anthropic.com/claude) with winget in [PowerShell](https://github.com/PowerShell/PowerShell):

```powershell
winget install Anthropic.ClaudeCode --source winget
```

# Snippets

Once again, return to the `PackInit` function in your `vimrc`. Add this:

```vim
  # -------- snippets
  minpac#add('SirVer/ultisnips')
```

Don't forget to run `:PackUpdate` and restart Vim to make sure the new plugin directory is sourced.

Add some mappings to the bottom of your `vimrc`.

```vim
# -------------------------------------
#  configure ultisnips
# -------------------------------------

g:UltiSnipsExpandTrigger = "<C-l>"
g:UltiSnipsJumpForwardTrigger = "<C-d>"
g:UltiSnipsJumpBackwardTrigger = "<C-u>"
```

Now, you'll need some snippets. Plenty of documentation on this if you start at [SirVer/ultisnips: UltiSnips](https://github.com/SirVer/ultisnips). Let's walk through a simple example.

## create a snippet

In Windows, you'll need to explicitly create a snippets folder at

```
~\vimfiles\ultisnips
```

Just to see how it works, let's do that with Vim's `netrw` file browser.

- type `:Ex<enter>`
- press `d`
- type `ultisnips<enter>`
- type `:bd<enter>` to exit netrw

Now, UltiSnips will recognize this as your snippets directory. Open a Python file. If you don't have one handy, just `:e temp.py`. From the Python file, enter `:UltiSnipsEdit`. UltiSnips will open a file at

```
~\vimfiles\ultisnips\python.snippets
```

Enter this:

```
snippet docmod "module docstring" b
"""$1

:author: Your Name Here
:created: `!v strftime("%Y-%m-%d")`
"""
$2
endsnippet
```

Save, return to your Python file, and try out the snippet using the mappings you defined in this section. Type `docmod<C-l>`.

# Debugging

Vim uses the same debugging engine as VS Code and probably several others. To use it, you'll need a plugin and a json configuration.

Return to the `PackInit` function in your `vimrc`. Add this:

```vim
  # -------- debugging
  minpac#add('puremourning/vimspector')
```

Don't forget to run `:PackUpdate` and restart Vim to make sure the new plugin directory is sourced.

Select a set of mappings at the bottom of your `vimrc`.

```vim
# -------------------------------------
#  configure vimspector
# -------------------------------------

g:vimspector_enable_mappings = 'HUMAN'
# F10 and F11 (mapped by Vimspector) are intercepted by Windows Terminal
nmap <C-F10> <Plug>VimspectorStepOver
nmap <C-F11> <Plug>VimspectorStepInto
g:vimspector_base_dir = $MYVIMDIR .. 'pack\minpac\start\vimspector'
```

## .vimspector.json

Vimspector will need a configuration file. Once you get accustomed to reading and editing this file, you will probably want to shape it in different ways for each project.

The most straightforward way to handle configuration is to put a `.vimspector.json` file in *each* project folder. That way, you can make project-specific changes without additional complexity. We will copy this into a file in the next section.

```json
{
    "$schema": "https://puremourning.github.io/vimspector/schema/vimspector.schema.json",
    "configurations": {
        "run": {
            "adapter": "debugpy",
            "configuration": {
                "name": "run this Python file",
                "request": "launch",
                "type": "python",
                "cwd": "${workspaceRoot}",
                "python": "${workspaceRoot}/.venv/Scripts/python.exe",
                "program": "${file}",
                "pythonArgs": ["-Xfrozen_modules=off"]
            },
            "breakpoints": {
                "exception": {
                    "raised": "N",
                    "caught": "N",
                    "uncaught": "Y",
                    "userUnhandled": "N"
                }
            }
        },
        "run - main.py": {
            "adapter": "debugpy",
            "configuration": {
                "name": "run main.py",
                "request": "launch",
                "type": "python",
                "cwd": "${workspaceRoot}",
                "python": "${workspaceRoot}/.venv/Scripts/python.exe",
                "program": "${workspaceRoot}/src/example_python_project/main.py",
                "pythonArgs": ["-Xfrozen_modules=off"]
            },
            "breakpoints": {
                "exception": {
                    "raised": "N",
                    "caught": "N",
                    "uncaught": "Y",
                    "userUnhandled": "N"
                }
            }
        },
        "test": {
            "adapter": "debugpy",
            "configuration": {
                "name": "run this test file",
                "module": "pytest",
                "type": "python",
                "request": "launch",
                "cwd": "${workspaceRoot}",
                "python": "${workspaceRoot}/.venv/Scripts/python.exe",
                "pythonArgs": ["-Xfrozen_modules=off"],
                "args": [
                    "-q",
                    "${file}"
                ]
            },
            "breakpoints": {
                "exception": {
                    "raised": "N",
                    "caught": "N",
                    "uncaught": "Y",
                    "userUnhandled": "N"
                }
            }
        }
    }
}
```

There's a lot of text there. I have simplified it by following a few conventions like always naming my virtual environment folder `.venv` and my main Python file `main.py`.

Whatever you do, it's going to be a lot of text. If you look at the second configuration, "run main.py", you'll see a simple example of how you might edit your `.vimspector.json`. The value ...

```json
"program": "${workspaceRoot}/src/example_python_project/main.py",
```

... should be the path to a main project file. You can get deep into configuration. Start at [puremourning/vimspector](https://github.com/puremourning/vimspector) and read the documentation when you're ready. For now, you can go a long way just by editing the configuration I've provided.

## run Vimspector

First, create an example Python project. I'm going to create my example inside my `~\vimfiles` folder so I can more easily host this tutorial on [GitHub](https://github.com). From [PowerShell](https://github.com/PowerShell/PowerShell)

```powershell
mkdir ~\vimfiles\example_python_project
cd ~\vimfiles\example_python_project
py -m venv .venv
```

Create `~\vimfiles\example_python_project\.vimspector.json` with the json code under the previous heading. To do that in a [PowerShell](https://github.com/PowerShell/PowerShell) way, scroll back, copy the code to your clipboard, then enter this in [PowerShell](https://github.com/PowerShell/PowerShell):

```powershell
Get-Clipboard | Set-Content -Path "~\vimfiles\example_python_project\.vimspector.json"
```

We'll need something to debug, so open `~\vimfiles\example_python_project\main.py` in gVim and write a little Python code.

```python
def hello_world():
    greeting = "Hello, world!"
    print(greeting)

if __name__ == "__main__":
    hello_world()
```

Remember to save the `main.py` with `:w`, then press `f5` to launch vimspector. Vimspector will prompt you to select a configuration.

```
Which launch configuration?
1: run
2: run - main.py
3: test
```

Select `run` by pressing `1<enter>`, and Vimspector will prompt

```
The specified adapter 'debugpy' is not installed. Would you like to install the following gadgets? debugpy
```

Press Enter, and vimspector will install debugpy (in `pythonthreehome`) then launch the vimspector tab. You can experiment with it now, or `:call vimspector#Reset()` to get out and come back later.

# Fuzzy Finding

By now, I suspect you know the steps. Return to the `PackInit` function in your `vimrc`. Add this:

```vim
  # -------- fuzzy finder
  minpac#add('vim-fuzzbox/fuzzbox.vim')
```

Don't forget to run `:PackUpdate` and restart Vim to make sure the new plugin directory is sourced.

`:Fuzz<tab>` to see the commands. The most common may be `:FuzzyyGitFiles`. You likely want a mapping for it. Add this to `~\vimfiles\plugin_config.vim`:

```vim
# -------------------------------------
#  configure fuzzbox.vim
# -------------------------------------

nnoremap <C-P> :FuzzyGitFiles<CR>
inoremap <C-P> <ESC>:FuzzyGitFiles<CR>
```

Don't expect that to do much right now unless you're in a git directory with `git add`-ed files, but it will help you quickly navigate through your project later on.

*But what if I want to open a file that isn't controlled by Git?*

Everyone has opinions. My opinion is this: save keystrokes and use the best shortcuts for the things you do (like opening a Git controlled file) hundreds of times a day. For less common tasks, worry less about efficiency. That means open the non-Git-controlled file with `:e`, `:Ex`, `:FuzzyFiles` or a shortcut (that you may not even remember) to one of those. This keeps your hundreds-of-times-a-day functions uncluttered and top of mind.

Additionally, avoid the bad habit of using a fuzzy finder to switch between a handful of files. `:h mark-motions` for the most straightforward way to accomplish that in Vim.

# The Usual Suspects

There are several [Tim Pope](https://github.com/tpope) plugins that could qualify as "the usual suspects". These are so common that it's all-but taken for granted that you have them installed. Some form of [vim-easymotion](https://github.com/easymotion/vim-easymotion) is also common, so common that the behavior is usually implemented in browser and editor "Vim modes". I use [easyjump.vim](https://github.com/girishji/EasyJump.vim).

```vim
  # -------- the usual suspects
  minpac#add('tpope/vim-dispatch')  # async build
  minpac#add('tpope/vim-fugitive')  # git integration
  minpac#add('tpope/vim-obsession')  # session management
  minpac#add('girishji/EasyJump.vim')  # easymotion alternative
```

- [vim-dispatch](https://github.com/tpope/vim-dispatch)
- [fugitive.vim](https://github.com/tpope/vim-fugitive)
- [vim-obsession](https://github.com/tpope/vim-obsession)
- [easyjump.vim](https://github.com/girishji/EasyJump.vim)

At some point, you'll want to review the documentation for all of these, but the only one we'll rely on for this guide is vim-dispatch. [vim-dispatch](https://github.com/tpope/vim-dispatch) allows you to `make` (compile) programs asynchronously. This guide is focused on Python dev, and we don't compile Python programs, but we will use vim-dispatch's `Make` command to run [pre-commit](https://pre-commit.com/) (a common Python tool) asynchronously.

# Vim Configuration

Too many options to discuss, but we'll "scratch the surface" with a few examples.

```vim
:e $MYVIMRC
```

Two settings and one leader mapping.

```vim
set number  # turn on line numbers
set belloff=all  # turn off the error bell

# remove trailing whitespace
nnoremap <leader>_ :%s/\s\+$//g<CR>
```

These settings and mappings will apply to all filetypes, but can be overwritten with file-specific settings in the `~\vimfiles\after\ftplugin` folder.

# gVim Configuration

We're going to do some light configuration in gVim, less to configure it, more to walk through a few concepts.

If you are running gVim, gVim will read an additional configuration file, `gvimrc`, after reading your `vimrc`. Open `gvimrc` in gVim.

```powershell
gvim ~\vimfiles\gvimrc
```

And paste in this content:

```vim
vim9script

# if you can't see the below characters, get a better font
set listchars=tab:→\ ,eol:↵,trail:·,extends:↷,precedes:↶
```

The `listchars` value isn't the most important part of your gVim configuration, but we're starting here for a reason. Inside gVim, look at the line beginning with `set listchars` and chances are you won't be able to see all of the characters.

## set gVim guifont

Start gVim then launch a gui menu to select an available font.

```vim
:set guifont=*
```

You might find a font that shows the characters and looks nice to your tastes, but possibly not.

### install another font

Let's install a nice-looking (to my taste, at least) font with these "extra" characters. To accomplish this, we will install a font for the entire Windows system, then select that font in gVim. Go to [Release dejavu-fonts-2.37 · dejavu-fonts/dejavu-fonts · GitHub](https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37), download `dejavu-fonts-ttf-2.37.zip`, extract the contents, right click on `DejaVuSansMono.ttf` (it's in one of the subfolders), and install. You will now be able to select `DejaVu Sans Mono` in the gVim font menu.

### setting the guifont

Your font selection has a special name that gVim will understand. You can see it by typing

```vim
:set guifont
```

Now, let's capture the output of `:set guifont`. Open your `gvimrc`, place your cursor on an empty line, and type this command:

```vim
:call append('.', 'set guifont=' .. &guifont)
```

This will insert the following into your `gvimrc`.

```vim
set guifont=DejaVu_Sans_Mono:h10:cANSI:qDRAFT
```

Keep that line in `~/vimfiles/gvimrc` and your font selection will persist. If you open gVim on a system without `DejaVu Sans Mono`, gVim will revert to the default font. If you'd like to choose your own fallback, you  can list as many fonts as you like, separated by commas. gVim will start with the first and search for an available font.

```vim
set guifont=Consolas:h10:cANSI:qDRAFT,SimSun-ExtB:h11:cANSI:qDEFAULT,DejaVuSansMono_NFM:h10:cANSI:qDRAFT
```

`:set list!` if you want to see your `listchars` in action. `:set list!` again to turn it off.

## updating the terminal font

You may want to go back and change the Windows Terminal font through the Windows Terminal settings dialog, but those changes will affect all terminal programs. If you'd rather keep your current terminal font, you can set a simpler `listchars` for Vim. In your `vimrc` ...

```vim
set listchars=tab:>\ ,trail:-,extends:>,precedes:<,nbsp:+
```

## renderoptions

If you paste the following into Vim (running in [PowerShell](https://github.com/PowerShell/PowerShell)), you will see what you see in your browser: a colorful Unicode garden.

```
# symbols for render test
# 🌸 (U+1F338) 🌼 (U+1F33C) 🌻 (U+1F33B) 🌺 (U+1F33A) 🌹 (U+1F339)
# 🌷 (U+1F337) 💐 (U+1F490) 🌲 (U+1F332) 🌳 (U+1F333) 🌴 (U+1F334)
# 🌵 (U+1F335) 🌿 (U+1F33F) 🌱 (U+1F331) 🍀 (U+1F340) 🍁 (U+1F341)
# 🍂 (U+1F342) 🍃 (U+1F343) 🍎 (U+1F34E) 🍏 (U+1F34F) 🍐 (U+1F350)
# 🍊 (U+1F34A) 🍋 (U+1F34B) 🍌 (U+1F34C) 🍉 (U+1F349) 🍇 (U+1F347)
# 🍓 (U+1F353) 🍒 (U+1F352) 🍑 (U+1F351) 🥝 (U+1F95D) 🍍 (U+1F34D)
# 🥥 (U+1F965) 🍅 (U+1F345) 🍆 (U+1F346) 🥑 (U+1F951) 🥒 (U+1F952)
# 🌽 (U+1F33D) 🥕 (U+1F955) 🥔 (U+1F954) 🧄 (U+1F9C4) 🧅 (U+1F9C5)
```

If you paste this text into gVim, the result will be considerably less interesting. To get nice, colorful symbols, tell gVim to use the same DirectX rendering as [PowerShell](https://github.com/PowerShell/PowerShell). Add this to your `gvimrc`:

```vim
set renderoptions=type:directx,gamma:1.0,geom:0,renmode:5,taamode:1
```

## window size

While we're here, let's add another common gVim configuration request. This one is passive, so you won't have any new commands to learn. Add this to your `gvim.vimrc`.

```vim
# open at a useful size
if !exists('g:vimrc_sourced')
  g:vimrc_sourced = 1
  set lines=50
  set columns=120
endif
```

gVim will now open at 120 columns and 50 lines. Adjust those numbers to your tastes.

# The Vim ftplugin Directory

Naturally, Vim doesn't treat every filetype the same. Set specific configuration variables in

```
~\vimfiles\after\ftplugin
```

Vim will read two `ftplugin` directories:

- Settings in `~\vimfiles\ftplugin` are sourced before plugins are loaded. So, they will affect plugins and can be overwritten by plugins.
- Settings in `~\vimfiles\after\ftplugin` will load plugins without any of these settings and will overwrite any settings made in plugins.

## configure Vim for Python files

```powershell
mkdir ~\vimfiles\after
mkdir ~\vimfiles\after\ftplugin
vim ~\vimfiles\after\ftplugin\python.vim
```

Enter and adjust to your preference.

```vim
vim9script

setlocal colorcolumn=89  # max cols in black is 88
setlocal textwidth=88  # wrapping for gq (for comments and docstrings)
```

You may prefer to put either of these in your global `vimrc` so they apply to all files. If you're keeping them here, use `setlocal` instead of `set` so they *stop* applying when you edit something that *isn't* a Python file.

As an example, let's create a map to run our test suite in Vim's integrated terminal. Notice the `<buffer>` flag. Like `setlocal`, `<buffer>` keeps configuration local to a file. In this case, every file with a *python* filetype.

```vim
nnoremap <buffer> <leader>t :update<CR>:vert term python -m pytest<t_ku>
```

This mapping will

- save the current buffer
- start a command with `:!python -m pytest`
- press up to reload the previous `:!python -m pytest` command
- then nothing

The mapping will not run the command, but will wait for you to

- optionally navigate through the history of commands starting with `:!python -m pytest` by using the arrow keys
- press Enter

There are several ways to navigate command history in Vim. This one is given as an example.

## configure the aichat window

The [madox2/vim-ai](https://github.com/madox2/vim-ai) plugin creates a new filetype for its AI chat window. From any Vim window (split), run `:set filetype<CR>` to see the filetype. Configure any filetype by creating a file at `~\vimfiles\after\ftplugin\[filetype].vim`.

```vim
:e $MYVIMDIR\after\ftplugin\aichat.vim
```

```vim
vim9script

setlocal wrap
setlocal linebreak

# Make the AI chat window behave like ChatGPT, Grok, Discord, etc.
# <Enter> submits a query / post; <Shift-Enter> creates a new line.
nnoremap <buffer> <Enter> :AIChat<CR>
inoremap <buffer> <Enter> <Esc>:AIChat<CR>
nnoremap <buffer> <S-Enter> <Enter>
inoremap <buffer> <S-Enter> <Enter>
```

# The Vim compiler Directory

Vim uses the `make` command to run compilers and other tools. `*.vim` files in the `complier` directory define how compilers are called and how the output is displayed.

Python isn't a compiled language, but Python developers can can borrow `make` ( we'll use the asynchronous `Make` in [tpope/vim-dispatch](https://github.com/tpope/vim-dispatch)) to lint and fix our Python files.

## asynchronous pre-commit

Set up a mapping to run `pre-commit` asynchronously in Vim's `quickfix` window. To do this, define a compiler in `$MYVIMDIR/compiler`.

```vim
:e $MYVIMDIR\compiler\precommit.vim
```

Add this content to `~\vimfiles\compiler\precommit.vim`:

```vim
vim9script

CompilerSet makeprg=pre-commit\ run

# mypy
CompilerSet errorformat=%f:%l:\ %m

# ruff
CompilerSet errorformat+=%E%m\ %#-->\ %f:%l:%c

# pyright
CompilerSet errorformat+=%f:%l:%c\ -\ %m
```

Add this content to `~\vimfiles\after\ftplugin\python.vim`:

```vim
def g:RunPrecommit(): void
  compiler precommit
  update
  Make
enddef

nmap <buffer> <leader>l :call RunPrecommit()<CR>
```

Now you can press `<leader>l` from a Python module to run your pre-commit hooks. This requires [vim-dispatch](https://github.com/tpope/vim-dispatch).

# More

At this point, *your OS and various APIs* are a high-functioning IDE. You may still want to put some work into your editor, but that will be the easy part. Vim has great documentation available with `:h topic` if you know what you're looking for. If you're not sure what you're looking for, try `:FuzzyHelp` to search the help files with the [fuzzbox](https://github.com/vim-fuzzbox/fuzzbox.vim) plugin we just installed.

It's a common thing to commit your Vim configuration and even to keep it public. Here's mine: [ShayHill/vimfiles](https://github.com/ShayHill/vimfiles). Here's famous Vim user Tim Pope's config: [tpope/dotfiles](https://github.com/tpope/dotfiles). Remember that it's never finished. Enjoy the process.

# TL;DR?

If you already have a setup you're happy with, these might help with any nagging issues.

- Install [PowerShell 7](https://github.com/PowerShell/PowerShell)  # Vim in PowerShell 5 and CMD are tougher. "My OS is my IDE" doesn't with WSL.

```powershell
winget install Microsoft.PowerShell --source winget
```

- Install GNU zip and unzip  # Plugins look for these

```powershell
winget install GnuWin32.Zip GnuWin32.UnZip --source winget
[Environment]::SetEnvironmentVariable("PATH", "$($env:PATH);C:\Program Files (x86)\GnuWin32\bin", [EnvironmentVariableTarget]::User)
```

- Don't use the latest Copilot. Lock version at 1.4.1 or clone [ShayHill/copilot.vim](https://github.com/ShayHill/copilot.vim)
- in `vimrc` (in this order):

```vim
set shell=pwsh
set termguicolors
&t_8u = "\e[58:2::%lu:%lu:%lum"  # fix spelling and `yegappan/lsp` error rendering
```

- Install [DejaVuSansMono.ttf](https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37)  # A fixed-width font with plenty of symbols and dotted 0
- in `gvimrc`:

```vim
set guifont=DejaVu_Sans_Mono:h10:cANSI:qDRAFT
set renderoptions=type:directx,gamma:1.0,geom:0,renmode:5,taamode:1  # better symbol colors
```

- Clone minpac with this instead of the command on the GitHub page:

```powershell
git clone https://github.com/k-takata/minpac.git $env:USERPROFILE\vimfiles\pack\minpac\opt\minpac
```

