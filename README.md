# Dotfiles Manager

## Introduction

Dotfiles Manager is a Python tool for synchronizing configuration files (dotfiles) across Linux, macOS, and Windows.  
All sync rules are managed in a single `settings.json` file, allowing flexible specification of which configs to sync, platform-specific paths, and files to exclude.  
This makes it easy to quickly restore a development or work environment on any new machine.

---

## Quick Start

1. **Prepare the environment**

   - Requires Python 3.
   - Clone this repo and edit `settings.json` as needed.

2. **Sync configs to the machine (from repo to system)**

   ```bash
   python3 manager.py --dispatch
   ```

3. **Collect configs from the machine (from system to repo)**

   ```bash
   python3 manager.py --retrieve
   ```

4. **Show help**
   ```bash
   python3 manager.py --help
   ```

---

## Configuration File (`settings.json`)

Each application can have multiple configuration items.  
Each item can specify type (`file` or `directory`), host path, repo path, excludes, and platform-specific settings.

**Example 1: Syncing a single file**

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

**What happens on different platforms:**

- **Linux/macOS**
  - `dispatch`: Copies `.vimrc` from the repo to `~/.vimrc` on the system.
  - `retrieve`: Copies `~/.vimrc` from the system to `.vimrc` in the repo.
- **Windows**
  - `dispatch`: Copies `.vimrc` from the repo to `~/_vimrc` on the system.
  - `retrieve`: Copies `~/_vimrc` from the system to `.vimrc` in the repo.

---

**Example 2: Syncing a directory**

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

- **Linux/macOS**
  - `dispatch`: Copies the entire `.config/kitty` directory from the repo to `~/.config/kitty` on the system, skipping any files listed in `excludes` (e.g., `kitty.conf.bak`).
  - `retrieve`: Copies `~/.config/kitty` from the system to `.config/kitty` in the repo, skipping excluded files.
- **Windows**
  - Unless a `windows` override is specified, the same logic applies, but a different path or disabling sync for Windows can be set using the `windows` key.

---

- Platform keys use lowercase (e.g. `"windows"`, `"darwin"`, `"linux"`).
- Use `excludes` to skip files or directories not to be synced.
- Set `enable: false` to skip syncing on a specific platform.

---

## Commitizen Setup & Usage

### What is Commitizen?

Commitizen helps standardize git commit messages, which is useful for teams or for automating changelog generation.

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

- Only add `package.json` and `package-lock.json` to git. **Do not commit `node_modules/`.**
- Add to `.gitignore`:
  ```
  node_modules/
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
