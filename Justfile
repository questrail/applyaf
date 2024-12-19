# List the available justfile recipes
[group('general')]
@default:
  just --list --unsorted

# List the lines of code in the project
[group('general')]
loc:
  scc --remap-unknown "-*- Justfile -*-":"justfile"

# Lint and format code using ruff
[group('test')]
fix: 
  ruff check
  ruff format

# Test code using pytest
[group('test')]
test: 
  uv run pytest

# Add/update dependency
[group('dependencies')]
add dep:
  uv add {{dep}}

# Add/update dependency to the development group
[group('dependencies')]
dev dep:
  uv add --dev {{dep}}

# List the outdated dependencies
[group('dependencies')]
out:
  uv pip list --outdated

# Lock/freeze dependencies
[group('dependencies')]
lock:
  uv lock

# Format, test, build, and publish to PyPI
[group('deploy')]
deploy: fix test
  uv build
  uv publish
