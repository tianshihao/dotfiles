# Configuration Sync Manager

## Introduction

The Configuration Sync Manager is a Python utility designed to synchronize configuration files across different environments. It supports conditional synchronization based on the operating system, allowing users to maintain consistent settings across Windows, Linux, and macOS. The tool reads configurations from a `settings.json` file, which specifies the source and target directories for each configuration, as well as whether the synchronization should be enabled for each platform.

## Usage

### Setting Up

1. Ensure Python is installed on your system.
2. Place your configuration settings in the `settings.json` file following the provided structure.

### Running the Tool

To use the Configuration Sync Manager, navigate to the directory containing `manager.py` and run one of the following commands in your terminal:

- **Dispatch Configurations to Host:**

  ```bash
  python3 manager.py --dispatch
  ```

  This command copies the specified configurations to their target locations on the host machine.

- **Retrieve Configurations from Host:**

  ```bash
  python3 manager.py --retrieve
  ```

  _(Functionality to be implemented)_ This command would retrieve configurations from the host machine back to the source directory.

- **Merge Configurations:**

  ```bash
  python manager.py --merge
  ```

  _(Functionality to be implemented)_ This command would merge configurations between the host and the repository.

- **Help:**

  ```bash
  python3 manager.py --help
  ```

  This command displays the available options and usage instructions.

### Configuration File (`settings.json`)

The `settings.json` file contains the configurations to be synchronized. Each configuration specifies a name, whether it's enabled, and platform-specific settings including the source and target directories. Here's an example structure:

```json
{
  "configurations": [
    {
      "name": "fish",
      "enable": true,
      "platform": {
        "Windows": {
          "source": "fish",
          "target": "",
          "enable": false
        },
        "Linux": {
          "source": "fish",
          "target": "~/.config",
          "enable": true
        },
        "Darwin": {
          "source": "fish",
          "target": "~/.config",
          "enable": true
        }
      }
    }
  ]
}
```

Ensure the `enable` flag is set to `true` for each platform you wish to synchronize configurations for.

### Commitizen

```bash
sudo apt install -y node
sudo apt install -y npm
npm install -g commitizen
commitizen init cz-emoji-conventional --save-dev --save-exact --force
```