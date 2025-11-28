## **nscout**

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

From PyPI:

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

This keeps the tool fast, predictable, and convenient during package creation.

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

## **Notes**

nscout stays intentionally small and focused. If it helps you ship cleaner packages, the project has done its job.

It was built for the tiny moments that slow releases down, and smoothing even one step in your workflow makes it worthwhile.

The project is open to thoughtful improvements and small quality-of-life contributions.

Future growth will be deliberate—only in places where it clearly adds value, like lightweight automation hooks or CI-friendly helpers.

---

**Powered by Python, fueled by caffeine, guided by late-night curiosity ☕🚀**
