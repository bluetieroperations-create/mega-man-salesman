param([string]$c)
$o = powershell -Command $c 2>&1 | Out-String
$f = "C:\Users\maste\.openclaw\workspace\x.txt"
Start-Sleep -Milliseconds 500
[System.IO.File]::WriteAllText($f, $o, [System.Text.Encoding]::UTF8)
Write-Host $o