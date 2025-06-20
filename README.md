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
   ```

   Shows what will be copied, which items are enabled, and the paths for your system.

3. **Copy files from your computer back to the repo**

   ```bash
   python3 -m src.main --retrieve
   ```

4. **Copy files from the repo to your computer**

   ```bash
   python3 -m src.main --dispatch
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
