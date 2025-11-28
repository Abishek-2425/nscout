import argparse
from .checker import check_name, PYPI, TESTPYPI

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Package name to check")
    args = parser.parse_args()
    
    pkg = args.name.strip()

    pypi_status = check_name(pkg, PYPI)
    testpypi_status = check_name(pkg, TESTPYPI)

    print(f"PyPi : {pypi_status}")
    print(f"TestPyPi : {testpypi_status}")

if __name__ == "__main__":
    main()