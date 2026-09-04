# Splitzy — local dev server (PWA needs http://, not file://)
# Run:  powershell -ExecutionPolicy Bypass -File .\serve.ps1
# Then open http://localhost:8091/  (Ctrl+C to stop)

$http = [System.Net.HttpListener]::new()
$http.Prefixes.Add("http://localhost:8091/")
$http.Start()
Write-Host "Splitzy running at http://localhost:8091/ - Press Ctrl+C to stop"

$mime = @{
    '.html' = 'text/html'
    '.js'   = 'application/javascript'
    '.json' = 'application/json'
    '.svg'  = 'image/svg+xml'
    '.png'  = 'image/png'
    '.css'  = 'text/css'
}

while ($http.IsListening) {
    $ctx = $http.GetContext()
    $path = $ctx.Request.Url.LocalPath
    if ($path -eq '/') { $path = '/index.html' }
    $file = Join-Path $PSScriptRoot $path.TrimStart('/')
    if (Test-Path $file -PathType Leaf) {
        $ext = [System.IO.Path]::GetExtension($file)
        $ctx.Response.ContentType = if ($mime[$ext]) { $mime[$ext] } else { 'application/octet-stream' }
        $bytes = [System.IO.File]::ReadAllBytes($file)
        $ctx.Response.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
        $ctx.Response.StatusCode = 404
    }
    $ctx.Response.Close()
}
