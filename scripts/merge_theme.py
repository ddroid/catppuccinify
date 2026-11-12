import subprocess
import re

# 1. Read upstream files
upstream_theme = subprocess.check_output(["git", "show", "upstream/main:theme.js"]).decode("utf-8")

# Let's inspect where resolveAccentColor is in upstream_theme
accent_old_start = "  async function resolveAccentColor(sourceUrl, fallbackUrl) {"
accent_old_end = "    window.dispatchEvent(new Event(\"liquifyAccentColorReady\"));\n  }"

assert accent_old_start in upstream_theme, "accent_old_start not found"
assert accent_old_end in upstream_theme, "accent_old_end not found"

accent_replacement = r"""  /* Catppuccin palette organized by flavor – each flavor snaps to its own
     official swatches with contrast-safe pairings. */
  var CATPPUCCIN_FLAVOR_ACCENTS = {
    mocha: [
      "F5E0DC", "F2CDCD", "F5C2E7", "CBA6F7", "F38BA8", "EBA0AC",
      "FAB387", "F9E2AF", "A6E3A1", "94E2D5", "89DCEB", "74C7EC", "89B4FA", "B4BEFE"
    ],
    macchiato: [
      "F4DBD6", "F0C6C6", "F5BDE6", "C6A0F6", "ED8796", "EE99A0",
      "F5A97F", "EED49F", "A6DA95", "8BD5CA", "91D7E3", "7DC4E4", "8AADF4", "B7BDF8"
    ],
    frappe: [
      "F2D5CF", "EEBEBE", "F4B8E4", "CA9EE6", "E78284", "EA999C",
      "EF9F76", "E5C890", "A6D189", "81C8BE", "99D1DB", "85C1DC", "8CAAEE", "BABBF1"
    ],
    latte: [
      "DC8A78", "DD7878", "EA76CB", "8839EF", "D20F39", "E64553",
      "FE640B", "DF8E1D", "40A02B", "179299", "04A5E5", "209FB5", "1E66F5", "7287FD"
    ]
  };
  var CATPPUCCIN_FLAVOR_NEUTRALS = {
    mocha: ["CDD6F4", "A6ADC8", "9399B2", "585B70", "313244", "1E1E2E", "181825", "11111B"],
    macchiato: ["CAD3F5", "A5ADCB", "939AB7", "5B6078", "363A4F", "24273A", "1E2030", "181926"],
    frappe: ["C6D0F5", "A5ADCE", "949CBB", "626880", "414559", "303446", "292C3C", "232634"],
    latte: ["4C4F69", "6C6F85", "7C7F93", "ACB0BE", "CCD0DA", "EFF1F5", "E6E9EF", "DCE0E8"]
  };
  function getActiveFlavor() {
    try {
      return document.documentElement.dataset.liquifyFlavor || localStorage.getItem(COLOR_SCHEME_KEY) || "mocha";
    } catch {
      return "mocha";
    }
  }
  function parseRgb(rgb) {
    const m2 = /rgb\((\d+),\s*(\d+),\s*(\d+)\)/.exec(rgb);
    if (!m2) return null;
    return { r: +m2[1], g2: +m2[2], b2: +m2[3] };
  }
  function luminanceOf({ r, g2, b2 }) {
    const f = (v) => {
      const c = v / 255;
      return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * f(r) + 0.7152 * f(g2) + 0.0722 * f(b2);
  }
  function contrastRatio(a, b2) {
    const la = luminanceOf(a);
    const lb = luminanceOf(b2);
    const [hi, lo] = la > lb ? [la, lb] : [lb, la];
    return (hi + 0.05) / (lo + 0.05);
  }
  function hexToRgb(hex) {
    const clean = hex.replace("#", "");
    return { r: parseInt(clean.slice(0, 2), 16), g2: parseInt(clean.slice(2, 4), 16), b2: parseInt(clean.slice(4, 6), 16) };
  }
  /* Find the palette swatch with the smallest perceptual distance to the
     sampled color in the active flavor's accent pool. */
  function nearestPaletteColor(rgbStr, pool) {
    const rgb = parseRgb(rgbStr);
    if (!rgb) return null;
    let best = null;
    let bestDist = Infinity;
    for (const hex of pool) {
      const c2 = hexToRgb(hex);
      const dr = rgb.r - c2.r;
      const dg = rgb.g2 - c2.g2;
      const db = rgb.b2 - c2.b2;
      const dist = 2 * dr * dr + 4 * dg * dg + 3 * db * db;
      if (dist < bestDist) {
        bestDist = dist;
        best = hex;
      }
    }
    return best ? `#${best}` : null;
  }
  function rgbFromCss(css) {
    const m2 = /rgba?\((\d+),\s*(\d+),\s*(\d+)/.exec(css);
    if (!m2) return null;
    return { r: +m2[1], g2: +m2[2], b2: +m2[3] };
  }
  /* Pick a secondary color: prefer a neutral swatch with enough contrast
     against the primary (>= 2.5:1), falling back to a far-enough accent. */
  function pickSecondaryColor(primaryHex, neutrals, accents) {
    const primary = hexToRgb(primaryHex);
    const lp = luminanceOf(primary);
    const onAccent = lp > 0.42 ? hexToRgb("11111B") : hexToRgb("EFF1F5");
    const neutralPool = neutrals || CATPPUCCIN_FLAVOR_NEUTRALS.mocha;
    const accentPool = accents || CATPPUCCIN_FLAVOR_ACCENTS.mocha;
    let best = null;
    let bestContrast = 0;
    for (const hex of neutralPool) {
      const c2 = hexToRgb(hex);
      const ratio = contrastRatio(primary, c2);
      if (ratio > bestContrast) {
        bestContrast = ratio;
        best = c2;
      }
    }
    if (best && bestContrast >= 2.5) {
      return { hex: `#${best.r.toString(16).padStart(2, "0")}${best.g2.toString(16).padStart(2, "0")}${best.b2.toString(16).padStart(2, "0")}`.toUpperCase(), onAccent };
    }
    let bestAccent = null;
    let bestAccentContrast = 0;
    for (const hex of accentPool) {
      const c2 = hexToRgb(hex);
      const ratio = contrastRatio(primary, c2);
      if (ratio > bestAccentContrast) {
        bestAccentContrast = ratio;
        bestAccent = c2;
      }
    }
    const fallback = bestAccent || (lp > 0.42 ? hexToRgb("11111B") : hexToRgb("EFF1F5"));
    const hexStr = `#${fallback.r.toString(16).padStart(2, "0")}${fallback.g2.toString(16).padStart(2, "0")}${fallback.b2.toString(16).padStart(2, "0")}`.toUpperCase();
    return { hex: hexStr, onAccent };
  }
  /* Resolve the accent pair for a cover, snapped to the active flavor */
  async function resolveAccentPair(sourceUrl, fallbackUrl) {
    const flavor = getActiveFlavor();
    const accents = CATPPUCCIN_FLAVOR_ACCENTS[flavor] || CATPPUCCIN_FLAVOR_ACCENTS.mocha;
    const neutrals = CATPPUCCIN_FLAVOR_NEUTRALS[flavor] || CATPPUCCIN_FLAVOR_NEUTRALS.mocha;
    const defaultMauveHex = (COLOR_PALETTES[flavor]?.button || "CBA6F7");
    const defaultMauve = `#${defaultMauveHex}`;

    let sampled = null;
    const direct = await getDominantColor(sourceUrl);
    if (direct) sampled = direct;
    if (!sampled && fallbackUrl && fallbackUrl !== sourceUrl) {
      const cover = await getDominantColor(fallbackUrl);
      if (cover) sampled = cover;
    }
    if (!sampled) {
      const palette = await getPaletteColor(Spicetify.Player?.data?.item?.uri ?? null);
      if (palette) sampled = palette;
    }
    const primary = nearestPaletteColor(sampled || defaultMauve, accents) || defaultMauve;
    const secondary = pickSecondaryColor(primary.replace("#", ""), neutrals, accents);
    return { primary, secondary: secondary.hex, onAccent: secondary.onAccent };
  }
  /* Safely converts both { r, g2, b2 } objects and hex strings to CSS rgb() */
  function cssRgb(val) {
    if (!val) return "rgb(0,0,0)";
    if (typeof val === "object" && val !== null && "r" in val && "g2" in val && "b2" in val) {
      return `rgb(${val.r},${val.g2},${val.b2})`;
    }
    const cleanHex = String(val).replace("#", "");
    const c2 = hexToRgb(cleanHex);
    return `rgb(${c2.r},${c2.g2},${c2.b2})`;
  }
  function readAccentBoosts() {
    return {
      satBoost: parseInt(localStorage.getItem("liquify-accent-sat-boost") || "17", 10) / 10,
      lightBoost: parseInt(localStorage.getItem("liquify-accent-light-boost") || "11", 10) / 10
    };
  }
  async function applyAccent(sourceUrl, fallbackUrl) {
    const flavor = getActiveFlavor();
    const defaultMauve = "#" + (COLOR_PALETTES[flavor]?.button || "CBA6F7");
    const defaultSecondary = "#" + (COLOR_PALETTES[flavor]?.lavender || "B4BEFE");
    const defaultOnAccent = flavor === "latte" ? hexToRgb("EFF1F5") : hexToRgb("11111B");

    const pair = sourceUrl === UNSAMPLEABLE
      ? { primary: defaultMauve, secondary: defaultSecondary, onAccent: defaultOnAccent }
      : await resolveAccentPair(sourceUrl, fallbackUrl);

    document.documentElement.style.setProperty("--accent-color", pair.primary);
    document.documentElement.style.setProperty("--accent-color-secondary", cssRgb(pair.secondary));
    document.documentElement.style.setProperty("--accent-on-accent", cssRgb(pair.onAccent));
    window.dispatchEvent(new Event("liquifyAccentColorReady"));
  }"""

