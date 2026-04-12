@param([string]$cmd)
$result = Invoke-Expression $cmd 2>&1
$result | Out-File "$env:USERPROFILE\.openclaw\workspace\out.txt" -Encoding UTF8
Get-Content "$env:USERPROFILE\.openclaw\workspace\out.txt"
