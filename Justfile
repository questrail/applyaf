# List the available justfile recipes
[group('general')]
@default:
  just --list --unsorted

# List the lines of code in the project
[group('general')]
loc:
  scc --remap-unknown "-*- Justfile -*-":"justfile"

# Lint code using ruff
[group('test')]
lint: 
  ruff check

# Test code using nose2
[group('test')]
test: 
  uv run nose2 -C

# List the outdated dependencies
[group('dependencies')]
outdated:
  pip list --outdated

# Freeze dependencies
[group('dependencies')]
freeze:
  uv lock
