import argparse
import sys
import json

from .checker import check_name
from . import __version__
from .format import print_single, print_multi


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