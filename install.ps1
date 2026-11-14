# Link the skill into Claude Code on Windows (a directory junction needs no admin rights).
# `git pull` in this repo then keeps the skill current.
$src = Join-Path $PSScriptRoot "skill\pinterest-taste"
$skills = Join-Path $HOME ".claude\skills"
$dest = Join-Path $skills "pinterest-taste"
New-Item -ItemType Directory -Force $skills | Out-Null
if (Test-Path $dest) {
    $item = Get-Item $dest -Force
    if ($item.LinkType -ne "Junction") { throw "$dest exists and is not a link; move it away first." }
    $item.Delete()
}
New-Item -ItemType Junction -Path $dest -Target $src | Out-Null
Write-Output "linked $dest -> $src"
