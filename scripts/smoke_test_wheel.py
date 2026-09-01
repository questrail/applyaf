# Copyright (c) 2013-2026 The applyaf developers. All rights reserved.
# Project site: https://github.com/questrail/applyaf
# Use of this source code is governed by a MIT-style license that
# can be found in the LICENSE.txt file for the project.
"""Check a built wheel from outside the source tree.

Every other check in this project runs against `src/`, so a packaging mistake
that leaves a module or `py.typed` out of the distribution passes ruff,
pyright, and the whole suite and ships anyway. Run this with the wheel
installed somewhere `src/` cannot be reached:

    uv run --no-project --with dist/*.whl python scripts/smoke_test_wheel.py 3.0.1

Python puts this file's own directory on `sys.path` rather than the working
directory, so `import applyaf` below can only resolve to the installed wheel.
"""

import argparse
import importlib.metadata
import importlib.resources

import applyaf


def main(expected: str) -> None:
    installed = importlib.metadata.version("applyaf")
    if installed != expected:
        raise SystemExit(f"The wheel installed {installed}, expected {expected}")

    for name in applyaf.__all__:
        getattr(applyaf, name)

    if not importlib.resources.files("applyaf").joinpath("py.typed").is_file():
        raise SystemExit("The wheel is missing py.typed")

    print(f"applyaf {installed} imported from {applyaf.__file__}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check a built applyaf wheel from outside the source tree."
    )
    parser.add_argument(
        "expected_version", help="the version the wheel is expected to install"
    )
    main(parser.parse_args().expected_version)