idx1 = upstream_theme.find(accent_old_start)
idx2 = upstream_theme.find(accent_old_end) + len(accent_old_end)
upstream_theme = upstream_theme[:idx1] + accent_replacement + upstream_theme[idx2:]

# Update default player width/height:
upstream_theme = upstream_theme.replace("var DEFAULT_CUSTOM_WIDTH = 80;\n  var DEFAULT_CUSTOM_HEIGHT = 88;", "var DEFAULT_CUSTOM_WIDTH = 70;\n  var DEFAULT_CUSTOM_HEIGHT = 80;")

# Config section:
config_anchor = "  // src/settings/features/config.ts\n  var PLAIN_KEYS = ["
assert config_anchor in upstream_theme, "config_anchor not found"

config_insert = """  // src/settings/features/config.ts
  var COLOR_SCHEME_KEY = "liquify-color-scheme";
  var COLOR_SCHEMES = [
    { value: "mocha", label: "Mocha" },
    { value: "macchiato", label: "Macchiato" },
    { value: "frappe", label: "Frappé" },
    { value: "latte", label: "Latte" }
  ];
  var COLOR_PALETTES = {
    mocha: {
      text: "CDD6F4", subtext: "A6ADC8", main: "1E1E2E", sidebar: "181825", player: "181825", card: "313244", shadow: "11111B", highlight: "45475A", "highlight-elevated": "45475A", "main-elevated": "313244", "selected-row": "585B70", button: "CBA6F7", "button-active": "A6E3A1", "button-disabled": "45475A", "tab-active": "313244", notification: "CBA6F7", "notification-error": "F38BA8", equalizer: "CBA6F7", misc: "9399B2",
      rosewater: "F5E0DC", flamingo: "F2CDCD", pink: "F5C2E7", mauve: "CBA6F7", red: "F38BA8", maroon: "EBA0AC", peach: "FAB387", yellow: "F9E2AF", green: "A6E3A1", teal: "94E2D5", sky: "89DCEB", sapphire: "74C7EC", blue: "89B4FA", lavender: "B4BEFE", subtext1: "BAC2DE", subtext0: "A6ADC8", overlay2: "9399B2", overlay1: "7F849C", overlay0: "6C7086", surface2: "585B70", surface1: "45475A", surface0: "313244", base: "1E1E2E", mantle: "181825", crust: "11111B"
    },
    macchiato: {
      text: "CAD3F5", subtext: "A5ADCB", main: "24273A", sidebar: "1E2030", player: "1E2030", card: "363A4F", shadow: "181926", highlight: "494D64", "highlight-elevated": "494D64", "main-elevated": "363A4F", "selected-row": "5B6078", button: "C6A0F6", "button-active": "A6DA95", "button-disabled": "494D64", "tab-active": "363A4F", notification: "C6A0F6", "notification-error": "ED8796", equalizer: "C6A0F6", misc: "939AB7",
      rosewater: "F4DBD6", flamingo: "F0C6C6", pink: "F5BDE6", mauve: "C6A0F6", red: "ED8796", maroon: "EE99A0", peach: "F5A97F", yellow: "EED49F", green: "A6DA95", teal: "8BD5CA", sky: "91D7E3", sapphire: "7DC4E4", blue: "8AADF4", lavender: "B7BDF8", subtext1: "B8C0E0", subtext0: "A5ADCB", overlay2: "939AB7", overlay1: "8087A2", overlay0: "6E738D", surface2: "5B6078", surface1: "494D64", surface0: "363A4F", base: "24273A", mantle: "1E2030", crust: "181926"
    },
    frappe: {
      text: "C6D0F5", subtext: "A5ADCE", main: "303446", sidebar: "292C3C", player: "292C3C", card: "414559", shadow: "232634", highlight: "51576D", "highlight-elevated": "51576D", "main-elevated": "414559", "selected-row": "626880", button: "CA9EE6", "button-active": "A6D189", "button-disabled": "51576D", "tab-active": "414559", notification: "CA9EE6", "notification-error": "E78284", equalizer: "CA9EE6", misc: "949CBB",
      rosewater: "F2D5CF", flamingo: "EEBEBE", pink: "F4B8E4", mauve: "CA9EE6", red: "E78284", maroon: "EA999C", peach: "EF9F76", yellow: "E5C890", green: "A6D189", teal: "81C8BE", sky: "99D1DB", sapphire: "85C1DC", blue: "8CAAEE", lavender: "BABBF1", subtext1: "B5BFE2", subtext0: "A5ADCE", overlay2: "949CBB", overlay1: "838BA7", overlay0: "737994", surface2: "626880", surface1: "51576D", surface0: "414559", base: "303446", mantle: "292C3C", crust: "232634"
    },
    latte: {
      text: "4C4F69", subtext: "6C6F85", main: "EFF1F5", sidebar: "E6E9EF", player: "E6E9EF", card: "CCD0DA", shadow: "DCE0E8", highlight: "BCC0CC", "highlight-elevated": "BCC0CC", "main-elevated": "CCD0DA", "selected-row": "ACB0BE", button: "8839EF", "button-active": "40A02B", "button-disabled": "BCC0CC", "tab-active": "CCD0DA", notification: "8839EF", "notification-error": "D20F39", equalizer: "8839EF", misc: "7C7F93",
      rosewater: "DC8A78", flamingo: "DD7878", pink: "EA76CB", mauve: "8839EF", red: "D20F39", maroon: "E64553", peach: "FE640B", yellow: "DF8E1D", green: "40A02B", teal: "179299", sky: "04A5E5", sapphire: "209FB5", blue: "1E66F5", lavender: "7287FD", subtext1: "5C5F77", subtext0: "6C6F85", overlay2: "7C7F93", overlay1: "8C8FA1", overlay0: "9CA0B0", surface2: "ACB0BE", surface1: "BCC0CC", surface0: "CCD0DA", base: "EFF1F5", mantle: "E6E9EF", crust: "DCE0E8"
    }
  };
  function applyColorScheme(scheme) {
    if (!COLOR_PALETTES[scheme]) scheme = "mocha";
    localStorage.setItem(COLOR_SCHEME_KEY, scheme);
    const root = document.documentElement;
    root.dataset.liquifyFlavor = scheme;
    for (const [key, value] of Object.entries(COLOR_PALETTES[scheme])) root.style.setProperty(`--spice-${key}`, `#${value}`);
    window.dispatchEvent(new Event("liquifyColorSchemeChange"));
    try {
      resetDynamicAccentCache?.();
      applySavedAccentSettings?.();
    } catch {
    }
  }
  function ensureColorSchemeApplied() {
    const saved = localStorage.getItem(COLOR_SCHEME_KEY);
    if (saved && COLOR_SCHEMES.some((s2) => s2.value === saved)) {
      try {
        applyColorScheme(saved);
      } catch {
      }
      return saved;
    }
    try {
      const bg = getComputedStyle(document.documentElement).getPropertyValue("--spice-main").trim().toUpperCase();
      const known = {
        mocha: "1E1E2E",
        macchiato: "24273A",
        frappe: "303446",
        latte: "EFF1F5"
      };
      for (const [name, hex] of Object.entries(known)) {
        if (bg.includes(hex)) {
          localStorage.setItem(COLOR_SCHEME_KEY, name);
          document.documentElement.dataset.liquifyFlavor = name;
          return name;
        }
      }
    } catch {
    }
    return "mocha";
  }
  var PLAIN_KEYS = [
    COLOR_SCHEME_KEY,"""

