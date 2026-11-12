import subprocess

upstream_css = subprocess.check_output(["git", "show", "upstream/main:user.css"]).decode("utf-8")

# In upstream css, apply the specific tweaks:
upstream_css = upstream_css.replace(
""".QTPPCyC4V18wBUZA {
  background-color: transparent;
}""",
""".QTPPCyC4V18wBUZA {
  display: none;
}"""
)

upstream_css = upstream_css.replace(
""".JDUQ8zTo6EUgHoYt {
  height: fit-content;
  padding: 20px;
  border-radius: 20px;
  box-shadow: var(--liquify-shadow);
}""",
""".JDUQ8zTo6EUgHoYt {
  height: fit-content;
  padding: 20px;
  margin-bottom: 20px;
  border-radius: 20px;
  box-shadow: var(--liquify-shadow);
}"""
)

catppuccin_base = """

/* ════════════════════════════════════════════════════════════════════
   Material base – transparency removed (shapes preserved)
   --------------------------------------------------------------------
   This section removes the glass transparency. Every radius, margin,
   animation and hover effect from the original theme above stays intact.
   All surfaces become solid tonal fills; backdrop refraction is disabled
   app-wide (the GlassSurface classes injected by theme.js become no-ops).

   Color tokens come from the active Catppuccin scheme (color.ini):
     --spice-main / --spice-sidebar / --spice-player / --spice-card /
     --spice-text / --spice-subtext / --spice-highlight / --spice-button
   ════════════════════════════════════════════════════════════════════ */

:root {
  /* Kill the glass rim shadows (inset highlights) – solid surfaces don't
     refract light, so the rim reads as noise. */
  --liquify-shadow: none;

  /* Tonal surface tokens (solid) */
  --liquify-surface: var(--spice-main, #121212);
  --liquify-surface-1: color-mix(in srgb, var(--spice-card, #282828) 55%, var(--spice-main, #121212));
  --liquify-surface-2: var(--spice-card, #282828);
  --liquify-surface-3: color-mix(in srgb, var(--spice-card, #282828) 82%, var(--spice-highlight, #3e3e3e));

  /* Text-on-accent: uses the JS-computed secondary color when the sampled
     accent is too light/dark (black/white covers), so contrast holds. */
  --liquify-on-accent: var(--accent-on-accent, var(--spice-shadow, #000));
  --liquify-accent-2: var(--accent-color-secondary, var(--spice-subtext, #b3b3b3));
}

/* ── App-wide solid base ─────────────────────────────────────────── */

html,
body,
.Root__top-container,
.Root__nav-bar,
.Root__main-view,
.Root__right-sidebar,
.Root__now-playing-bar,
.main-root-wrapper,
.main-view-container,
.main-view-container__scroll-node-child,
.main-view-container__scroll-node,
.os-viewport {
  background-color: var(--spice-main, #121212);
}

.Root__nav-bar,
.Root__right-sidebar {
  background-color: var(--spice-sidebar, #181818);
}

.Root__now-playing-bar {
  background-color: var(--spice-player, #181818) !important;
}

/* ── Keep runtime glass markers visually neutral by default ───────── */

.liquify-glass,
.liquify-glass--svg,
.liquify-glass--simple,
.liquify-glass--before::before,
.liquify-glass--svg.liquify-glass--before::before,
.liquify-glass--simple.liquify-glass--before::before {
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  background: transparent !important;
}

/* Dynamic cover layers keep the ambient tint but no blur/brightness */
.liquify-bg-layer {
  filter: brightness(0.55) !important;
  background-color: var(--spice-main, #121212);
  background-blend-mode: overlay;
}

.liquify-animated-bg {
  filter: none !important;
  opacity: 0 !important;
}

.liquify-animated-tile {
  display: none !important;
}

/* ── Solid surfaces for every glass target (both legacy and new Spotify) ── */

.main-topBar-background,
.zddkQq3wlxEOg6aa,
.main-trackList-trackListHeader,
.Root__now-playing-bar,
.main-globalNav-searchInputContainer .main-topBar-searchBar,
.Root__globalNav .main-globalNav-navLink,
.NJh1B8rnlSUlK7sY,
.search-searchCategory-carouselButton,
.e-10451-box--tinted,
.e-10860-box--tinted,
.main-entityHeader-container,
.main-actionBar-ActionBar,
.main-nowPlayingView-headerWrapper,
.main-nowPlayingView-section,
.main-nowPlayingView-trackInfo,
.main-contextMenu-tippy,
.PromotionButtonTooltip-module_tooltip-animation__cE-rt,
.iiX8td2tfVETS09_ button,
.gpBiAnJHb1gq46qV,
.view-homeShortcutsGrid-shortcut,
.main-home-filterChipsSection,
dialog,
.main-topBar-buddyFeed,
.main-userWidget-box,
.main-globalNav-historyButtons,
.EU1ylDKh7s2oMU0g,
.VwcQJ4Zsf0JKD3Ls,
.KQDsZX3kwwuAFpE8,
.KFAJvMWTSagxYXGC,
.main-trackList-trackListRow.q8suB2R_XkoUyIeZ,
.main-nowPlayingView-actionButton,
.main-playlistEditDetailsModal-container,
.main-playlistEditDetailsModal-imageDropDownButton,
.main-home-content section,
.os-scrollbar-handle,
.JDUQ8zTo6EUgHoYt,
.B9ji6YIpLSUHiyxx,
.gu0S9_98ZXIo5DaV,
.SUjhgyMvTou7TddO,
.ERRo1Br0ZQtJYVhz,
.LR7w41pC8ccVc11Q,
.VsYY0YB3c4lmhoDI,
.main-shelf-shelf,
.CO34wNPAbR8mpcdD,
.JthDv0xUCm8rLhu6,
.tlq9Tt69FX4bauLX,
.x-settings-section,
.fa_L1qIbh7QDDd_h,
.TguLwQ522LIEgpK_.IxVxBUbV5M5tGaEx,
.HOf9H18Ya0DkJ4_K,
.main-nowPlayingView-onTourItemGrid:hover,
.qm0mrbeno_z0mpoo,
.N3kf5S8O84aeaCZu,
.J8g7rZ2MDknxmiYP,
.Root__cinema-view,
.n5KI8mwa5o8qbn4b,
.vado7sbDrEsKhSmn,
.main-embedWidgetGenerator-container,
.e-10451-box--elevated,
.e-10860-legacy-box--elevated,
.Wzl40f9FIUD91O2o,
.mcZzjuAJUvE9X4gX,
.Htdd9HRV28F07Dwl,
.p67WtOnm9lsRLOu2,
.JLkvt5ABTQYw_rG7,
.mKvcoJ_veYlcHwOz,
.tMcqYZ2om0nYbgrw,
.yZCluNwEsPD2zYyY,
.Hrce4GF4EEkPJdBI,
.EpfIE3glwAOGcNT6,
.main-contextMenu-menu,
.xamNkt5LX9o8aL1q,
.marketplace-header,
.marketplace-tabBar-active,
.Dropdown-menu,
#marketplace-readme,
.liquifySettingsPanel,
.liquifySelectMenu,
.liquifySectionNavScrollBtn,
#liquify-next-song-card,
.main-card-card,
#liquify-settings-gear-btn,
.artist-artistDiscography-topBar.artist-artistDiscography-topBarScrolled,
.wJiY1vDfuci2a4db,
.oc3OomY6r9UoIEQ0,
.oReO3E1Df2odSFHX,
.fA6CNWFY1WQBCde9,
.main-trackCreditsModal-container,
.TGvpaalpJK0BKYYL,
.edvX5XPBIXITSQoH {
  background-color: var(--liquify-surface-1, #181818) !important;
}

/* Slightly lighter where the original glass was most prominent */
.main-nowPlayingView-trackInfo,
.main-nowPlayingView-headerWrapper,
.main-entityHeader-container,
.main-actionBar-ActionBar,
.main-contextMenu-menu,
.xamNkt5LX9o8aL1q,
.Dropdown-menu,
.liquifySettingsPanel,
.NJh1B8rnlSUlK7sY,
.zddkQq3wlxEOg6aa,
dialog,
.main-trackCreditsModal-container,
.main-playlistEditDetailsModal-container,
.main-embedWidgetGenerator-container {
  background-color: var(--liquify-surface-2, #242424) !important;
}

/* Elevated flyouts get the brightest surface + a soft drop shadow */
.main-contextMenu-menu,
.xamNkt5LX9o8aL1q,
.Dropdown-menu,
.liquifySettingsPanel,
dialog {
  background-color: var(--liquify-surface-3, #2a2a2a) !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5) !important;
}

/* Keep hover states tonal instead of transparent */
.main-card-card:hover,
.view-homeShortcutsGrid-shortcut:hover,
.main-trackList-trackListRow:hover,
.main-nowPlayingView-artistOnTourItem:hover,
.e-10451-box--interactive:hover,
.e-10860-legacy-box--interactive:hover,
.main-contextMenu-menuItemButton:hover {
  background-color: color-mix(in srgb, var(--spice-highlight, #3e3e3e) 55%, transparent) !important;
}

/* ── Contrast-safe accent usage ──────────────────────────────────── */

/* Text on accent-filled buttons uses the JS-computed on-accent color,
   so a white/black sampled accent never produces unreadable text. */
.e-10451-legacy-button-primary,
.e-10860-legacy-button-primary,
.e-10451-button-primary,
.e-10860-button-primary,
button.e-10451-legacy-button-primary,
button.e-10860-legacy-button-primary,
.main-playButton-PlayButton button,
button[data-testid="play-button"],
.encore-bright-accent-set {
  color: var(--liquify-on-accent, #000) !important;
}

/* Secondary accent surfaces (chips, toggles, highlights) */
.e-10451-legacy-chip__inner--selected,
.e-10860-legacy-chip__inner--selected,
.main-actionBar-ActionBar button[data-testid="action-bar-row"] > button,
.main-trackList-trackListRow[aria-selected="true"] {
  background-color: var(--accent-color, #1ed760) !important;
  color: var(--liquify-on-accent, #000) !important;
}

/* Where a very dark sampled accent would hide icons/text, use the
   secondary (contrast-checked) color instead. */
.main-actionBar-ActionBar button[data-testid="action-bar-row"] > button:hover,
.main-playButton-PlayButton button:hover,
button[data-testid="play-button"]:hover,
.e-10451-legacy-button-primary:hover,
.e-10860-legacy-button-primary:hover,
.e-10451-button-primary:hover,
.e-10860-button-primary:hover {
  background-color: var(--accent-color-secondary, var(--spice-highlight, #45475a)) !important;
  color: var(--liquify-on-accent, #000) !important;
}

/* Settings panel accent hover states also switch to the secondary */
.liquifyHeaderActionBtn:hover,
.liquifyStepperBtn:hover,
.liquifySectionNavScrollBtn:hover,
.liquifySectionNavBtn:hover,
.liquifyActionBtn:hover,
.liquifyConfigApplyBtn:hover {
  background: var(--accent-color-secondary, var(--spice-subtext, #b3b3b3)) !important;
}

/* Progress / volume bars keep the accent; the thumb stays visible */
.Root__now-playing-bar .progress-bar .progress-bar__slider,
.Root__now-playing-bar .volume-bar .progress-bar__slider {
  background-color: var(--accent-color, #cba6f7) !important;
}

/* Placeholder text is unreadable on light covers otherwise */
::-webkit-input-placeholder {
  color: var(--spice-subtext, #b3b3b3);
}

/* ══════════════════════ Settings menu cleanup ══════════════════════ */

#liquify-settings-react-overlay .liquifySettingsBody #liquify-sec-nextSongCard,
#liquify-settings-react-overlay .liquifySettingsBody #liquify-sec-canvasCoverArt,
#liquify-settings-react-overlay .liquifySettingsBody #liquify-sec-playlist,
#liquify-settings-react-overlay .liquifySettingsBody #liquify-sec-transparent {
  display: none !important;
}

/* The reset-all button sits at the very bottom of the panel; with the
   removed sections it now follows the Config section. Give it some air. */
.liquifySettingsPanel .liquifyResetBtn {
  margin-top: 8px;
}

/* ── Right Now Playing header ─────────────────────────────────────── */

.main-nowPlayingView-headerWrapper.liquify-npv-header-at-top {
  background: var(--liquify-surface-1, #181825) !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  transition: background-color 0.2s ease;
}

.main-nowPlayingView-headerWrapper.liquify-npv-header-scrolled {
  background: var(--liquify-surface-2, #242424) !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.28) !important;
  transition: background-color 0.2s ease, box-shadow 0.2s ease;
}

/* ── Liquid Lyrics viewport and controls ──────────────────────────── */

.liquify-lyrics-viewport {
  position: relative;
  min-height: 0 !important;
  max-height: 100% !important;
  overflow: hidden !important;
  overscroll-behavior: contain;
  contain: layout paint;
}

.liquify-lyrics-viewport .lyrics-lyrics-contentContainer,
.liquify-lyrics-content {
  min-height: 0 !important;
  max-height: 100% !important;
  overflow: auto !important;
  overscroll-behavior: contain;
  scroll-padding-block: 24px;
}

/* ── Artist selection and banner image fitting ───────────────────── */

.main-trackList-trackListRow:is(
  [aria-selected="true"],
  [data-selected="true"],
  .selected,
  .is-selected,
  .liquify-artist-row-selected
),
.main-trackList-trackListRow:is(
  [aria-selected="true"],
  [data-selected="true"],
  .selected,
  .is-selected,
  .liquify-artist-row-selected
):hover {
  background: var(--accent-color, #1ed760) !important;
  color: var(--liquify-on-accent, #000) !important;
  box-shadow: 0 0 0 1px color-mix(in srgb, var(--accent-color, #1ed760) 70%, transparent) !important;
  transform: none !important;
}

.main-trackList-trackListRow:is(
  [aria-selected="true"],
  [data-selected="true"],
  .selected,
  .is-selected,
  .liquify-artist-row-selected
) * {
  color: inherit !important;
}

.main-entityHeader-image,
.main-entityHeader-image img,
.main-entityHeader-imageContainerWrapper {
  background-size: cover !important;
  background-position: center center !important;
  background-repeat: no-repeat !important;
}

.main-entityHeader-image img {
  width: 100% !important;
  height: 100% !important;
  object-fit: cover !important;
  object-position: center center !important;
}

/* Prevent the generic legacy-button hover animation from affecting lyrics. */
.lyrics-lyrics-background .e-10451-legacy-button:hover,
.lyrics-lyrics-background .e-10860-legacy-button:hover,
.lyrics-lyrics-contentContainer .e-10451-legacy-button:hover,
.lyrics-lyrics-contentContainer .e-10860-legacy-button:hover {
  transform: none !important;
  box-shadow: none !important;
}

/* Keep a visible gap between consecutive artist content blocks. */
.artist-artistDiscography-headerContainer + .artist-artistDiscography-content,
.artist-artistDiscography-content + .artist-artistDiscography-content,
.artist-artistDiscography-content > section + section {
  margin-top: 16px !important;
}

/* The banner controller owns visibility; the image must fill its existing box. */
.jiWxWueoicolJZnS:not(.liquify-artist-banner-hidden),
.jiWxWueoicolJZnS:not(.liquify-artist-banner-hidden) img,
.main-entityHeader-image:not(.liquify-artist-banner-hidden),
.main-entityHeader-image:not(.liquify-artist-banner-hidden) img {
  opacity: 1 !important;
}

.jiWxWueoicolJZnS.liquify-artist-banner-hidden,
.jiWxWueoicolJZnS.liquify-artist-banner-hidden img {
  opacity: 0 !important;
}
"""

full_css = upstream_css + catppuccin_base

with open("user.css", "w", encoding="utf-8") as f:
    f.write(full_css)

print("✅ Successfully updated user.css with latest upstream and Catppuccin Material styles!")
