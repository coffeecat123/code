param([string]$path)
if (-not $path) { exit }
$path = $path -replace '\\', '/'
Set-Clipboard -Value "`"$path`""