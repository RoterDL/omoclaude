# exp-002: Script Extraction Requires allowed-tools Update

## Dilemma
Extracted inline bash to `capture-diff.sh` but SKILL.md frontmatter `allowed-tools` only whitelisted `spec-manager.py` and `codeagent-wrapper`. New script blocked at runtime.

## Strategy
Every time a new script is extracted from a SKILL.md, add its path to the `allowed-tools` frontmatter array as an explicit implementation step. Validate by checking frontmatter after edit.

## Applicable Scenario
Any skill that extracts inline code to a separate script file.

## Keywords
allowed-tools, frontmatter, script extraction, SKILL.md, permissions
