<#
.SYNOPSIS
  Fingerprint the sources listed in ../references/sources.md and report which moved.

.DESCRIPTION
  Reads the Markdown table in sources.md. For each row:
    - a github.com/<owner>/<repo>/blob/<branch>/<path> URL is fingerprinted as gh:<sha12>,
      the latest commit touching that path (GitHub REST API, unauthenticated: 60 req/h).
    - any other URL is fetched and fingerprinted as sha:<hex12>, the SHA-256 of the page text
      after <script>/<style> blocks, tags and whitespace are stripped.
  Prints one line per row: UNCHANGED | CHANGED | NEW | ERROR, then a summary.

.PARAMETER GateOnly
  Print only the number of days since `last-refresh:` and exit 0 (<= gate) or 1 (> gate).

.PARAMETER GateDays
  The refresh gate in days. Default 7. A `gate-days: N` line in the sources file overrides the default
  when the parameter is not given explicitly (docs-maintainer uses 30).

.PARAMETER Update
  Rewrite sources.md with the new fingerprints, today's `checked` dates and today's `last-refresh`.
  Run only after the refresh report has been shown to the user (refresh.md §5).

.PARAMETER Path
  sources.md location. Defaults to ../references/sources.md relative to this script.
#>
[CmdletBinding()]
param(
  [switch]$GateOnly,
  [switch]$Update,
  [int]$GateDays = 0,
  [string]$Path = (Join-Path $PSScriptRoot '..\references\sources.md')
)

$ErrorActionPreference = 'Stop'
$Path = (Resolve-Path $Path).Path
$raw = [IO.File]::ReadAllText($Path, [Text.Encoding]::UTF8)
$lines = $raw -split "`r?`n"
$today = (Get-Date).ToString('yyyy-MM-dd')

# --- gate -------------------------------------------------------------------
$gateLine = $lines | Where-Object { $_ -match '^last-refresh:\s*(\d{4}-\d{2}-\d{2})' } | Select-Object -First 1
if (-not $gateLine) { Write-Error "sources.md has no 'last-refresh: yyyy-mm-dd' line"; exit 2 }
$lastRefresh = [datetime]::ParseExact($Matches[1], 'yyyy-MM-dd', $null)
$days = [int]((Get-Date).Date - $lastRefresh.Date).TotalDays
if ($GateDays -le 0) {
  $gateLine2 = $lines | Where-Object { $_ -match '^gate-days:\s*(\d+)' } | Select-Object -First 1
  $GateDays = if ($gateLine2) { [int]$Matches[1] } else { 7 }
}
if ($GateOnly) {
  "last-refresh $($lastRefresh.ToString('yyyy-MM-dd')) — $days day(s) ago — gate $GateDays — " + ($(if ($days -gt $GateDays) { 'REFRESH DUE' } else { 'fresh' }))
  exit $(if ($days -gt $GateDays) { 1 } else { 0 })
}

# --- parse table -------------------------------------------------------------
$rows = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
  $l = $lines[$i]
  if ($l -notmatch '^\|') { continue }
  $cells = ($l.Trim() -replace '^\|', '' -replace '\|$', '') -split '\|' | ForEach-Object { $_.Trim() }
  if ($cells.Count -lt 6) { continue }
  if ($cells[0] -eq 'id' -or $cells[0] -match '^-+$') { continue }
  $rows += [pscustomobject]@{ line = $i; id = $cells[0]; kind = $cells[1]; url = $cells[2]; fp = $cells[3]; checked = $cells[4]; purpose = $cells[5] }
}
if ($rows.Count -eq 0) { Write-Error 'no source rows found'; exit 2 }

# --- fingerprinting ------------------------------------------------------------
$headers = @{ 'User-Agent' = 'ai-agents-md-refresh'; 'Accept' = 'text/html,application/json,text/plain,*/*' }

