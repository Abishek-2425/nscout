import argparse
import sys
import json

from .checker import check_name
from . import __version__


# -------------------------------------------------------------------
# Color helpers (disabled in --quiet mode)
# -------------------------------------------------------------------
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def colorize(text, color, quiet):
    if quiet:
        return text
    return f"{color}{text}{RESET}"


# -------------------------------------------------------------------
# Pretty output for a *single* package
# -------------------------------------------------------------------
def print_single(result, quiet):
    name = result["name"]
    status = result["status"]

    # Determine status color
    if status == "taken":
        status_str = colorize("taken", RED, quiet)
    elif status == "not_taken":
        status_str = colorize("not taken", GREEN, quiet)
    else:
        status_str = colorize("error", YELLOW, quiet)

    print(f"\n{name} — {status_str}")

    # If taken, show metadata
    if status == "taken" and result["metadata"]:
        m = result["metadata"]

        print(f"Version:        {m['version']}")
        print(f"Summary:        {m['summary'] or '—'}")
        print(f"Author:         {m['author'] or '—'}")
        print(f"Author Email:   {m['author_email'] or '—'}")
        print(f"License:        {m['license'] or '—'}")
        print(f"Homepage:       {m['homepage'] or '—'}")
        print(f"Project URL:    {m['project_url'] or '—'}")
        print(f"Python Req:     {m['requires_python'] or '—'}")
        print(f"Release Count:  {m['release_count']}")

        if m["latest_release"]:
            ts = m["latest_release"]["timestamp"]
            print(f"Latest Release: {m['latest_release']['version']} ({ts})")


# -------------------------------------------------------------------
# Table for *multiple* packages  (final polished alignment)
# -------------------------------------------------------------------
def print_multi(results, quiet):
    # Column widths
    NAME_W = 20
    STATUS_W = 12
    VERSION_W = 12

    # Header
    print(f"\n{'Name':{NAME_W}} {'Status':{STATUS_W}} {'Version':{VERSION_W}} Summary")
    print("-" * (NAME_W + STATUS_W + VERSION_W + 10 + 20))

    for result in results:
        name = result["name"]

        # raw status for padding
        raw_status = (
            "taken" if result["status"] == "taken"
            else "not taken" if result["status"] == "not_taken"
            else "error"
        )

        padded_status = f"{raw_status:{STATUS_W}}"

        # colorize padded status
        if result["status"] == "taken":
            status_str = colorize(padded_status, RED, quiet)
        elif result["status"] == "not_taken":
            status_str = colorize(padded_status, GREEN, quiet)
        else:
            status_str = colorize(padded_status, YELLOW, quiet)

        version = result["metadata"]["version"] if result["metadata"] else "—"
        summary = result["metadata"]["summary"] if result["metadata"] else "—"

        print(
            f"{name:{NAME_W}} "
            f"{status_str} "
            f"{version:{VERSION_W}} "
            f"{summary[:40]}"
        )

# -------------------------------------------------------------------
# Main CLI entry
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Inspect PyPI/TestPyPI package availability and metadata."
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"nscout {__version__}",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as structured JSON.",
    )

    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Disable colors and decorative output.",
    )

    parser.add_argument(
        "-r",
        "--read",
        metavar="FILE",
        help="Read package names from a file (one per line).",
    )

    parser.add_argument(
        "names",
        nargs="*",
        help="Package names to check.",
    )

    args = parser.parse_args()

    # Read file mode
    file_names = []
    if args.read:
        try:
            with open(args.read, "r", encoding="utf-8") as f:
                for line in f:
                    pkg = line.strip()
                    if pkg:
                        file_names.append(pkg)
        except FileNotFoundError:
            print(f"File not found: {args.read}")
            sys.exit(4)

    # Combine CLI names + file names
    all_names = list(dict.fromkeys(args.names + file_names))
    if not all_names:
        print("No package names provided.")
        sys.exit(4)

    # Run checks
    results = [check_name(name) for name in all_names]

    # JSON mode
    if args.json:
        print(json.dumps(results, indent=2))
        sys.exit(0)

    # Pretty output
    if len(results) == 1:
        print_single(results[0], args.quiet)
    else:
        print_multi(results, args.quiet)

    # Exit codes:
    # 1 = name taken
    # 4 = network/server error
    exit_code = 0
    for r in results:
        if r["status"] == "taken":
            exit_code = 1
        if r["status"] == "error":
            exit_code = 4

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
# -------------------------------------------------------------------