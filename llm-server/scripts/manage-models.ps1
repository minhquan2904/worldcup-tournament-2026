<# 
.SYNOPSIS
    LLM Server - Model Management
.DESCRIPTION
    Manage models on Ollama server: list, pull, remove, info.
.EXAMPLE
    .\scripts\manage-models.ps1 list
    .\scripts\manage-models.ps1 pull qwen2.5-coder:7b
    .\scripts\manage-models.ps1 remove qwen2.5-coder:3b
    .\scripts\manage-models.ps1 info qwen2.5-coder:3b
#>

param(
    [Parameter(Position=0)]
    [ValidateSet("list", "pull", "remove", "info", "running")]
    [string]$Action = "list",

    [Parameter(Position=1)]
    [string]$Model = ""
)

$CONTAINER = "llm-server"
$port = if ($env:LLM_PORT) { $env:LLM_PORT } else { '11434' }
$BASE_URL = "http://localhost:$port"

function Test-OllamaRunning {
    try {
        $null = Invoke-RestMethod -Uri "$BASE_URL/api/tags" -TimeoutSec 5
        return $true
    } catch {
        Write-Host "[ERROR] LLM Server is not running. Start with:" -ForegroundColor Red
        Write-Host "   docker compose up -d" -ForegroundColor Yellow
        return $false
    }
}

switch ($Action) {
    "list" {
        if (-not (Test-OllamaRunning)) { exit 1 }
        $result = Invoke-RestMethod -Uri "$BASE_URL/api/tags"
        if ($result.models.Count -eq 0) {
            Write-Host "[WARN] No models installed." -ForegroundColor Yellow
        } else {
            Write-Host "[INFO] Installed models ($($result.models.Count)):" -ForegroundColor Cyan
            foreach ($m in $result.models) {
                $sizeGB = [math]::Round($m.size / 1GB, 2)
                Write-Host "  - $($m.name) -- ${sizeGB}GB -- $($m.details.family)" -ForegroundColor White
            }
        }
    }
    "pull" {
        if (-not $Model) { Write-Host "[ERROR] Model name required. E.g.: .\manage-models.ps1 pull qwen2.5-coder:7b" -ForegroundColor Red; exit 1 }
        if (-not (Test-OllamaRunning)) { exit 1 }
        Write-Host "[PULL] Pulling $Model..." -ForegroundColor Cyan
        docker exec $CONTAINER ollama pull $Model
    }
    "remove" {
        if (-not $Model) { Write-Host "[ERROR] Model name required." -ForegroundColor Red; exit 1 }
        if (-not (Test-OllamaRunning)) { exit 1 }
        Write-Host "[DEL] Removing $Model..." -ForegroundColor Yellow
        docker exec $CONTAINER ollama rm $Model
    }
    "info" {
        if (-not $Model) { Write-Host "[ERROR] Model name required." -ForegroundColor Red; exit 1 }
        if (-not (Test-OllamaRunning)) { exit 1 }
        docker exec $CONTAINER ollama show $Model
    }
    "running" {
        if (-not (Test-OllamaRunning)) { exit 1 }
        Write-Host "[INFO] Models currently loaded in VRAM:" -ForegroundColor Cyan
        docker exec $CONTAINER ollama ps
    }
}