function Get-GitHubFingerprint([string]$url) {
  if ($url -notmatch '^https://github\.com/([^/]+)/([^/]+)/blob/([^/]+)/(.+)$') { return $null }
  $owner, $repo, $branch, $file = $Matches[1], $Matches[2], $Matches[3], $Matches[4]
  $api = "https://api.github.com/repos/$owner/$repo/commits?path=$([uri]::EscapeDataString($file))&sha=$branch&per_page=1"
  $j = Invoke-RestMethod -Headers $headers -Uri $api -TimeoutSec 30
  if (-not $j -or -not $j[0].sha) { throw "no commits returned for $file" }
  return 'gh:' + $j[0].sha.Substring(0, 12)
}

function Get-PageFingerprint([string]$url) {
  $r = Invoke-WebRequest -Headers $headers -Uri $url -TimeoutSec 45 -MaximumRedirection 5
  $t = [string]$r.Content
  $t = [regex]::Replace($t, '(?is)<(script|style|noscript)\b.*?</\1>', ' ')
  $t = [regex]::Replace($t, '(?s)<!--.*?-->', ' ')
  $t = [regex]::Replace($t, '(?s)<[^>]+>', ' ')
  $t = [Net.WebUtility]::HtmlDecode($t)
  $t = [regex]::Replace($t, '\s+', ' ').Trim()
  $bytes = [Text.Encoding]::UTF8.GetBytes($t)
  $hash = [Security.Cryptography.SHA256]::Create().ComputeHash($bytes)
  return 'sha:' + (($hash | ForEach-Object { $_.ToString('x2') }) -join '').Substring(0, 12)
}

$results = @()
foreach ($row in $rows) {
  $status = ''; $new = ''
  if ($row.fp -match '^manual') {
    # The site blocks plain clients (403/429); the Refresh path reads it in a browser and updates the date by hand.
    $results += [pscustomobject]@{ row = $row; status = 'MANUAL'; new = $row.fp; err = $null }
    '{0,-9} {1,-24} {2,-18}    open in a browser; compare against the purpose column' -f 'MANUAL', $row.id, $row.fp
    continue
  }
  try {
    $new = Get-GitHubFingerprint $row.url
    if (-not $new) { $new = Get-PageFingerprint $row.url }
    if ($row.fp -eq '-' -or [string]::IsNullOrWhiteSpace($row.fp)) { $status = 'NEW' }
    elseif ($row.fp -eq $new) { $status = 'UNCHANGED' }
    else { $status = 'CHANGED' }
  } catch {
    $status = 'ERROR'; $new = $row.fp
    $err = $_.Exception.Message -replace '\s+', ' '
  }
  $results += [pscustomobject]@{ row = $row; status = $status; new = $new; err = $err }
  $err = $null
  '{0,-9} {1,-24} {2,-18} -> {3,-18} {4}' -f $status, $row.id, $row.fp, $new, ($(if ($status -eq 'ERROR') { $results[-1].err } else { '' }))
}

$counts = $results | Group-Object status | ForEach-Object { "$($_.Name)=$($_.Count)" }
"`nsummary: " + ($counts -join '  ') + "  (last-refresh $($lastRefresh.ToString('yyyy-MM-dd')), $days day(s) ago, gate $GateDays)"

# --- update ---------------------------------------------------------------------
if ($Update) {
  foreach ($res in $results) {
    if ($res.status -in @('ERROR', 'MANUAL')) { continue }
    $r = $res.row
    $cells = ($lines[$r.line].Trim() -replace '^\|', '' -replace '\|$', '') -split '\|' | ForEach-Object { $_.Trim() }
    $cells[3] = $res.new
    $cells[4] = $today
    $lines[$r.line] = '| ' + ($cells -join ' | ') + ' |'
  }
  $lines = $lines | ForEach-Object { if ($_ -match '^last-refresh:') { "last-refresh: $today" } else { $_ } }
  [IO.File]::WriteAllText($Path, ($lines -join "`n"), [Text.UTF8Encoding]::new($false))
  "sources.md updated: fingerprints and last-refresh = $today"
}
