      ````
                        ┌───────────────────────────────────────────────────────┐
                        │ ███╗   ██╗███████╗ ██████╗ ██████╗ ██╗   ██╗████████╗ │
                        │ ████╗  ██║██╔════╝██╔════╝██╔═══██╗██║   ██║╚══██╔══╝ │
                        │ ██╔██╗ ██║███████╗██║     ██║   ██║██║   ██║   ██║    │
                        │ ██║╚██╗██║╚════██║██║     ██║   ██║██║   ██║   ██║    │
                        │ ██║ ╚████║███████║╚██████╗╚██████╔╝╚██████╔╝   ██║    │
                        │ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝    ╚═╝    │
                        └───────────────────────────────────────────────────────┘
````

<p align="center">
  <em>A fast, metadata-rich PyPI name inspector</em>
</p>

<p align="center">
  <a href="https://pypi.org/project/nscout/"><img src="https://img.shields.io/pypi/v/nscout?color=4caf50&label=PyPI%20" alt="PyPI Version"></a>
  <a href="https://pypi.org/project/nscout/"><img src="https://img.shields.io/pypi/pyversions/nscout?color=2196f3" alt="Python Versions"></a>
  <a href="https://github.com/"><img src="https://img.shields.io/badge/license-MIT-purple.svg" alt="License"></a>
  <a href="https://pypi.org/project/nscout/#files"><img src="https://img.shields.io/badge/downloads-not%20yet%20tracked-lightgrey"></a>
</p>

<p align="center">
  nscout checks PyPI and TestPyPI availability, extracts rich metadata,<br>
  formats results into clean readable tables, and integrates perfectly into<br>
  CI environments via JSON output.<br>
  Blazing-fast in-memory caching keeps repeated lookups instant.
</p>

---
## nscout is designed to be:
- quick to use  
- informative out of the box  
- script-friendly  
- safe for automation (JSON mode, quiet mode)  
- ideal for package authors checking names before publishing  

---

## Why nscout?

Choosing a package name sounds simple — until PyPI tells you it isn’t.  
With more than half a million packages published, many good names are taken,  
and simply knowing **“available or not”** isn’t enough anymore.

nscout gives you **the story behind the name**, not just the answer.

- If a name is available → you can publish immediately.  
- If it’s taken → you instantly see who owns it, how active it is,  
  what it does, and whether it’s safe to choose something similar.  
- If PyPI misbehaves → you get structured error information,  
  not cryptic failures.

It’s fast, scriptable, reliable, and ideal for developers preparing packages.

---

## ✨ Features

- Check whether a package name is **taken** or **not taken**
- Automatic metadata fetch from PyPI:
  - latest version
  - summary / description
  - author + author email
  - license
  - homepage & project URLs
  - Python requirement
  - release count
  - latest release timestamp
  - complete version history
- Clean pretty layout for **single package** checks
- Compact table layout for **multiple packages**
- File mode (`-r file.txt`) for batch operations
- JSON mode for scripts & CI tools
- Quiet mode for log-friendly output
- In-memory caching for ultra-fast repeated lookups
- Works with both **PyPI** and **TestPyPI**
- Robust error handling (timeouts, DNS, server failures)

---

## 📦 Installation

```bash
pip install nscout
````

Or install locally during development:

```bash
pip install -e .
```

---

## 🚀 Usage

### **Check a single package**

```bash
nscout requests
```

Example output:

```
requests — taken
Version:        2.32.5
Summary:        Python HTTP for Humans.
Author:         Kenneth Reitz
Author Email:   me@kennethreitz.org
License:        Apache-2.0
Homepage:       https://requests.readthedocs.io
Project URL:    https://pypi.org/project/requests/
Python Req:     >=3.9
Release Count:  157
Latest Release: 2.32.5 (2025-08-18T20:46:00.542304Z)
```

---

### **Check multiple packages**

```bash
nscout requests flyn numpy
```

Output:

```
Name                 Status       Version      Summary
---------------------------------------------------------------------------
requests             taken        2.32.5       Python HTTP for Humans.
flyn                 taken        0.1.8        Natural-language to shell command conver
numpy                taken        2.3.5        Fundamental package for array computing
```

---

### **File mode**

Create a file: names.txt

```
requests
numpy
mynewpkg
```

Run:

```bash
nscout -r names.txt
```

---

### **JSON output (for CI / scripts)**

```bash
nscout requests --json
```

Example (truncated):

```json
[
  {
    "name": "requests",
    "status": "taken",
    "source": {
      "pypi": { "taken": true },
      "testpypi": { "taken": true }
    },
    "metadata": {
      "version": "2.32.5",
      "summary": "Python HTTP for Humans.",
      "author": "Kenneth Reitz",
      "author_email": "me@kennethreitz.org",
      "license": "Apache-2.0",
      "homepage": "https://requests.readthedocs.io",
      "project_url": "https://pypi.org/project/requests/",
      "release_count": 157,
      "latest_release": {
        "version": "2.32.5",
        "timestamp": "2025-08-18T20:46:00.542304Z"
      }
    },
    "error": null
  }
]
```

---

### **Quiet mode**

Disable colors and decoration:

```bash
nscout requests flyn numpy --quiet
```

---

### **Version**

```bash
nscout --version
```

---

## 🧠 Exit Codes

| Code | Meaning                      |
| ---- | ---------------------------- |
| 0    | All names available          |
| 1    | At least one name is taken   |
| 4    | Network error / PyPI failure |

These codes are safe and predictable for CI pipelines.

---

## 🏗 Project Structure

```
nscout/
├── nscout/
│   ├── cache.py    # in-memory caching
│   ├── checker.py  # availability & metadata fetching logic
│   ├── cli.py      # command line interface
│   ├── format.py   # pretty output & table layouts
├── pyproject.toml
├── README.md
└── .gitignore

```

---

## 🛠 Development

Install in editable mode:

```bash
pip install -e .
```

Run the CLI:

```bash
python -m nscout.cli package_name
```

---

## 📤 Publishing

```bash
python -m build
twine upload dist/*
```

---

## ⚠ Known Issues / Limitations

- PyPI sometimes throttles requests for frequently-updated packages.  
  nscout handles this gracefully, but rare transient `"error"` states may occur.
- TestPyPI does not provide full metadata, so only availability is checked.
- Package summaries longer than ~40 characters are truncated in table mode.
- Windows PowerShell sometimes delays network requests when behind VPNs or proxies.



---

## 🧭 Roadmap

### 🔜 Next planned features
- **Detailed error classification**  
  Distinguish between timeout, DNS failure, PyPI 5xx, rate-limiting, etc.

- **Version selection flags**  
  (`--latest`, `--history`, etc.)

- **Rich-powered formatting**  
  Optional: colors, tables, and layout via the `rich` library.

- **Offline cache persistence**  
  Save metadata locally for repeated work.

- **Programmatic API**  
  Allow importing and using nscout as a library.

### 🚀 Future ideas
- Plugin system for custom registries (npm, crates.io, RubyGems)  
- A web UI for package-name searching  
- A GitHub Action that uses nscout to block publishing if a name is taken  





