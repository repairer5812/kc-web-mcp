# Windows PowerShell 5.1+ / PowerShell 7. Docker Desktop must be running.
[CmdletBinding()]
param(
    [ValidateSet('start','stop','status','connection','token','verify')]
    [string]$Action = 'start'
)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    throw 'Install Docker Desktop, start its Linux container engine, then run this command again.'
}
function Invoke-Compose {
    param([string[]]$ComposeArguments)
    & docker compose @ComposeArguments
    if ($LASTEXITCODE -ne 0) { throw "Docker Compose failed (exit $LASTEXITCODE)." }
}
Invoke-Compose -ComposeArguments @('version')
& docker info --format '{{.OSType}}' | ForEach-Object {
    if ($_ -ne 'linux') { throw 'Switch Docker Desktop to Linux containers.' }
}
if ($LASTEXITCODE -ne 0) { throw 'Docker is not ready. Start Docker Desktop first.' }
switch ($Action) {
    'start' {
        Invoke-Compose -ComposeArguments @('up','-d','--build','--wait','--wait-timeout','180')
        Write-Host 'Runtime is healthy. Verify the public connection, then read the URL:'
        Write-Host '  .\scripts\pc.ps1 connection'
        Write-Host '  .\scripts\pc.ps1 token  # private terminal only'
        Write-Host 'Keep this PC awake while ChatGPT is using it.'
    }
    'verify' { Invoke-Compose -ComposeArguments @('exec','-T','runtime','python3','/opt/kc-mcp/scripts/check_live.py') }
    'stop' { Invoke-Compose -ComposeArguments @('stop') }
    'status' { Invoke-Compose -ComposeArguments @('ps') }
    'connection' { Invoke-Compose -ComposeArguments @('exec','-T','runtime','cat','/state/connection-url.txt') }
    'token' {
        Write-Host 'Private owner token: enter only on your service OAuth page. Never paste into chat or logs.'
        Invoke-Compose -ComposeArguments @('exec','-T','runtime','cat','/state/oauth-owner.token')
    }
}