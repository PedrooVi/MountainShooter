$ErrorActionPreference = "Stop"

if ($env:OS -ne "Windows_NT") {
    throw "Este script deve ser executado no Windows."
}

$root = $PSScriptRoot
$sourceAssets = Join-Path $root "asset"
$buildRoot = Join-Path $root "build"
$staging = Join-Path $buildRoot "release\ZombieRunner"
$workPath = Join-Path $buildRoot "pyinstaller-work"
$specPath = Join-Path $buildRoot "pyinstaller-spec"
$distRoot = Join-Path $root "dist"
$package = Join-Path $distRoot "ZombieRunner"
$zipPath = Join-Path $distRoot "ZombieRunner.zip"

if (-not (Test-Path -LiteralPath $sourceAssets -PathType Container)) {
    throw "Pasta de assets ausente: $sourceAssets"
}
if ((Test-Path -LiteralPath $staging) -or (Test-Path -LiteralPath $package) -or (Test-Path -LiteralPath $zipPath)) {
    throw "A saida ZombieRunner ja existe. Mova os artefatos anteriores antes de reconstruir."
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    throw "uv nao foi encontrado no PATH. Instale uv antes de compilar."
}

New-Item -ItemType Directory -Force -Path $staging, $workPath, $specPath | Out-Null

$pyInstallerArgs = @(
    "run", "--project", $root, "--group", "build",
    "python", "-m", "PyInstaller",
    "--clean", "--noconfirm", "--onefile", "--windowed",
    "--name", "ZombieRunner",
    "--distpath", $staging,
    "--workpath", $workPath,
    "--specpath", $specPath,
    "--paths", $root,
    (Join-Path $root "main.py")
)
& uv @pyInstallerArgs
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller falhou com codigo $LASTEXITCODE."
}

$packageAssets = Join-Path $staging "assets"
$backgroundSource = Join-Path $sourceAssets "Backgrounds"
$characterSource = Join-Path $sourceAssets "Personagens"
$zombieSource = Join-Path $sourceAssets "Zombies"
$backgroundTarget = Join-Path $packageAssets "Backgrounds"
$characterTarget = Join-Path $packageAssets "Personagens"
$zombieTarget = Join-Path $packageAssets "Zombies"

$cityFolders = Get-ChildItem -LiteralPath $backgroundSource -Directory |
    Where-Object { $_.Name -match "^city \d+$" }
if ($cityFolders.Count -ne 8) {
    throw "Esperados 8 cenarios urbanos, encontrados $($cityFolders.Count)."
}
foreach ($city in $cityFolders) {
    $cityTarget = Join-Path $backgroundTarget $city.Name
    New-Item -ItemType Directory -Force -Path $cityTarget | Out-Null
    Get-ChildItem -LiteralPath $city.FullName -File -Filter "*.png" |
        Copy-Item -Destination $cityTarget
}
Copy-Item -LiteralPath (Join-Path $backgroundSource "License.txt") -Destination $backgroundTarget

foreach ($character in @("Shinobi", "Samurai")) {
    $characterTargetFolder = Join-Path $characterTarget $character
    New-Item -ItemType Directory -Force -Path $characterTargetFolder | Out-Null
    foreach ($animation in @("Run.png", "Jump.png")) {
        $animationPath = Join-Path (Join-Path $characterSource $character) $animation
        if (-not (Test-Path -LiteralPath $animationPath -PathType Leaf)) {
            throw "Animacao de personagem ausente: $animationPath"
        }
        Copy-Item -LiteralPath $animationPath -Destination $characterTargetFolder
    }
}
Copy-Item -LiteralPath (Join-Path $characterSource "Licens.txt") -Destination $characterTarget

$zombieFolders = Get-ChildItem -LiteralPath (Join-Path $zombieSource "PNG") -Directory
foreach ($zombie in $zombieFolders) {
    $animationSource = Join-Path $zombie.FullName "animation"
    $animationTarget = Join-Path (Join-Path (Join-Path $zombieTarget "PNG") $zombie.Name) "animation"
    New-Item -ItemType Directory -Force -Path $animationTarget | Out-Null
    $frames = Get-ChildItem -LiteralPath $animationSource -File |
        Where-Object { $_.BaseName -match "^(Run|Jump)\d+$" }
    if (-not ($frames | Where-Object { $_.BaseName -match "^Run\d+$" }) -or
        -not ($frames | Where-Object { $_.BaseName -match "^Jump\d+$" })) {
        throw "Frames de corrida ou pulo ausentes para $($zombie.Name)."
    }
    $frames | Copy-Item -Destination $animationTarget
}
Copy-Item -LiteralPath (Join-Path $zombieSource "License.txt") -Destination $zombieTarget
Copy-Item -LiteralPath (Join-Path $root "README.md") -Destination $staging

New-Item -ItemType Directory -Force -Path $distRoot | Out-Null
Move-Item -LiteralPath $staging -Destination $package
Compress-Archive -Path $package -DestinationPath $zipPath -CompressionLevel Optimal

Write-Output "Executavel: $package\ZombieRunner.exe"
Write-Output "Distribuicao: $package"
Write-Output "ZIP: $zipPath"