upstream_theme = upstream_theme.replace(config_anchor, config_insert)

# SettingsContent:
content_anchor = '    const [accentMode, setAccentMode] = React.useState(readLS("liquify-accent-mode", "dynamic"));'
assert content_anchor in upstream_theme, "content_anchor not found"
scheme_state = '    const [scheme, setScheme] = React.useState(localStorage.getItem(COLOR_SCHEME_KEY) || "mocha");\n' + content_anchor
upstream_theme = upstream_theme.replace(content_anchor, scheme_state)

sec_accent = 'React.createElement(Section, { id: "liquify-sec-accent", title: titles.accent }, '
assert sec_accent in upstream_theme, "sec_accent not found"

sec_accent_replacement = sec_accent + """/* @__PURE__ */ React.createElement("div", { className: "liquifyRow" }, /* @__PURE__ */ React.createElement("div", { className: "liquifyLabel" }, "Color Scheme", /* @__PURE__ */ React.createElement(HelpTip, { text: "Switch between the Catppuccin flavors." })), /* @__PURE__ */ React.createElement(
      Select,
      {
        value: scheme,
        options: COLOR_SCHEMES,
        onChange: (v2) => {
          setScheme(v2);
          applyColorScheme(v2);
        }
      }
    )), """
upstream_theme = upstream_theme.replace(sec_accent, sec_accent_replacement, 1)

# In startLiquifySettings, call ensureColorSchemeApplied();
start_anchor = "  async function startLiquifySettings() {\n    const anyWin = window;\n    if (anyWin.liquifyStandaloneTsInitialized) return;\n    anyWin.liquifyStandaloneTsInitialized = true;\n    await awaitSpicetifyReact();"
assert start_anchor in upstream_theme, "start_anchor not found"
start_replacement = start_anchor + "\n    ensureColorSchemeApplied();"
upstream_theme = upstream_theme.replace(start_anchor, start_replacement)

# Write modified theme.js
with open("theme.js", "w", encoding="utf-8") as f:
    f.write(upstream_theme)

print("✅ Successfully updated theme.js with latest upstream and Catppuccin extensions!")
