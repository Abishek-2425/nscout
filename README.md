# **nscout**

A small command-line tool for checking whether a package name is already taken on **PyPI** and **TestPyPI**.
It queries PyPI’s public JSON endpoints and reports the results in a simple, readable format.

---

## **Features**

* Checks availability on both PyPI and TestPyPI
* No special exit codes — clear human-readable output only
* Minimal dependencies, very fast
* Works on Python 3.10+

---

## **Installation**

From PyPI (after publishing):

```bash
pip install nscout
```

For local development:

```bash
pip install -e .
```

---

## **Usage**

Run:

```bash
nscout <package-name>
```

Example:

```bash
nscout requests
```

Output:

```
PyPi : taken
TestPyPi : not taken
```

The tool always prints exactly these two lines — no exit-code text.

---

## **Why this tool exists**

PyPI doesn’t have a dedicated “is this name available?” endpoint.
This tool performs a lightweight check against PyPI’s JSON metadata URLs:

* If the endpoint returns **404**, the name is **not taken**
* Any other response means the name exists or the server is unreachable

This makes the tool quick, reliable, and easy to use during package creation.

---

## **Development**

Run directly from source:

```bash
python -m nscout <package-name>
```

Project layout:

```
nscout/
├── nscout/
│   ├── checker.py      # core logic
│   ├── cli.py          # command line interface
│   └── __init__.py
├── pyproject.toml
├── .gitignore
└── README.md

```

---
