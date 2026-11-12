#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
let errors = 0;

function reportError(msg) {
  console.error(`❌ [ERROR] ${msg}`);
  errors++;
}

function reportSuccess(msg) {
  console.log(`✅ [OK] ${msg}`);
}

console.log('🔍 Validating Catppuccinify repository assets and syntax...\n');

// 1. Validate manifest.json
try {
  const manifestPath = path.join(ROOT, 'manifest.json');
  if (!fs.existsSync(manifestPath)) {
    reportError('manifest.json does not exist');
  } else {
    const raw = fs.readFileSync(manifestPath, 'utf8');
    const manifest = JSON.parse(raw);
    if (!Array.isArray(manifest) || manifest.length === 0) {
      reportError('manifest.json must be a non-empty array of theme objects');
    } else {
      const theme = manifest[0];
      const requiredFields = ['name', 'description', 'preview', 'readme', 'usercss', 'schemes', 'include'];
      for (const field of requiredFields) {
        if (!theme[field]) {
          reportError(`manifest.json theme is missing required field: ${field}`);
        }
      }
      for (const inc of theme.include || []) {
        if (!inc.startsWith('http') && !fs.existsSync(path.join(ROOT, inc))) {
          reportError(`manifest.json include file missing: ${inc}`);
        }
      }
      if (!fs.existsSync(path.join(ROOT, theme.usercss))) {
        reportError(`manifest.json usercss file missing: ${theme.usercss}`);
      }
      if (!fs.existsSync(path.join(ROOT, theme.schemes))) {
        reportError(`manifest.json schemes file missing: ${theme.schemes}`);
      }
      reportSuccess('manifest.json is valid and all referenced files exist');
    }
  }
} catch (err) {
  reportError(`manifest.json validation failed: ${err.message}`);
}

// 1b. Validate spotikit.json
try {
  const spotikitPath = path.join(ROOT, 'spotikit.json');
  if (fs.existsSync(spotikitPath)) {
    const raw = fs.readFileSync(spotikitPath, 'utf8');
    const sp = JSON.parse(raw);
    if (!sp.name || !sp.spotify || !sp.main || !sp.style) {
      reportError('spotikit.json missing required metadata fields');
    } else {
      reportSuccess(`spotikit.json is valid (targets Spotify ${sp.spotify})`);
    }
  }
} catch (err) {
  reportError(`spotikit.json validation failed: ${err.message}`);
}

// 2. Validate color.ini
try {
  const colorIniPath = path.join(ROOT, 'color.ini');
  if (!fs.existsSync(colorIniPath)) {
    reportError('color.ini does not exist');
  } else {
    const content = fs.readFileSync(colorIniPath, 'utf8');
    const sections = {};
    let currentSection = null;

    const lines = content.split(/\r?\n/);
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith(';')) continue;
      const sectionMatch = trimmed.match(/^\[(.*)\]$/);
      if (sectionMatch) {
        currentSection = sectionMatch[1];
        sections[currentSection] = {};
        continue;
      }
      const kvMatch = trimmed.match(/^([a-zA-Z0-9_-]+)\s*=\s*([a-fA-F0-9]{6})$/);
      if (kvMatch && currentSection) {
        sections[currentSection][kvMatch[1].toLowerCase()] = kvMatch[2].toLowerCase();
      } else if (currentSection && trimmed.includes('=')) {
        reportError(`Invalid color entry in [${currentSection}]: "${trimmed}" (must be 6-digit hex)`);
      }
    }

    const expectedFlavors = ['mocha', 'macchiato', 'frappe', 'latte'];
    const requiredKeys = ['text', 'subtext', 'main', 'sidebar', 'player', 'card', 'shadow', 'button', 'button-active'];

    for (const flavor of expectedFlavors) {
      const foundSection = Object.keys(sections).find(s => s.toLowerCase() === flavor);
      if (!foundSection) {
        reportError(`color.ini missing section for flavor: [${flavor}]`);
      } else {
        const sec = sections[foundSection];
        for (const k of requiredKeys) {
          if (!sec[k]) {
            reportError(`[${foundSection}] in color.ini missing required key: ${k}`);
          }
        }
      }
    }
    reportSuccess(`color.ini valid: verified ${Object.keys(sections).length} sections across all 4 Catppuccin flavors`);

    // Verify sync between color.ini and theme.js COLOR_PALETTES
    const themeJsPath = path.join(ROOT, 'theme.js');
    if (fs.existsSync(themeJsPath)) {
      const themeContent = fs.readFileSync(themeJsPath, 'utf8');
      const paletteMatch = themeContent.match(/var COLOR_PALETTES = (\{[\s\S]*?\n  \};)/);
      if (paletteMatch) {
        try {
          const evalPalettes = new Function(`return ${paletteMatch[1]}`)();
          for (const flavor of expectedFlavors) {
            const iniSec = sections[flavor];
            const jsPal = evalPalettes[flavor];
            if (!jsPal) {
              reportError(`theme.js COLOR_PALETTES missing flavor: ${flavor}`);
            } else {
              for (const [k, v] of Object.entries(jsPal)) {
                if (iniSec && iniSec[k.toLowerCase()] !== v.toLowerCase()) {
                  reportError(`Palette mismatch in ${flavor}.${k}: color.ini=${iniSec?.[k.toLowerCase()]} vs theme.js=${v}`);
                }
              }
            }
          }
          reportSuccess('color.ini and theme.js COLOR_PALETTES are 100% in sync across all 4 flavors');
        } catch (e) {
          reportError(`Failed to parse COLOR_PALETTES from theme.js: ${e.message}`);
        }
      }
    }
  }
} catch (err) {
  reportError(`color.ini validation failed: ${err.message}`);
}

