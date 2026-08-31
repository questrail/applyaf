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
test:
  uv run pytest

# Add dependency
[group('dependencies')]
add dep:
  uv add {{dep}}

# Add dependency to the development group
[group('dependencies')]
dev dep:
  uv add --dev {{dep}}

# Update dependency
[group('dependencies')]
up dep:
  uv remove {{dep}}
  uv add {{dep}}
  uv lock -P {{dep}}

# List the outdated dependencies
[group('dependencies')]
out:
  uv pip list --outdated

# Lock/freeze dependencies
[group('dependencies')]
lock:
  uv lock

# Check, test, build, and publish to PyPI
[group('deploy')]
deploy: lint test
  uv build
  uv publish
