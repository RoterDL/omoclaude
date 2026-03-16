# exp-003: POSIX vs Bash Shebang Mismatch

## Dilemma
Script declared `#!/bin/sh` but used `<<<` (here-string), a Bash-only feature. `sh -n` syntax check failed.

## Strategy
If any Bash-specific syntax is used (`<<<`, arrays, `[[ ]]`, process substitution), use `#!/bin/bash`. Only use `#!/bin/sh` for strictly POSIX-compatible scripts.

## Applicable Scenario
Writing shell scripts that will be syntax-checked or run on systems where `/bin/sh` is not Bash (e.g., dash on Ubuntu).

## Keywords
shebang, POSIX, bash, here-string, shell compatibility
