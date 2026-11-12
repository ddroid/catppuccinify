# Catppuccinify Spicetify Theme Installer for Windows (PowerShell)
# Usage:
#   iwr -useb https://raw.githubusercontent.com/ddroid/catppuccinify/main/install.ps1 | iex
#   & ([scriptblock]::Create((iwr -useb https://raw.githubusercontent.com/ddroid/catppuccinify/main/install.ps1))) -Flavor latte

param (
    [string]$Flavor = "mocha"
)

Write-Host "Catppuccinify Spicetify Theme Installer" -ForegroundColor Magenta

# Check spicetify
if (-not (Get-Command spicetify -ErrorAction SilentlyContinue)) {
    Write-Host "Error: spicetify CLI was not found in PATH." -ForegroundColor Red
    Write-Host "Please install Spicetify first: https://spicetify.app/docs/getting-started" -ForegroundColor Yellow
    exit 1
}

$Flavor = $Flavor.ToLower()
if ($Flavor -eq "frappé") {
    $Flavor = "frappe"
}

$validFlavors = @("mocha", "macchiato", "frappe", "latte")
if ($validFlavors -notcontains $Flavor) {
    Write-Host "Unknown flavor '$Flavor'. Defaulting to mocha." -ForegroundColor Yellow
    $Flavor = "mocha"
}

# Locate themes folder
$spicetifyConfig = spicetify -c 2>$null
if ($spicetifyConfig) {
    $spicetifyDir = Split-Path $spicetifyConfig
} elseif ($env:APPDATA -and (Test-Path (Join-Path $env:APPDATA "spicetify"))) {
    $spicetifyDir = Join-Path $env:APPDATA "spicetify"
} else {
    $spicetifyDir = Join-Path $env:USERPROFILE ".spicetify"
}

$themesDir = Join-Path $spicetifyDir "Themes"
$targetDir = Join-Path $themesDir "catppuccinify"

if (-not (Test-Path $themesDir)) {
    New-Item -ItemType Directory -Path $themesDir -Force | Out-Null
}

Write-Host "Installing Catppuccinify to: $targetDir" -ForegroundColor Cyan

$cloned = $false
if (Test-Path (Join-Path $targetDir ".git")) {
    git -C $targetDir pull --ff-only
    $cloned = ($LASTEXITCODE -eq 0)
} else {
    if (Test-Path $targetDir) {
        Remove-Item -Recurse -Force $targetDir
    }
    if (Get-Command git -ErrorAction SilentlyContinue) {
        git clone --depth 1 "https://github.com/ddroid/catppuccinify.git" $targetDir
        $cloned = ($LASTEXITCODE -eq 0)
    }
}

if (-not $cloned -or -not (Test-Path (Join-Path $targetDir "theme.js"))) {
    Write-Host "Downloading individual theme files directly..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ddroid/catppuccinify/main/color.ini" -OutFile (Join-Path $targetDir "color.ini")
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ddroid/catppuccinify/main/user.css" -OutFile (Join-Path $targetDir "user.css")
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ddroid/catppuccinify/main/theme.js" -OutFile (Join-Path $targetDir "theme.js")
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ddroid/catppuccinify/main/manifest.json" -OutFile (Join-Path $targetDir "manifest.json")
    try {
        Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ddroid/catppuccinify/main/spotikit.json" -OutFile (Join-Path $targetDir "spotikit.json")
    } catch {}
}

Write-Host "Configuring Spicetify..." -ForegroundColor Green
spicetify config current_theme catppuccinify color_scheme $Flavor
spicetify config inject_css 1 inject_theme_js 1 replace_colors 1 overwrite_assets 1

Write-Host "Applying theme to Spotify..." -ForegroundColor Green
spicetify apply
if ($LASTEXITCODE -ne 0) {
    Write-Host "Standard apply returned non-zero. Attempting 'spicetify backup apply'..." -ForegroundColor Yellow
    spicetify backup apply
}

Write-Host "Catppuccinify ($Flavor) installed successfully!" -ForegroundColor Green
