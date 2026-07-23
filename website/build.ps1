# Build wrapper for the SkillFishOS website on Windows + Dropbox.
#
# Root problem: Astro stages its build in <project>/.astro (pages, client assets,
# image service). Our project lives in a Dropbox-synced folder, and Dropbox's
# filesystem filter locks .astro during the final consolidation -> `astro build`
# dies with `EBUSY ... rmdir '...\.astro\...'` AFTER writing the HTML but BEFORE
# copying _astro CSS and public/ assets into the output. Result: an HTML-only,
# broken dist. `cacheDir`/`outDir` config can't relocate <root>/.astro, and a
# junction at <root>/.astro is refused by Dropbox's cloud filter.
#
# Fix: copy the source OUT of Dropbox and build there (node_modules is junctioned
# from the real one - the junction is created outside Dropbox, which is allowed).
# outDir / cacheDir / vite.cacheDir already point to %TEMP% (see astro.config.mjs).
$ErrorActionPreference = 'Continue'
$proj  = $PSScriptRoot
$build = Join-Path $env:TEMP 'skfweb-build'
$out   = Join-Path $env:TEMP 'skillfishos-website-dist'

if (-not (Test-Path $build)) { New-Item -ItemType Directory -Force -Path $build | Out-Null }

# Mirror the source into the out-of-Dropbox build dir (skip heavy/derived dirs).
robocopy $proj $build /MIR /XD node_modules .astro dist .git /NFL /NDL /NJH /NJS /NP /R:1 /W:1 | Out-Null

# node_modules via junction (created outside Dropbox => not blocked by the cloud filter).
$nm = Join-Path $build 'node_modules'
if (-not (Test-Path $nm)) { cmd /c mklink /J "$nm" (Join-Path $proj 'node_modules') | Out-Null }

Push-Location $build
npm run build
Pop-Location

if (Test-Path (Join-Path $out 'index.html')) {
    $n   = (Get-ChildItem -Recurse $out -Filter *.html).Count
    $css = (Get-ChildItem -Recurse $out -Filter *.css -ErrorAction SilentlyContinue).Count
    $img = (Get-ChildItem (Join-Path $out 'img') -ErrorAction SilentlyContinue).Count
    Write-Host ("[build.ps1] OK - {0} HTML, {1} CSS, {2} img in {3}" -f $n, $css, $img, $out) -ForegroundColor Green
    if ($css -lt 1 -or $img -lt 1) {
        Write-Host "[build.ps1] WARNING: assets missing - dist looks incomplete!" -ForegroundColor Red
        exit 1
    }
    exit 0
}
Write-Host ("[build.ps1] FAILED - no output in {0}" -f $out) -ForegroundColor Red
exit 1
