# **namescout**

A lightweight command-line tool for checking whether a package name is already taken on **PyPI** and **TestPyPI**.
It queries PyPI’s public JSON endpoints and reports results in a consistent, script-friendly format.

---

## **Features**

* Checks name availability on both PyPI and TestPyPI
* Minimal dependencies, fast responses
* Deterministic output format for automation
* Compatible with Python 3.10+

---

## **Installation**

From PyPI (after publishing):

```bash
pip install namescout
```

For local development:

```bash
pip install -e .
```

---

## **Usage**

Run a check:

```bash
namescout <package-name>
```

### **Output format**

```
exit code : <code>
PyPi : taken | not taken
TestPyPi : taken | not taken
```

### Example

```bash
namescout requests
```

Output:

```
exit code : 1
PyPi : taken
TestPyPi : not taken
```

---

## **Exit codes**

These codes reflect the result from **PyPI**, since it is the authoritative source for package publishing:

| Code | Meaning              |
| ---- | -------------------- |
| 0    | Name is not taken    |
| 1    | Name is taken        |
| 2    | Network or API error |

---

## **Why this tool exists**

PyPI does not offer a dedicated endpoint for checking name availability.
`namescout` performs small, direct checks against the Warehouse JSON API:

* A **404 response** means the name does not exist → **not taken**
* Any other status (200, 5xx, etc.) indicates the name exists or the service is unreachable

This makes it a reliable and efficient way to verify package name availability.

---

## **Development**

Run from source:

```bash
python -m namescout <package-name>
```

Project structure:

```
namescout/
├── namescout/
│   ├── __init__.py
│   ├── cli.py          # command-line interface
│   └── checker.py      # availability logic
├── pyproject.toml
├── README.md
└── LICENSE
```
---