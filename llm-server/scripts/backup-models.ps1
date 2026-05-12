<#
.SYNOPSIS
    LLM Server - Backup & Restore model volume
.DESCRIPTION
    Backup/restore Ollama models volume to avoid re-downloading.
.EXAMPLE
    .\scripts\backup-models.ps1 backup
    .\scripts\backup-models.ps1 restore
#>

param(
    [Parameter(Position=0)]
    [ValidateSet("backup", "restore")]
    [string]$Action = "backup"
)

$VOLUME_NAME = "llm-server_ollama-models"
$BACKUP_DIR = Join-Path $PSScriptRoot "..\backups"
$BACKUP_FILE = Join-Path $BACKUP_DIR "ollama-models-$(Get-Date -Format 'yyyyMMdd-HHmmss').tar.gz"

if (-not (Test-Path $BACKUP_DIR)) {
    New-Item -ItemType Directory -Path $BACKUP_DIR -Force | Out-Null
}

switch ($Action) {
    "backup" {
        Write-Host "[BACKUP] Backing up LLM models..." -ForegroundColor Cyan
        Write-Host "   Volume: $VOLUME_NAME" -ForegroundColor White
        
        docker run --rm `
            -v "${VOLUME_NAME}:/data:ro" `
            -v "${BACKUP_DIR}:/backup" `
            alpine tar czf "/backup/$(Split-Path $BACKUP_FILE -Leaf)" -C /data .
        
        if ($LASTEXITCODE -eq 0) {
            $size = [math]::Round((Get-Item $BACKUP_FILE).Length / 1MB, 1)
            Write-Host "[OK] Backup saved: $BACKUP_FILE (${size}MB)" -ForegroundColor Green
        } else {
            Write-Host "[FAIL] Backup failed" -ForegroundColor Red
        }
    }
    "restore" {
        $latest = Get-ChildItem $BACKUP_DIR -Filter "ollama-models-*.tar.gz" | 
                  Sort-Object LastWriteTime -Descending | 
                  Select-Object -First 1
        
        if (-not $latest) {
            Write-Host "[FAIL] No backup found in $BACKUP_DIR" -ForegroundColor Red
            exit 1
        }
        
        Write-Host "[RESTORE] Restoring from: $($latest.Name)" -ForegroundColor Cyan
        Write-Host "[WARN] Container will be stopped during restore." -ForegroundColor Yellow
        $confirm = Read-Host "Continue? (y/n)"
        if ($confirm -ne "y") { exit 0 }
        
        docker compose -f (Join-Path $PSScriptRoot "..\docker-compose.yml") stop ollama
        
        docker run --rm `
            -v "${VOLUME_NAME}:/data" `
            -v "${BACKUP_DIR}:/backup:ro" `
            alpine sh -c "rm -rf /data/* && tar xzf /backup/$($latest.Name) -C /data"
        
        docker compose -f (Join-Path $PSScriptRoot "..\docker-compose.yml") start ollama
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "[OK] Restore completed. Container restarted." -ForegroundColor Green
        } else {
            Write-Host "[FAIL] Restore failed" -ForegroundColor Red
        }
    }
}
