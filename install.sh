#!/usr/bin/env bash
# GamePulse one-command installer
#
# Usage:
#   curl -fsSL https://mathewrj.github.io/GamePulse-Integration/install.sh | bash
#
# Detects the package manager and installs the appropriate package from the
# latest GitHub Release. Arch/CachyOS users are redirected to AUR.
#
set -euo pipefail

REPO="MathewRJ/GamePulse"
API="https://api.github.com/repos/${REPO}/releases/latest"

# ── helpers ──────────────────────────────────────────────────────────────────

fetch() {
    if command -v curl &>/dev/null; then
        curl -fsSL "$@"
    elif command -v wget &>/dev/null; then
        wget -qO- "$@"
    else
        echo "ERROR: curl or wget is required." >&2
        exit 1
    fi
}

fetch_to() {
    local url="$1" dest="$2"
    if command -v curl &>/dev/null; then
        curl -fsSL -o "${dest}" "${url}"
    else
        wget -qO "${dest}" "${url}"
    fi
}

# ── resolve latest release ───────────────────────────────────────────────────

TAG=$(fetch "${API}" | grep '"tag_name"' | sed 's/.*"tag_name": *"\([^"]*\)".*/\1/')
VERSION="${TAG#v}"
BASE="https://github.com/${REPO}/releases/download/${TAG}"

echo "==> GamePulse ${VERSION}"
echo ""

# ── detect distro and install ────────────────────────────────────────────────

if command -v pacman &>/dev/null; then
    echo "Arch-based system detected."
    echo ""
    echo "Install via AUR (includes eBPF probes, builds from source):"
    echo "  yay -S gamepulse-git"
    echo ""
    echo "Or install the pre-built package from the release:"
    PKG="gamepulse-${VERSION}-1-x86_64.pkg.tar.zst"
    echo "  pacman -U '${BASE}/${PKG}'"
    exit 0

elif command -v apt-get &>/dev/null; then
    echo "Debian/Ubuntu detected."
    FILE="/tmp/gamepulse-agent_${VERSION}-1_amd64.deb"
    echo "==> Downloading ${FILE##*/} ..."
    fetch_to "${BASE}/gamepulse-agent_${VERSION}-1_amd64.deb" "${FILE}"
    echo "==> Installing..."
    sudo dpkg -i "${FILE}"
    rm -f "${FILE}"

elif command -v dnf &>/dev/null; then
    echo "Fedora/RHEL detected."
    FILE="/tmp/gamepulse-agent-${VERSION}-1.x86_64.rpm"
    echo "==> Downloading ${FILE##*/} ..."
    fetch_to "${BASE}/gamepulse-agent-${VERSION}-1.x86_64.rpm" "${FILE}"
    echo "==> Installing..."
    sudo dnf install -y "${FILE}"
    rm -f "${FILE}"

elif command -v rpm &>/dev/null; then
    echo "RPM-based system detected."
    FILE="/tmp/gamepulse-agent-${VERSION}-1.x86_64.rpm"
    echo "==> Downloading ${FILE##*/} ..."
    fetch_to "${BASE}/gamepulse-agent-${VERSION}-1.x86_64.rpm" "${FILE}"
    echo "==> Installing..."
    sudo rpm -i "${FILE}"
    rm -f "${FILE}"

else
    echo "Unsupported distribution."
    echo "Download packages from: https://github.com/${REPO}/releases/latest"
    exit 1
fi

# ── post-install ─────────────────────────────────────────────────────────────

echo ""
echo "==> gamepulse-agent ${VERSION} installed."
echo ""
echo "Next steps:"
echo "  1. Edit /etc/gamepulse/gamepulse.toml — set your Elasticsearch endpoint and API key"
echo "  2. Run: gamepulse setup   (verifies connectivity and writes user config)"
echo "  3. Add to Steam launch options: gamepulse run %command%"
echo ""
echo "Docs: https://github.com/${REPO}#readme"
