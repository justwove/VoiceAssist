Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
$build = "Nvdia"
$cmd="pyinstaller --onefile \\wsl.localhost\Debian\opt\VoiceAssist_$build\dash_app.py --distpath \\wsl.localhost\Debian\opt\VoiceAssist_$build\release/"
Write-Host "Running command: $cmd"
# Run the command
Invoke-Expression -Command $cmd
Write-Host "Release created at \\wsl.localhost\Debian\opt\VoiceAssist_$build\release"

$wsl_release = "bash -d Debian /opt/VoiceAssist_$build/create_release.sh"
echo $wsl_release