$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskInput = Get-ChildItem -LiteralPath (Join-Path $taskRoot 'ban_da_sua') -Filter '*.docx' | Select-Object -First 1
$taskOutput = Join-Path $taskRoot 'review_revision/render/report.pdf'
[IO.Directory]::CreateDirectory((Split-Path $taskOutput)) | Out-Null
$taskDoc = [Runtime.InteropServices.Marshal]::BindToMoniker($taskInput.FullName)
try {
    $taskDoc.ExportAsFixedFormat($taskOutput, 17)
    Write-Output 'Rendered report to internal QA PDF'
} finally {
    $taskDoc.Close([ref]0)
}
