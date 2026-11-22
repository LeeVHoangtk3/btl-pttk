$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))
$taskSource = [IO.Path]::GetFullPath((Join-Path $taskRoot 'code_pttk/docs/doi_chieu_datn24'))
$taskRenderRoot = [IO.Path]::GetFullPath((Join-Path $taskRoot 'build/report_review/render'))
[IO.Directory]::CreateDirectory($taskRenderRoot) | Out-Null

# Use a dedicated, hidden Word instance. Never attach to or quit user sessions.
$taskWord = New-Object -ComObject Word.Application
$taskWord.Visible = $false
$taskWord.DisplayAlerts = 0
try {
    $taskFiles = @(Get-ChildItem -LiteralPath $taskSource -Filter '*.docx' | Where-Object { $_.Name -notlike '~$*' })
    for ($taskIndex = 0; $taskIndex -lt $taskFiles.Count; $taskIndex++) {
        $taskFile = $taskFiles[$taskIndex]
        $taskDocument = $null
        try {
            $taskDocument = $taskWord.Documents.Open($taskFile.FullName, $false, $false, $false)
            Write-Output ('Opened document ' + $taskIndex)
            $taskDocument.UpdateStylesOnOpen = $false
            $taskDocument.Fields.Update() | Out-Null
            $taskTocCount = $taskDocument.TablesOfContents.Count
            for ($taskTocIndex = 1; $taskTocIndex -le $taskTocCount; $taskTocIndex++) {
                $taskDocument.TablesOfContents.Item($taskTocIndex).Update()
            }
            # Word expands the TOC field into a trailing empty field paragraph.
            # Keep it small so it does not create a page containing only a footer.
            for ($taskTocIndex = 1; $taskTocIndex -le $taskTocCount; $taskTocIndex++) {
                $taskParagraph = $taskDocument.TablesOfContents.Item($taskTocIndex).Range.Paragraphs.Last
                if ($taskParagraph.Range.Text -eq "`r" -and $taskParagraph.Range.InlineShapes.Count -eq 0) {
                    $taskParagraph.Range.Font.Size = 1
                    $taskParagraph.Format.SpaceAfter = 0
                    $taskParagraph.Format.SpaceBefore = 0
                    $taskParagraph.Format.LineSpacingRule = 4
                    $taskParagraph.Format.LineSpacing = 1
                }
            }
            $taskDocument.Repaginate()
            $taskDocument.Fields.Update() | Out-Null
            for ($taskTocIndex = 1; $taskTocIndex -le $taskTocCount; $taskTocIndex++) {
                $taskDocument.TablesOfContents.Item($taskTocIndex).UpdatePageNumbers()
            }
            $taskSavedCopy = [IO.Path]::GetFullPath((Join-Path $taskRenderRoot ('document-' + $taskIndex + '.docx')))
            $taskDocument.SaveAs2($taskSavedCopy, 12)
            Write-Output ('Updated document ' + $taskIndex)
            $taskPdf = [IO.Path]::GetFullPath((Join-Path $taskRenderRoot ('document-' + $taskIndex + '.pdf')))
            $taskDocument.ExportAsFixedFormat($taskPdf, 17)
            Write-Output ($taskFile.Name + ' | pages=' + $taskDocument.ComputeStatistics(2))
        } finally {
            if ($null -ne $taskDocument) {
                $taskDocument.Close(0)
                [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskDocument)
            }
        }
    }
} finally {
    $taskWord.Quit()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($taskWord)
}
# Write the cached field results back only after Word releases its file locks.
for ($taskIndex = 0; $taskIndex -lt $taskFiles.Count; $taskIndex++) {
    $taskSavedCopy = [IO.Path]::GetFullPath((Join-Path $taskRenderRoot ('document-' + $taskIndex + '.docx')))
    Copy-Item -LiteralPath $taskSavedCopy -Destination $taskFiles[$taskIndex].FullName -Force
}
