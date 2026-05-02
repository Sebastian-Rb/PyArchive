if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python no está instalado. Instálalo desde https://python.org"
    exit
}

$tmp = New-TemporaryFile
$url = "https://raw.githubusercontent.com/Sebastian-Rb/PyArchive/main/GestorArchivos.py"

Write-Host "Descargando script..."
Invoke-WebRequest $url -OutFile $tmp

Write-Host "Ejecutando..."
python $tmp
