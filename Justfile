# List the available justfile recipes
[group('general')]
@default:
  just --list --unsorted

# List the lines of code in the project
[group('general')]
loc:
  scc --remap-unknown "-*- Justfile -*-":"justfile"

# Lint and format code using ruff, applying any fixes
[group('test')]
fix:
  uv run ruff check --fix
  uv run ruff format

# Check lint, formatting, and types without modifying any files
[group('test')]
lint:
  uv run ruff check
  uv run ruff format --check
  uv run pyright

# Test code using pytest
[group('test')]
test *args:
  uv run pytest {{args}}

# Test code and report coverage
[group('test')]
cov *args:
  uv run pytest --cov --cov-report=term --cov-report=html {{args}}

# Add dependency
[group('dependencies')]
add dep:
  uv add {{dep}}

# Add dependency to the development group
[group('dependencies')]
dev dep:
  uv add --dev {{dep}}

# Update dependency to the newest version allowed by pyproject.toml
[group('dependencies')]
up dep:
  uv lock --upgrade-package {{dep}}
  uv sync

# Update all dependencies
[group('dependencies')]
up-all:
  uv lock --upgrade
  uv sync

# List the outdated dependencies
[group('dependencies')]
out:
  uv pip list --outdated

# Lock/freeze dependencies
[group('dependencies')]
lock:
  uv lock

# Check, test, and build the distributions that CI will publish
[group('deploy')]
build: lint test
  @test -z "$(git status --porcelain)" || { echo "Working tree is dirty"; exit 1; }
  uv build --clear

# Bump the version, close out the CHANGELOG, commit, and tag a release
[group('deploy')]
release bump="patch": lint test
  #!/usr/bin/env bash
  set -euo pipefail
  if [ -n "$(git status --porcelain)" ]; then
    echo "Working tree is dirty" >&2; exit 1
  fi
  if [ "$(git branch --show-current)" != master ]; then
    echo "Releases are cut from master" >&2; exit 1
  fi
  behind="$(git rev-list --count HEAD..@{upstream} 2>/dev/null || echo 0)"
  if [ "$behind" != 0 ]; then
    echo "master is ${behind} commit(s) behind its upstream; pull first" >&2; exit 1
  fi
  if ! python3 - <<'PY'
  import pathlib, re, sys
  body = re.search(
      r"^## Unreleased\s*\n(.*?)(?=^## v)",
      pathlib.Path("CHANGELOG.md").read_text(),
      re.S | re.M,
  )
  sys.exit(0 if body and body.group(1).strip() else 1)
  PY
  then
    echo "CHANGELOG.md has no entries under Unreleased" >&2; exit 1
  fi
  version="$(uv version --short --bump {{bump}} --dry-run)"
  tag="v${version}"
  if git rev-parse -q --verify "refs/tags/${tag}" >/dev/null; then
    echo "Tag ${tag} already exists" >&2; exit 1
  fi
  uv version --bump {{bump}}
  uv lock
  VERSION="$version" python3 - <<'PY'
  import datetime, os, pathlib
  heading = f"## v{os.environ['VERSION']} - {datetime.date.today().isoformat()}"
  p = pathlib.Path("CHANGELOG.md")
  s = p.read_text()
  p.write_text(s.replace("## Unreleased\n", f"## Unreleased\n\n{heading}\n", 1))
  PY
  git commit -qam "Release ${tag}"
  git tag -a "${tag}" -m "${tag}"
  echo
  echo "Tagged ${tag}. Publish it with:"
  echo
  echo "    git push --follow-tags"
