#!/usr/bin/env bash
# Catppuccinify Spicetify Theme Installer
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/ddroid/catppuccinify/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/ddroid/catppuccinify/main/install.sh | bash -s -- <mocha|macchiato|frappe|latte>

set -e

# Colors
C_RESET="\033[0m"
C_BOLD="\033[1m"
C_MAUVE="\033[38;2;203;166;247m"
C_BLUE="\033[38;2;137;180;250m"
C_GREEN="\033[38;2;166;227;161m"
C_PEACH="\033[38;2;250;179;135m"
C_RED="\033[38;2;243;139;168m"

echo -e "${C_MAUVE}${C_BOLD}"
cat << 'EOF'
   ____      _                               _       _  __       
  / ___|__ _| |_ _ __  _   _  ___ ___(_)_ __ (_)/ _|_   _ 
 | |   / _` | __| '_ \| | | |/ __/ __| | '_ \| | |_| | | |
 | |__| (_| | |_| |_) | |_| | (_| (__| | | | | |  _| |_| |
  \____\__,_|\__| .__/ \__,_|\___\___|_|_| |_|_|_|  \__, |
                |_|                                  |___/ 
EOF
echo -e "${C_BLUE}Catppuccinify Spicetify Theme Installer${C_RESET}\n"

# Verify Spicetify is installed
if ! command -v spicetify >/dev/null 2>&1; then
  echo -e "${C_RED}Error: spicetify CLI is not found in your PATH.${C_RESET}"
  echo -e "Please install Spicetify first: ${C_PEACH}https://spicetify.app/docs/getting-started${C_RESET}"
  echo -e "Quick install: ${C_BOLD}curl -fsSL https://raw.githubusercontent.com/spicetify/cli/main/install.sh | sh${C_RESET}"
  exit 1
fi

# Determine Flavor (default: mocha)
INPUT_FLAVOR="${1:-mocha}"
FLAVOR=$(echo "$INPUT_FLAVOR" | tr '[:upper:]' '[:lower:]')

case "$FLAVOR" in
  mocha|macchiato|frappe|latte)
    ;;
  frappé)
    FLAVOR="frappe"
    ;;
  *)
    echo -e "${C_PEACH}Warning: Unknown flavor '${INPUT_FLAVOR}'. Defaulting to 'mocha'.${C_RESET}"
    echo -e "Valid flavors: ${C_BOLD}mocha${C_RESET}, ${C_BOLD}macchiato${C_RESET}, ${C_BOLD}frappe${C_RESET}, ${C_BOLD}latte${C_RESET}"
    FLAVOR="mocha"
    ;;
esac

echo -e "Selected flavor: ${C_GREEN}${C_BOLD}${FLAVOR}${C_RESET}"

# Locate Spicetify Themes directory
SPICETIFY_CONFIG_DIR=""
if SPICETIFY_CONFIG_FILE=$(spicetify -c 2>/dev/null); then
  SPICETIFY_CONFIG_DIR=$(dirname "$SPICETIFY_CONFIG_FILE")
fi

if [ -z "$SPICETIFY_CONFIG_DIR" ] || [ ! -d "$SPICETIFY_CONFIG_DIR" ]; then
  if [ -d "$HOME/.config/spicetify" ]; then
    SPICETIFY_CONFIG_DIR="$HOME/.config/spicetify"
  elif [ -d "$HOME/.spicetify" ]; then
    SPICETIFY_CONFIG_DIR="$HOME/.spicetify"
  else
    SPICETIFY_CONFIG_DIR="$HOME/.config/spicetify"
    mkdir -p "$SPICETIFY_CONFIG_DIR"
  fi
fi

THEMES_DIR="$SPICETIFY_CONFIG_DIR/Themes"
TARGET_DIR="$THEMES_DIR/catppuccinify"
mkdir -p "$THEMES_DIR"

echo -e "Installing theme into: ${C_BLUE}${TARGET_DIR}${C_RESET}..."

REPO_URL="https://github.com/ddroid/catppuccinify.git"

if [ -d "$TARGET_DIR/.git" ]; then
  echo "Existing git checkout found. Updating..."
  git -C "$TARGET_DIR" pull --ff-only || true
else
  rm -rf "$TARGET_DIR"
  if command -v git >/dev/null 2>&1; then
    git clone --depth 1 "$REPO_URL" "$TARGET_DIR"
  else
    mkdir -p "$TARGET_DIR"
    curl -fsSL https://raw.githubusercontent.com/ddroid/catppuccinify/main/color.ini -o "$TARGET_DIR/color.ini"
    curl -fsSL https://raw.githubusercontent.com/ddroid/catppuccinify/main/user.css -o "$TARGET_DIR/user.css"
    curl -fsSL https://raw.githubusercontent.com/ddroid/catppuccinify/main/theme.js -o "$TARGET_DIR/theme.js"
    curl -fsSL https://raw.githubusercontent.com/ddroid/catppuccinify/main/manifest.json -o "$TARGET_DIR/manifest.json"
    curl -fsSL https://raw.githubusercontent.com/ddroid/catppuccinify/main/spotikit.json -o "$TARGET_DIR/spotikit.json" || true
  fi
fi

echo -e "${C_GREEN}Applying Spicetify configurations...${C_RESET}"
spicetify config current_theme catppuccinify color_scheme "$FLAVOR"
spicetify config inject_css 1 inject_theme_js 1 replace_colors 1 overwrite_assets 1

echo -e "${C_GREEN}Applying theme to Spotify...${C_RESET}"
if ! spicetify apply; then
  echo -e "${C_PEACH}Standard apply returned non-zero. Attempting 'spicetify backup apply'...${C_RESET}"
  spicetify backup apply
fi

echo -e "\n${C_GREEN}${C_BOLD}✨ Catppuccinify installed successfully! Enjoy your ${FLAVOR} flavor! ✨${C_RESET}\n"
