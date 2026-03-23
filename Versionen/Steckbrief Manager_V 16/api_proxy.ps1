# API Reverse Proxy - leitet Anfragen an den lokalen Flask-Server weiter
# Wird von PowerShell ausgefuehrt (nicht von python.exe blockiert)
$port = 5001
$targetBase = "http://localhost:5000"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://+:$port/")

try {
    $listener.Start()
    Write-Host "API-Proxy laeuft auf Port $port -> $targetBase"
    Write-Host "Extern erreichbar unter http://$($env:COMPUTERNAME):$port/"
    Write-Host "Druecke Ctrl+C zum Beenden."

    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        # CORS-Header
        $response.Headers.Add("Access-Control-Allow-Origin", "*")
        $response.Headers.Add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        $response.Headers.Add("Access-Control-Allow-Headers", "Content-Type")

        if ($request.HttpMethod -eq "OPTIONS") {
            $response.StatusCode = 200
            $response.Close()
            continue
        }

        $targetUrl = "$targetBase$($request.RawUrl)"
        try {
            $webRequest = [System.Net.HttpWebRequest]::Create($targetUrl)
            $webRequest.Method = $request.HttpMethod
            $webRequest.ContentType = $request.ContentType
            $webRequest.Timeout = 30000

            if ($request.HasEntityBody) {
                $reader = New-Object System.IO.StreamReader($request.InputStream)
                $body = $reader.ReadToEnd()
                $reader.Close()
                $bytes = [System.Text.Encoding]::UTF8.GetBytes($body)
                $webRequest.ContentLength = $bytes.Length
                $reqStream = $webRequest.GetRequestStream()
                $reqStream.Write($bytes, 0, $bytes.Length)
                $reqStream.Close()
            }

            $webResponse = $webRequest.GetResponse()
            $respStream = $webResponse.GetResponseStream()
            $respReader = New-Object System.IO.StreamReader($respStream)
            $respBody = $respReader.ReadToEnd()
            $respReader.Close()

            $response.ContentType = $webResponse.ContentType
            $response.StatusCode = [int]$webResponse.StatusCode
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($respBody)
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
            $webResponse.Close()
        }
        catch {
            $errMsg = '{"error": "API nicht erreichbar"}'
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($errMsg)
            $response.StatusCode = 502
            $response.ContentType = "application/json"
            $response.ContentLength64 = $buffer.Length
            $response.OutputStream.Write($buffer, 0, $buffer.Length)
        }
        $response.Close()
    }
}
catch {
    Write-Host "Fehler: $_"
}
finally {
    $listener.Stop()
}
