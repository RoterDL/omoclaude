#!/bin/bash
set -e

if [ -z "${SKIP_WARNING:-}" ]; then
  echo "⚠️  WARNING: install.sh is LEGACY and will be removed in future versions."
  echo "Please use the new installation method:"
  echo "  npx github:cexll/myclaude"
  echo ""
  echo "Set SKIP_WARNING=1 to bypass this message"
  echo "Continuing with legacy installation in 5 seconds..."
  sleep 5
fi

# Detect platform
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

# Normalize architecture names
case "$ARCH" in
    x86_64) ARCH="amd64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    *) echo "Unsupported architecture: $ARCH" >&2; exit 1 ;;
esac

# Build download URL
REPO="cexll/myclaude"
VERSION="${CODEAGENT_WRAPPER_VERSION:-${VERSION:-latest}}"
BINARY_NAME="codeagent-wrapper-${OS}-${ARCH}"
if [ "$VERSION" = "latest" ]; then
    URL="https://github.com/${REPO}/releases/latest/download/${BINARY_NAME}"
else
    URL="https://github.com/${REPO}/releases/download/${VERSION}/${BINARY_NAME}"
fi

INSTALL_DIR="${INSTALL_DIR:-$HOME/.claude}"
BIN_DIR="${INSTALL_DIR}/bin"
mkdir -p "$BIN_DIR"

WRAPPER_PATH="${BIN_DIR}/codeagent-wrapper"
SHOULD_DOWNLOAD=1

if [ -x "${WRAPPER_PATH}" ]; then
    LOCAL_VER_RAW=$("${WRAPPER_PATH}" --version 2>/dev/null || true)
    LOCAL_VER=$(printf '%s\n' "${LOCAL_VER_RAW}" | sed -n 's/.* version[[:space:]]\{1,\}\([^[:space:]]\{1,\}\).*/\1/p' | head -n 1)
    if [ -z "${LOCAL_VER}" ]; then
        LOCAL_VER=$(printf '%s\n' "${LOCAL_VER_RAW}" | awk 'NF{print $NF; exit}')
    fi
    LOCAL_VER=$(printf '%s' "${LOCAL_VER}" | tr -d '\r\n[:space:]')

    REMOTE_VER=""
    if [ "$VERSION" = "latest" ]; then
        RELEASE_JSON=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" 2>/dev/null || true)
        if [ -n "${RELEASE_JSON}" ]; then
            REMOTE_VER=$(printf '%s\n' "${RELEASE_JSON}" | sed -n 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]\{1,\}\)".*/\1/p' | head -n 1)
            REMOTE_VER=$(printf '%s' "${REMOTE_VER}" | tr -d '\r\n[:space:]')
        fi
        if [ -z "${REMOTE_VER}" ]; then
            echo "WARNING: failed to query latest release version; continuing with download."
        fi
    else
        REMOTE_VER=$(printf '%s' "${VERSION}" | tr -d '\r\n[:space:]')
    fi

    if [ -n "${LOCAL_VER}" ] && [ -n "${REMOTE_VER}" ] && [ "${LOCAL_VER}" = "${REMOTE_VER}" ]; then
        echo "codeagent-wrapper is already up to date (${LOCAL_VER}), skipping download."
        SHOULD_DOWNLOAD=0
    fi
fi

if [ "${SHOULD_DOWNLOAD}" -eq 1 ]; then
    echo "Downloading codeagent-wrapper from ${URL}..."
    if ! curl -fsSL "$URL" -o /tmp/codeagent-wrapper; then
        echo "ERROR: failed to download binary" >&2
        exit 1
    fi

    mv /tmp/codeagent-wrapper "${WRAPPER_PATH}"
    chmod +x "${WRAPPER_PATH}"

    if "${WRAPPER_PATH}" --version >/dev/null 2>&1; then
        echo "codeagent-wrapper installed successfully to ${WRAPPER_PATH}"
    else
        echo "ERROR: installation verification failed" >&2
        exit 1
    fi
fi

# Auto-add to shell config files with idempotency
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    echo ""
    echo "WARNING: ${BIN_DIR} is not in your PATH"

    # Detect user's default shell (from $SHELL, not current script executor)
    USER_SHELL=$(basename "$SHELL")
    case "$USER_SHELL" in
        zsh)
            RC_FILE="$HOME/.zshrc"
            PROFILE_FILE="$HOME/.zprofile"
            ;;
        *)
            RC_FILE="$HOME/.bashrc"
            PROFILE_FILE="$HOME/.profile"
            ;;
    esac

    # Idempotent add: check if complete export statement already exists
    EXPORT_LINE="export PATH=\"${BIN_DIR}:\$PATH\""
    FILES_TO_UPDATE=("$RC_FILE" "$PROFILE_FILE")

    for FILE in "${FILES_TO_UPDATE[@]}"; do
        if [ -f "$FILE" ] && grep -qF "${EXPORT_LINE}" "$FILE" 2>/dev/null; then
            echo "  ${BIN_DIR} already in ${FILE}, skipping."
        else
            echo "  Adding to ${FILE}..."
            echo "" >> "$FILE"
            echo "# Added by myclaude installer" >> "$FILE"
            echo "${EXPORT_LINE}" >> "$FILE"
        fi
    done

    echo "  Done. Restart your shell or run:"
    echo "    source ${PROFILE_FILE}"
    echo "    source ${RC_FILE}"
    echo ""
fi
