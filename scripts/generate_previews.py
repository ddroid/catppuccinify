#!/usr/bin/env python3
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(ROOT, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

PALETTES = {
    "mocha": {
        "name": "Mocha",
        "tag": "Darkest Theme",
        "base": "#1E1E2E",
        "mantle": "#181825",
        "crust": "#11111B",
        "card": "#313244",
        "highlight": "#45475A",
        "text": "#CDD6F4",
        "subtext": "#A6ADC8",
        "accent": "#CBA6F7",
        "accent_alt": "#89B4FA",
        "accent_green": "#A6E3A1",
        "accent_peach": "#FAB387"
    },
    "macchiato": {
        "name": "Macchiato",
        "tag": "Medium Dark",
        "base": "#24273A",
        "mantle": "#1E2030",
        "crust": "#181926",
        "card": "#363A4F",
        "highlight": "#494D64",
        "text": "#CAD3F5",
        "subtext": "#A5ADCB",
        "accent": "#C6A0F6",
        "accent_alt": "#8AADF4",
        "accent_green": "#A6DA95",
        "accent_peach": "#F5A97F"
    },
    "frappe": {
        "name": "Frappé",
        "tag": "Soft Dark / Low Contrast",
        "base": "#303446",
        "mantle": "#292C3C",
        "crust": "#232634",
        "card": "#414559",
        "highlight": "#51576D",
        "text": "#C6D0F5",
        "subtext": "#A5ADCE",
        "accent": "#CA9EE6",
        "accent_alt": "#8CAAEE",
        "accent_green": "#A6D189",
        "accent_peach": "#EF9F76"
    },
    "latte": {
        "name": "Latte",
        "tag": "Official Light Theme",
        "base": "#EFF1F5",
        "mantle": "#E6E9EF",
        "crust": "#DCE0E8",
        "card": "#CCD0DA",
        "highlight": "#BCC0CC",
        "text": "#4C4F69",
        "subtext": "#6C6F85",
        "accent": "#8839EF",
        "accent_alt": "#1E66F5",
        "accent_green": "#40A02B",
        "accent_peach": "#FE640B"
    }
}

def render_preview_svg(flavor_key, p):
    w, h = 1200, 680
    return f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="cardGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['accent']}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{p['accent_alt']}" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="cardGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['accent_alt']}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{p['accent_green']}" stop-opacity="0.8"/>
    </linearGradient>
    <linearGradient id="cardGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p['accent_peach']}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{p['accent']}" stop-opacity="0.8"/>
    </linearGradient>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#000000" flood-opacity="0.35"/>
    </filter>
  </defs>

  <!-- App Window Background -->
  <rect width="{w}" height="{h}" rx="16" fill="{p['base']}"/>

  <!-- Window Header / Titlebar -->
  <rect width="{w}" height="48" rx="16" fill="{p['mantle']}"/>
  <rect y="32" width="{w}" height="16" fill="{p['mantle']}"/>
  <circle cx="28" cy="24" r="6" fill="#F38BA8"/>
  <circle cx="48" cy="24" r="6" fill="#F9E2AF"/>
  <circle cx="68" cy="24" r="6" fill="#A6E3A1"/>
  <text x="{w/2}" y="30" fill="{p['subtext']}" font-family="system-ui, -apple-system, sans-serif" font-size="13" font-weight="500" text-anchor="middle">Spotify - Catppuccinify ({p['name']} Flavor)</text>

  <!-- Sidebar -->
  <rect x="16" y="60" width="240" height="520" rx="16" fill="{p['mantle']}"/>
  <!-- Nav items -->
  <rect x="28" y="76" width="216" height="40" rx="10" fill="{p['card']}"/>
  <rect x="42" y="88" width="16" height="16" rx="4" fill="{p['accent']}"/>
  <text x="70" y="101" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="14" font-weight="600">Home</text>

  <rect x="42" y="132" width="16" height="16" rx="4" fill="{p['subtext']}"/>
  <text x="70" y="145" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="14" font-weight="500">Search</text>

  <rect x="42" y="172" width="16" height="16" rx="4" fill="{p['subtext']}"/>
  <text x="70" y="185" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="14" font-weight="500">Your Library</text>

  <!-- Playlists Divider -->
  <line x1="36" y1="210" x2="236" y2="210" stroke="{p['highlight']}" stroke-width="1"/>

  <text x="42" y="240" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="13" font-weight="500">✨ Catppuccin Chill</text>
  <text x="42" y="272" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="13" font-weight="500">🎵 Lofi Beats 2026</text>
  <text x="42" y="304" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="13" font-weight="500">⚡ Coding Synthwave</text>
  <text x="42" y="336" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="13" font-weight="500">☕ Coffee &amp; Jazz</text>
  <text x="42" y="368" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="13" font-weight="500">🌌 Ambient Dreams</text>

  <!-- Flavor Badge in Sidebar -->
  <rect x="32" y="520" width="208" height="42" rx="10" fill="{p['card']}"/>
  <circle cx="52" cy="541" r="7" fill="{p['accent']}"/>
  <text x="68" y="546" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="13" font-weight="600">Flavor: {p['name']}</text>

  <!-- Main View Area -->
  <rect x="272" y="60" width="912" height="520" rx="16" fill="{p['mantle']}"/>

  <!-- Hero Header in Main View -->
  <rect x="292" y="80" width="872" height="150" rx="14" fill="{p['card']}" filter="url(#shadow)"/>
  <rect x="312" y="100" width="110" height="110" rx="12" fill="url(#cardGrad1)"/>
  <text x="444" y="125" fill="{p['accent']}" font-family="system-ui, sans-serif" font-size="12" font-weight="700" letter-spacing="1">PLAYLIST</text>
  <text x="444" y="165" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="32" font-weight="800">Catppuccinify {p['name']}</text>
  <text x="444" y="195" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="14">Official {p['name']} palette with rounded glassmorphism &amp; dynamic switching • 120 songs, 6 hr 42 min</text>

  <!-- Section Title -->
  <text x="292" y="265" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="20" font-weight="700">Made For You</text>
  <text x="1100" y="265" fill="{p['accent']}" font-family="system-ui, sans-serif" font-size="13" font-weight="600" text-anchor="end">Show all</text>

  <!-- Content Cards Grid -->
  <!-- Card 1 -->
  <rect x="292" y="285" width="200" height="260" rx="12" fill="{p['card']}"/>
  <rect x="307" y="300" width="170" height="160" rx="10" fill="url(#cardGrad1)"/>
  <!-- Floating play button -->
  <circle cx="452" cy="435" r="22" fill="{p['accent']}" filter="url(#shadow)"/>
  <polygon points="447,425 463,435 447,445" fill="{p['crust']}"/>
  <text x="307" y="490" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="15" font-weight="600">Daily Mix 1</text>
  <text x="307" y="512" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="13">Lo-fi beats, chill hop</text>

  <!-- Card 2 -->
  <rect x="516" y="285" width="200" height="260" rx="12" fill="{p['card']}"/>
  <rect x="531" y="300" width="170" height="160" rx="10" fill="url(#cardGrad2)"/>
  <text x="531" y="490" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="15" font-weight="600">Deep Focus</text>
  <text x="531" y="512" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="13">Ambient &amp; electronic</text>

  <!-- Card 3 -->
  <rect x="740" y="285" width="200" height="260" rx="12" fill="{p['card']}"/>
  <rect x="755" y="300" width="170" height="160" rx="10" fill="url(#cardGrad3)"/>
  <text x="755" y="490" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="15" font-weight="600">Synthwave City</text>
  <text x="755" y="512" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="13">Retro futuristic drives</text>

  <!-- Card 4 -->
  <rect x="964" y="285" width="200" height="260" rx="12" fill="{p['card']}"/>
  <rect x="979" y="300" width="170" height="160" rx="10" fill="url(#cardGrad1)"/>
  <text x="979" y="490" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="15" font-weight="600">Acoustic Morning</text>
  <text x="979" y="512" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="13">Unplugged warm melodies</text>

  <!-- Now Playing Bar -->
  <rect x="16" y="595" width="{w - 32}" height="70" rx="14" fill="{p['crust']}" filter="url(#shadow)"/>

  <!-- Left: Track info -->
  <rect x="32" y="607" width="46" height="46" rx="8" fill="url(#cardGrad1)"/>
  <text x="90" y="626" fill="{p['text']}" font-family="system-ui, sans-serif" font-size="14" font-weight="600">Resonance (Catppuccin Edit)</text>
  <text x="90" y="644" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="12">HOME • Odyssey</text>

  <!-- Center: Controls -->
  <!-- Prev -->
  <polygon points="560,622 550,630 560,638" fill="{p['subtext']}"/>
  <line x1="548" y1="622" x2="548" y2="638" stroke="{p['subtext']}" stroke-width="2"/>
  <!-- Play/Pause -->
  <circle cx="600" cy="630" r="18" fill="{p['accent']}"/>
  <polygon points="596,623 607,630 596,637" fill="{p['crust']}"/>
  <!-- Next -->
  <polygon points="640,622 650,630 640,638" fill="{p['subtext']}"/>
  <line x1="652" y1="622" x2="652" y2="638" stroke="{p['subtext']}" stroke-width="2"/>

  <!-- Progress Bar -->
  <text x="440" y="658" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="10" text-anchor="end">2:14</text>
  <rect x="450" y="654" width="300" height="4" rx="2" fill="{p['highlight']}"/>
  <rect x="450" y="654" width="165" height="4" rx="2" fill="{p['accent']}"/>
  <circle cx="615" cy="656" r="5" fill="{p['text']}"/>
  <text x="760" y="658" fill="{p['subtext']}" font-family="system-ui, sans-serif" font-size="10">3:32</text>

  <!-- Right: Volume & extras -->
  <rect x="1040" y="628" width="80" height="4" rx="2" fill="{p['highlight']}"/>
  <rect x="1040" y="628" width="55" height="4" rx="2" fill="{p['accent_alt']}"/>
  <circle cx="1095" cy="630" r="4" fill="{p['text']}"/>
  <path d="M1130 626 L1134 626 L1138 622 L1138 638 L1134 634 L1130 634 Z" fill="{p['subtext']}"/>
</svg>"""

def render_showcase_svg():
    w, h = 1200, 700
    return f"""<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <filter id="cardShadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#000000" flood-opacity="0.45"/>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="{w}" height="{h}" fill="#11111B"/>

  <!-- Title & Subtitle -->
  <text x="{w/2}" y="56" fill="#CDD6F4" font-family="system-ui, sans-serif" font-size="32" font-weight="800" text-anchor="middle">Catppuccinify - 4 Soothing Flavors</text>
  <text x="{w/2}" y="88" fill="#A6ADC8" font-family="system-ui, sans-serif" font-size="16" font-weight="500" text-anchor="middle">Seamless dynamic switching across all official Catppuccin colorways</text>

  <!-- 4 Columns Showcase -->
  <!-- 1. Mocha -->
  <g transform="translate(40, 120)">
    <rect width="260" height="520" rx="16" fill="{PALETTES['mocha']['base']}" filter="url(#cardShadow)"/>
    <rect width="260" height="70" rx="16" fill="{PALETTES['mocha']['mantle']}"/>
    <rect y="50" width="260" height="20" fill="{PALETTES['mocha']['mantle']}"/>
    <circle cx="30" cy="35" r="8" fill="{PALETTES['mocha']['accent']}"/>
    <text x="50" y="40" fill="{PALETTES['mocha']['text']}" font-family="system-ui, sans-serif" font-size="18" font-weight="700">Mocha</text>
    <text x="30" y="105" fill="{PALETTES['mocha']['subtext']}" font-family="system-ui, sans-serif" font-size="12" font-weight="600">DARKEST • DEFAULT</text>

    <!-- Mini UI Mockup -->
    <rect x="20" y="125" width="220" height="120" rx="12" fill="{PALETTES['mocha']['card']}"/>
    <circle cx="50" cy="160" r="16" fill="{PALETTES['mocha']['accent']}"/>
    <rect x="80" y="150" width="130" height="10" rx="5" fill="{PALETTES['mocha']['text']}"/>
    <rect x="80" y="168" width="90" height="8" rx="4" fill="{PALETTES['mocha']['subtext']}"/>
    <rect x="20" y="200" width="220" height="4" rx="2" fill="{PALETTES['mocha']['highlight']}"/>
    <rect x="20" y="200" width="140" height="4" rx="2" fill="{PALETTES['mocha']['accent']}"/>

    <!-- Swatches -->
    <text x="20" y="275" fill="{PALETTES['mocha']['text']}" font-family="system-ui, sans-serif" font-size="13" font-weight="600">Palette Swatches</text>
    <g transform="translate(20, 290)">
      <circle cx="15" cy="15" r="12" fill="#F5E0DC"/>
      <circle cx="45" cy="15" r="12" fill="#F5C2E7"/>
      <circle cx="75" cy="15" r="12" fill="#CBA6F7"/>
      <circle cx="105" cy="15" r="12" fill="#F38BA8"/>
      <circle cx="135" cy="15" r="12" fill="#FAB387"/>
      <circle cx="165" cy="15" r="12" fill="#A6E3A1"/>
      <circle cx="195" cy="15" r="12" fill="#89B4FA"/>
    </g>

    <!-- Code pill -->
    <rect x="20" y="445" width="220" height="42" rx="8" fill="{PALETTES['mocha']['crust']}"/>
    <text x="32" y="471" fill="{PALETTES['mocha']['accent']}" font-family="monospace" font-size="12">color_scheme mocha</text>
  </g>

  <!-- 2. Macchiato -->
  <g transform="translate(325, 120)">
    <rect width="260" height="520" rx="16" fill="{PALETTES['macchiato']['base']}" filter="url(#cardShadow)"/>
    <rect width="260" height="70" rx="16" fill="{PALETTES['macchiato']['mantle']}"/>
    <rect y="50" width="260" height="20" fill="{PALETTES['macchiato']['mantle']}"/>
    <circle cx="30" cy="35" r="8" fill="{PALETTES['macchiato']['accent']}"/>
    <text x="50" y="40" fill="{PALETTES['macchiato']['text']}" font-family="system-ui, sans-serif" font-size="18" font-weight="700">Macchiato</text>
    <text x="30" y="105" fill="{PALETTES['macchiato']['subtext']}" font-family="system-ui, sans-serif" font-size="12" font-weight="600">MEDIUM DARK</text>

    <!-- Mini UI Mockup -->
    <rect x="20" y="125" width="220" height="120" rx="12" fill="{PALETTES['macchiato']['card']}"/>
    <circle cx="50" cy="160" r="16" fill="{PALETTES['macchiato']['accent']}"/>
    <rect x="80" y="150" width="130" height="10" rx="5" fill="{PALETTES['macchiato']['text']}"/>
    <rect x="80" y="168" width="90" height="8" rx="4" fill="{PALETTES['macchiato']['subtext']}"/>
    <rect x="20" y="200" width="220" height="4" rx="2" fill="{PALETTES['macchiato']['highlight']}"/>
    <rect x="20" y="200" width="140" height="4" rx="2" fill="{PALETTES['macchiato']['accent']}"/>

    <!-- Swatches -->
    <text x="20" y="275" fill="{PALETTES['macchiato']['text']}" font-family="system-ui, sans-serif" font-size="13" font-weight="600">Palette Swatches</text>
    <g transform="translate(20, 290)">
      <circle cx="15" cy="15" r="12" fill="#F4DBD6"/>
      <circle cx="45" cy="15" r="12" fill="#F5BDE6"/>
      <circle cx="75" cy="15" r="12" fill="#C6A0F6"/>
      <circle cx="105" cy="15" r="12" fill="#ED8796"/>
      <circle cx="135" cy="15" r="12" fill="#F5A97F"/>
      <circle cx="165" cy="15" r="12" fill="#A6DA95"/>
      <circle cx="195" cy="15" r="12" fill="#8AADF4"/>
    </g>

    <!-- Code pill -->
    <rect x="20" y="445" width="220" height="42" rx="8" fill="{PALETTES['macchiato']['crust']}"/>
    <text x="32" y="471" fill="{PALETTES['macchiato']['accent']}" font-family="monospace" font-size="12">color_scheme macchiato</text>
  </g>

  <!-- 3. Frappe -->
  <g transform="translate(610, 120)">
    <rect width="260" height="520" rx="16" fill="{PALETTES['frappe']['base']}" filter="url(#cardShadow)"/>
    <rect width="260" height="70" rx="16" fill="{PALETTES['frappe']['mantle']}"/>
    <rect y="50" width="260" height="20" fill="{PALETTES['frappe']['mantle']}"/>
    <circle cx="30" cy="35" r="8" fill="{PALETTES['frappe']['accent']}"/>
    <text x="50" y="40" fill="{PALETTES['frappe']['text']}" font-family="system-ui, sans-serif" font-size="18" font-weight="700">Frappé</text>
    <text x="30" y="105" fill="{PALETTES['frappe']['subtext']}" font-family="system-ui, sans-serif" font-size="12" font-weight="600">LOW CONTRAST DARK</text>

    <!-- Mini UI Mockup -->
    <rect x="20" y="125" width="220" height="120" rx="12" fill="{PALETTES['frappe']['card']}"/>
    <circle cx="50" cy="160" r="16" fill="{PALETTES['frappe']['accent']}"/>
    <rect x="80" y="150" width="130" height="10" rx="5" fill="{PALETTES['frappe']['text']}"/>
    <rect x="80" y="168" width="90" height="8" rx="4" fill="{PALETTES['frappe']['subtext']}"/>
    <rect x="20" y="200" width="220" height="4" rx="2" fill="{PALETTES['frappe']['highlight']}"/>
    <rect x="20" y="200" width="140" height="4" rx="2" fill="{PALETTES['frappe']['accent']}"/>

    <!-- Swatches -->
    <text x="20" y="275" fill="{PALETTES['frappe']['text']}" font-family="system-ui, sans-serif" font-size="13" font-weight="600">Palette Swatches</text>
    <g transform="translate(20, 290)">
      <circle cx="15" cy="15" r="12" fill="#F2D5CF"/>
      <circle cx="45" cy="15" r="12" fill="#F4B8E4"/>
      <circle cx="75" cy="15" r="12" fill="#CA9EE6"/>
      <circle cx="105" cy="15" r="12" fill="#E78284"/>
      <circle cx="135" cy="15" r="12" fill="#EF9F76"/>
      <circle cx="165" cy="15" r="12" fill="#A6D189"/>
      <circle cx="195" cy="15" r="12" fill="#8CAAEE"/>
    </g>

    <!-- Code pill -->
    <rect x="20" y="445" width="220" height="42" rx="8" fill="{PALETTES['frappe']['crust']}"/>
    <text x="32" y="471" fill="{PALETTES['frappe']['accent']}" font-family="monospace" font-size="12">color_scheme frappe</text>
  </g>

  <!-- 4. Latte -->
  <g transform="translate(895, 120)">
    <rect width="260" height="520" rx="16" fill="{PALETTES['latte']['base']}" filter="url(#cardShadow)"/>
    <rect width="260" height="70" rx="16" fill="{PALETTES['latte']['mantle']}"/>
    <rect y="50" width="260" height="20" fill="{PALETTES['latte']['mantle']}"/>
    <circle cx="30" cy="35" r="8" fill="{PALETTES['latte']['accent']}"/>
    <text x="50" y="40" fill="{PALETTES['latte']['text']}" font-family="system-ui, sans-serif" font-size="18" font-weight="700">Latte</text>
    <text x="30" y="105" fill="{PALETTES['latte']['subtext']}" font-family="system-ui, sans-serif" font-size="12" font-weight="600">OFFICIAL LIGHT THEME</text>

    <!-- Mini UI Mockup -->
    <rect x="20" y="125" width="220" height="120" rx="12" fill="{PALETTES['latte']['card']}"/>
    <circle cx="50" cy="160" r="16" fill="{PALETTES['latte']['accent']}"/>
    <rect x="80" y="150" width="130" height="10" rx="5" fill="{PALETTES['latte']['text']}"/>
    <rect x="80" y="168" width="90" height="8" rx="4" fill="{PALETTES['latte']['subtext']}"/>
    <rect x="20" y="200" width="220" height="4" rx="2" fill="{PALETTES['latte']['highlight']}"/>
    <rect x="20" y="200" width="140" height="4" rx="2" fill="{PALETTES['latte']['accent']}"/>

    <!-- Swatches -->
    <text x="20" y="275" fill="{PALETTES['latte']['text']}" font-family="system-ui, sans-serif" font-size="13" font-weight="600">Palette Swatches</text>
    <g transform="translate(20, 290)">
      <circle cx="15" cy="15" r="12" fill="#DC8A78"/>
      <circle cx="45" cy="15" r="12" fill="#EA76CB"/>
      <circle cx="75" cy="15" r="12" fill="#8839EF"/>
      <circle cx="105" cy="15" r="12" fill="#D20F39"/>
      <circle cx="135" cy="15" r="12" fill="#FE640B"/>
      <circle cx="165" cy="15" r="12" fill="#40A02B"/>
      <circle cx="195" cy="15" r="12" fill="#1E66F5"/>
    </g>

    <!-- Code pill -->
    <rect x="20" y="445" width="220" height="42" rx="8" fill="{PALETTES['latte']['crust']}"/>
    <text x="32" y="471" fill="{PALETTES['latte']['accent']}" font-family="monospace" font-size="12">color_scheme latte</text>
  </g>
</svg>"""

print("🎨 Generating preview SVGs and PNGs...")

# Generate showcase
showcase_svg = os.path.join(ASSETS_DIR, "flavor-showcase.svg")
showcase_png = os.path.join(ASSETS_DIR, "flavor-showcase.png")
with open(showcase_svg, "w") as f:
    f.write(render_showcase_svg())
subprocess.run(["ffmpeg", "-y", "-i", showcase_svg, showcase_png], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(f"  + Generated: {showcase_png}")

# Generate individual flavor previews
for key, palette in PALETTES.items():
    svg_file = os.path.join(ASSETS_DIR, f"preview-{key}.svg")
    png_file = os.path.join(ASSETS_DIR, f"preview-{key}.png")
    with open(svg_file, "w") as f:
        f.write(render_preview_svg(key, palette))
    subprocess.run(["ffmpeg", "-y", "-i", svg_file, png_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  + Generated: {png_file}")

print("✨ All preview images generated successfully!")
