$ErrorActionPreference = "Stop"

$path = Join-Path $PSScriptRoot "..\\app\\main.py"
$path = (Resolve-Path $path).Path

$t = Get-Content -Path $path -Raw -Encoding UTF8

if ($t -notmatch "from app\.modules\.ai import router as ai_router") {
  $t = $t -replace "from app\.modules\.system import router as system_router(\r?\n)", "from app.modules.system import router as system_router`r`nfrom app.modules.ai import router as ai_router`r`n"
}

if ($t -notmatch "app\.include_router\(ai_router,\s*prefix=""/api/ai""") {
  $t = $t -replace "app\.include_router\(system_router, prefix=""/api/system"", tags=\[""系统模块""\]\)(\r?\n)", "app.include_router(system_router, prefix=""/api/system"", tags=[""系统模块""])`r`napp.include_router(ai_router, prefix=""/api/ai"", tags=[""AI助手""])`r`n"
}

Set-Content -Path $path -Value $t -Encoding UTF8
Write-Output "patched: $path"

