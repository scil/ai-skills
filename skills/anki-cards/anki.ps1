# AnkiConnect helpers for the anki-cards skill. Dot-source this:  . .\anki.ps1
# Requires Anki open with the AnkiConnect add-on (http://localhost:8765).
#
# NOTE: all functions use descriptive Verb-Noun names on purpose — single-letter
# names (R/H/%/?) collide with built-in PowerShell aliases and silently swallow
# arguments.

$script:AnkiUrl = 'http://localhost:8765'

function Invoke-Anki {
  param([Parameter(Mandatory)][string]$Action, [hashtable]$Params = @{})
  $json  = @{ action = $Action; version = 6; params = $Params } | ConvertTo-Json -Depth 12
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)   # UTF-8 so Chinese survives
  Invoke-RestMethod -Uri $script:AnkiUrl -Method Post `
    -ContentType 'application/json; charset=utf-8' -Body $bytes -TimeoutSec 20
}

function Test-Anki {
  # Returns the AnkiConnect version if reachable; throws if Anki/add-on is down.
  (Invoke-Anki 'version').result
}

function New-AnkiDeck {
  param([Parameter(Mandatory)][string]$Deck)
  Invoke-Anki 'createDeck' @{ deck = $Deck } | Out-Null
}

function New-BasicNote {
  param(
    [Parameter(Mandatory)]$Deck, [Parameter(Mandatory)]$Front,
    [Parameter(Mandatory)]$Back, [string[]]$Tags = @(), $Model = '问答题'
  )
  @{ deckName = $Deck; modelName = $Model
     fields = @{ '正面' = $Front; '背面' = $Back }
     tags = $Tags; options = @{ allowDuplicate = $true } }
}

function New-RevNote {
  # Basic + reversed: generates both directions (2 cards). Good for 术语↔释义 / 对比.
  param([Parameter(Mandatory)]$Deck, [Parameter(Mandatory)]$Front,
        [Parameter(Mandatory)]$Back, [string[]]$Tags = @())
  New-BasicNote -Deck $Deck -Front $Front -Back $Back -Tags $Tags `
    -Model '问答题（同时生成翻转的卡片）'
}

function New-ClozeNote {
  # Text must contain at least one {{c1::...}} deletion.
  param([Parameter(Mandatory)]$Deck, [Parameter(Mandatory)]$Text,
        [string[]]$Tags = @(), $Model = '填空题')
  @{ deckName = $Deck; modelName = $Model
     fields = @{ '文字' = $Text; '背面额外' = '' }
     tags = $Tags; options = @{ allowDuplicate = $true } }
}

function Add-AnkiNotes {
  param([Parameter(Mandatory)][array]$Notes)
  $res = Invoke-Anki 'addNotes' @{ notes = $Notes }
  $ids = $res.result
  [pscustomobject]@{
    Requested = $Notes.Count
    Created   = ($ids | Where-Object { $_ -ne $null }).Count
    Failed    = ($ids | Where-Object { $_ -eq $null }).Count
    Error     = $res.error
  }
}

function Get-AnkiDeckStats {
  param([Parameter(Mandatory)][string]$Deck)
  [pscustomobject]@{
    Deck  = $Deck
    Notes = (Invoke-Anki 'findNotes' @{ query = "deck:$Deck" }).result.Count
    Cards = (Invoke-Anki 'findCards' @{ query = "deck:$Deck" }).result.Count
  }
}
