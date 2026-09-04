# Splitzy — sample data generator (WealthOrah-style)
# Writes sample-data.json with a set of bills, a group of 5 people, tip and currency.
# Run:  powershell -ExecutionPolicy Bypass -File .\generate-data.ps1
# Then load it into Splitzy (drag the file onto the app, or press Ctrl+Shift+L, or open index.html?sample=1).

$today = Get-Date
function DMY([int]$daysAgo) { return ($today.AddDays(-$daysAgo)).ToString('dd/MM/yyyy') }

# 6 sample bills (INR). Description | Amount | days ago
$bills = @(
    @{ desc = 'Dinner at Barbeque Nation'; amount = 4850.00; date = (DMY 0) },
    @{ desc = 'Cab rides (Uber)';           amount = 620.50;  date = (DMY 0) },
    @{ desc = 'Movie tickets (PVR)';        amount = 1800.00; date = (DMY 1) },
    @{ desc = 'Snacks & drinks';            amount = 940.00;  date = (DMY 1) },
    @{ desc = 'Bowling';                    amount = 1500.00; date = (DMY 2) },
    @{ desc = 'Coffee & desserts';          amount = 730.75;  date = (DMY 2) }
)

$sb = [System.Text.StringBuilder]::new()
[void]$sb.Append('{"version":"1.3.1","currency":"inr","people":5,"tip":10,"roundUp":false,"bills":[')

$first = $true
foreach ($b in $bills) {
    if (-not $first) { [void]$sb.Append(',') }
    $descEsc = ($b.desc -replace '\\','\\\\') -replace '"','\"'
    [void]$sb.Append(('{{"desc":"{0}","amount":{1},"date":"{2}"}}' -f $descEsc, $b.amount, $b.date))
    $first = $false
}

[void]$sb.Append(']}')

$outPath = Join-Path $PSScriptRoot 'sample-data.json'
[System.IO.File]::WriteAllText($outPath, $sb.ToString())
Write-Output "Done! Wrote $outPath ($($bills.Count) bills, group of 5, INR)."
