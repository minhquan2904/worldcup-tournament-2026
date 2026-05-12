<#
.SYNOPSIS
    LLM Server - Health Check
.DESCRIPTION
    Kiem tra toan dien trang thai LLM Server: container, API, GPU, models.
.EXAMPLE
    .\scripts\health-check.ps1
#>

$LLM_PORT = if ($env:LLM_PORT) { $env:LLM_PORT } else { "11434" }
$BASE_URL = "http://localhost:$LLM_PORT"
$allOk = $true

Write-Host ""
Write-Host "[HEALTH CHECK] LLM Server Health Check" -ForegroundColor Cyan
Write-Host ("=" * 50)

# 1. Docker container
Write-Host ""
Write-Host "[1/5] Docker container..." -NoNewline
$container = docker ps --filter "name=llm-server" --format "{{.Status}}" 2>$null
if ($container) {
    Write-Host " [OK] Running ($container)" -ForegroundColor Green
} else {
    Write-Host " [FAIL] Not running" -ForegroundColor Red
    $allOk = $false
    Write-Host "     -> docker compose up -d" -ForegroundColor Yellow
}

# 2. API accessible
Write-Host "[2/5] API endpoint..." -NoNewline
try {
    $null = Invoke-RestMethod -Uri "$BASE_URL/api/tags" -TimeoutSec 5
    Write-Host " [OK] Accessible ($BASE_URL)" -ForegroundColor Green
} catch {
    Write-Host " [FAIL] Unreachable" -ForegroundColor Red
    $allOk = $false
}

# 3. GPU status
Write-Host "[3/5] GPU..." -NoNewline
try {
    $gpuInfo = docker exec llm-server sh -c "nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv,noheader,nounits" 2>$null
    if ($gpuInfo) {
        $parts = $gpuInfo -split ","
        $name = $parts[0].Trim()
        $used = $parts[1].Trim()
        $total = $parts[2].Trim()
        Write-Host " [OK] $name - VRAM: ${used}/${total} MB" -ForegroundColor Green
    } else {
        Write-Host " [WARN] nvidia-smi not available (CPU mode?)" -ForegroundColor Yellow
    }
} catch {
    Write-Host " [WARN] Cannot check GPU" -ForegroundColor Yellow
}

# 4. Models loaded
Write-Host "[4/5] Models installed..." -NoNewline
try {
    $result = Invoke-RestMethod -Uri "$BASE_URL/api/tags" -TimeoutSec 5
    $count = $result.models.Count
    if ($count -gt 0) {
        Write-Host " [OK] $count model(s)" -ForegroundColor Green
        foreach ($m in $result.models) {
            $sizeGB = [math]::Round($m.size / 1GB, 2)
            Write-Host "     - $($m.name) (${sizeGB}GB)" -ForegroundColor White
        }
    } else {
        Write-Host " [WARN] No models installed" -ForegroundColor Yellow
        $allOk = $false
    }
} catch {
    Write-Host " [FAIL] Cannot check" -ForegroundColor Red
}

# 5. Inference test
Write-Host "[5/5] Inference test..." -NoNewline
try {
    $body = @{
        model = ($result.models[0].name)
        messages = @(@{role="user"; content="Reply with only: OK"})
        stream = $false
        options = @{ num_predict = 5 }
    } | ConvertTo-Json -Depth 3
    $resp = Invoke-RestMethod -Uri "$BASE_URL/api/chat" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 30
    Write-Host " [OK] Response received" -ForegroundColor Green
} catch {
    Write-Host " [FAIL] Inference failed" -ForegroundColor Red
    $allOk = $false
}

# Summary
Write-Host ""
Write-Host ("=" * 50)
if ($allOk) {
    Write-Host "[OK] LLM Server is healthy!" -ForegroundColor Green
} else {
    Write-Host "[WARN] Some checks failed. See details above." -ForegroundColor Yellow
}
Write-Host ""
