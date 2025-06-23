# Dotfiles Manager

## Introduction

Dotfiles Manager is a Python tool for syncing your dotfiles across Linux, macOS, and Windows. All rules are in `settings.json`. You choose what to sync, set different paths for each system, and pick files to skip. This helps you set up your work or dev environment on any computer fast.

---

## Quick Start

1. **Get ready**

   - Needs Python 3.
   - Clone this repo and edit `settings.json` as you like.

2. **See what will be copied**

   ```bash
   python3 -m src.main --overview
   # for a specified app(e.g. nvim)
   python3 -m src.main --overview --app nvim
   # for multiple apps(e.g. nvim, vim)
   python3 -m src.main --overview --app nvim vim
   ```

   Shows what will be copied, which items are enabled, and the paths for your system.

3. **Copy files from your computer back to the repo**

   ```bash
   python3 -m src.main --retrieve
   # for a specific app
   python3 -m src.main --retrieve --app nvim
   # for multiple apps
   python3 -m src.main --retrieve --app nvim vim
   ```

4. **Copy files from the repo to your computer**

   ```bash
   python3 -m src.main --dispatch
   # for a specific app
   python3 -m src.main --dispatch --app nvim
   # for multiple apps
   python3 -m src.main --dispatch --app nvim vim
   ```

5. **Show help**
   ```bash
   python3 -m src.main --help
   ```

---

## settings.json

You list your programs in `settings.json`. Each program can have many items. Each item can be a file or a folder. You set where it is on your computer, where it is in the repo, what to skip, and special rules for each system.

**Example 1: Copy one file**

```json
{
  "applications": [
    {
      "name": "vim",
      "enable": true,
      "configurations": [
        {
          "type": "file",
          "path_on_host": "~/.vimrc",
          "path_in_repo": ".vimrc",
          "windows": {
            "path_on_host": "~/_vimrc"
          }
        }
      ]
    }
  ]
}
```

**What happens:**

- On Linux or macOS: `.vimrc` is copied between the repo and `~/.vimrc`.
- On Windows: `.vimrc` is copied between the repo and `~/_vimrc`.

---

**Example 2: Copy a folder**

```json
{
  "applications": [
    {
      "name": "kitty",
      "enable": true,
      "configurations": [
        {
          "type": "directory",
          "path_on_host": "~/.config/kitty",
          "path_in_repo": ".config/kitty",
          "excludes": ["kitty.conf.bak"]
        }
      ]
    }
  ]
}
```

**What happens:**

- The whole `.config/kitty` folder is copied, skipping files in `excludes`.
- You can set different rules for Windows, macOS, or Linux with the keys `windows`, `darwin`, `linux`.

---

- Use lowercase for system keys.
- Use `excludes` to skip files or folders.
- Set `enable: false` to skip a program or a system.
- **Use `--app <name1> <name2> ...` to operate on one or more specific applications (e.g. nvim, vim, kitty, etc).**

---

## Commitizen

Commitizen helps you write git commit messages in a standard way. This is good for teams or making changelogs.

### How to set up

#### 1. If Node.js and npm are not installed

First, install Node.js and npm:

```bash
sudo apt update
sudo apt install -y nodejs npm
```

#### 2. If Node.js and npm are already installed

In the dotfiles repo directory:

```bash
npm install --save-dev commitizen
npx commitizen init cz-emoji-conventional --save-dev --save-exact --force
```

#### 3. How to use on a new machine

1. Clone the dotfiles repo.
2. Run:
   ```bash
   npm install
   ```
3. Use Commitizen to commit:
   ```bash
   npx cz
   ```
   or
   ```bash
   npx commitizen
   ```

---

## Changelog with Emoji Commits

If you use cz-emoji-conventional (emoji commit style), use the following method to generate a changelog that recognizes emoji commits:

1. Install the tools (globally or with npx):
   ```bash
   npm install -g conventional-changelog-cli conventional-changelog-emoji
   # or just use npx without global install
   # npx conventional-changelog -p emoji -i CHANGELOG.md -s
   ```
2. Generate or update your changelog:
   ```bash
   npx conventional-changelog -p emoji -i CHANGELOG.md -s -r 0
   ```

This will parse your cz-emoji-conventional commit messages and generate a changelog with emoji support.

If your changelog is empty, make sure your commit messages follow the emoji conventional format (e.g. `✨ feat: ...`).