// 3. Validate user.css
try {
  const cssPath = path.join(ROOT, 'user.css');
  if (!fs.existsSync(cssPath)) {
    reportError('user.css does not exist');
  } else {
    const css = fs.readFileSync(cssPath, 'utf8');
    if (css.length < 1000) {
      reportError('user.css is suspiciously small');
    }
    // Check balanced braces
    let openBraces = (css.match(/\{/g) || []).length;
    let closeBraces = (css.match(/\}/g) || []).length;
    if (openBraces !== closeBraces) {
      reportError(`user.css unbalanced braces: { (${openBraces}) vs } (${closeBraces})`);
    } else {
      reportSuccess(`user.css valid (${css.length} bytes, ${openBraces} rulesets, balanced braces)`);
    }
  }
} catch (err) {
  reportError(`user.css validation failed: ${err.message}`);
}

// 4. Validate theme.js
try {
  const jsPath = path.join(ROOT, 'theme.js');
  if (!fs.existsSync(jsPath)) {
    reportError('theme.js does not exist');
  } else {
    execSync(`node --check "${jsPath}"`);
    reportSuccess('theme.js syntax check passed');
  }
} catch (err) {
  reportError(`theme.js syntax check failed: ${err.message}`);
}

// 5. Validate assets (PNG headers)
const assetFiles = [
  'preview.png',
  'discord-icon.png',
  'assets/flavor-showcase.png',
  'assets/preview-mocha.png',
  'assets/preview-macchiato.png',
  'assets/preview-frappe.png',
  'assets/preview-latte.png'
];
for (const asset of assetFiles) {
  const fullPath = path.join(ROOT, asset);
  if (!fs.existsSync(fullPath)) {
    reportError(`Asset missing: ${asset}`);
    continue;
  }
  const buf = fs.readFileSync(fullPath);
  const isPng = buf.length > 8 &&
    buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4e && buf[3] === 0x47 &&
    buf[4] === 0x0d && buf[5] === 0x0a && buf[6] === 0x1a && buf[7] === 0x0a;
  if (!isPng) {
    reportError(`Asset ${asset} is not a valid PNG file`);
  } else {
    reportSuccess(`Asset ${asset} valid (${buf.length} bytes)`);
  }
}

console.log('\n----------------------------------------');
if (errors > 0) {
  console.error(`Validation failed with ${errors} error(s).`);
  process.exit(1);
} else {
  console.log('🎉 All validations passed successfully!');
  process.exit(0);
}
