#!/usr/bin/env python3
"""
Pre-Bash Hook - Block dangerous commands before execution.
"""

import platform
import sys

_UNIX_PATTERNS = [
    'rm -rf /',
    'rm -rf ~',
    'dd if=',
    ':(){:|:&};:',
    'mkfs.',
    '> /dev/sd',
]

_WINDOWS_PATTERNS = [
    'rd /s /q c:\\',
    'rmdir /s /q c:\\',
    'rd /s /q %userprofile%',
    'rmdir /s /q %userprofile%',
    'del /f /s /q c:\\',
    'format c:',
    'format d:',
    'format e:',
    'remove-item -recurse -force c:\\',
    'remove-item -recurse -force ~',
    'remove-item -recurse -force $home',
    'remove-item -recurse -force $env:userprofile',
    '%0|%0',
]

IS_WINDOWS = platform.system() == "Windows"
DANGEROUS_PATTERNS = _WINDOWS_PATTERNS if IS_WINDOWS else _UNIX_PATTERNS


def main():
    command = sys.argv[1] if len(sys.argv) > 1 else ''

    if IS_WINDOWS:
        command_check = command.lower()
    else:
        command_check = command

    for pattern in DANGEROUS_PATTERNS:
        if pattern in command_check:
            print(f"[CWF] BLOCKED: Dangerous command detected: {pattern}", file=sys.stderr)
            sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
