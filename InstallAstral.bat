echo off
cls
title Astral Installer V1.01

IF EXIST "Astral.py" (
	echo Astral is now being updated...

	powershell -Command "Invoke-WebRequest https://github.com/RenderingByte/Astral/archive/refs/heads/dist.zip -Outfile Astral.zip"

	powershell -Command "Expand-Archive -Force Astral.zip"

	move "%~dp0Astral\Astral-dist\*.*" "%~dp0"
	move "%~dp0Astral\Astral-dist\fonts" "%~dp0"
	move "%~dp0Astral\Astral-dist\images" "%~dp0"
	move "%~dp0Astral\Astral-dist\skins" "%~dp0"
	@RD /S /Q "%~dp0Astral\"
	del Astral.zip

	cls
	
	start Astral.bat

	exit
)

echo Astral will be installed to this directory.
echo If you wish to continue press any key.
echo If you do not want to install Astral here, you may close the window.

pause>nul

cls

echo Downloading Python Installer...
powershell -Command "Invoke-WebRequest https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe -Outfile Install-Python.exe"
cls
echo Downloading Node.js Installer...
powershell -Command "Invoke-WebRequest https://nodejs.org/dist/v16.15.1/node-v16.15.1-x64.msi -Outfile Install-Node.msi"

cls

echo [Installing Python]

start Install-Python.exe

echo:

echo Press any key once Python is Installed
pause>nul

echo [Installing Node.JS]

start Install-Node.msi

echo:

echo Press any key once Node is Installed
pause>nul

cls

echo [Installing Python Dependencies]
echo Installing Pygame...
pip install pygame
echo:
echo Installing PygameGui...
pip install pygame-gui
echo:
echo Installing Pypresence...
pip install pypresence

cls

echo All Dependencies Installed!

echo:

echo Downloading Astral...

powershell -Command "Invoke-WebRequest https://github.com/RenderingByte/Astral/archive/refs/heads/dist.zip -Outfile Astral.zip"

echo:

echo Download Completed!

echo:

echo Unzipping Archive...

powershell -Command "Expand-Archive -Force Astral.zip"

move "%~dp0Astral\Astral-dist\*.*" "%~dp0"
move "%~dp0Astral\Astral-dist\fonts" "%~dp0"
move "%~dp0Astral\Astral-dist\images" "%~dp0"
move "%~dp0Astral\Astral-dist\skins" "%~dp0"
@RD /S /Q "%~dp0Astral\"
del Astral.zip
del Install-Python.exe
del Install-Node.msi

echo:

echo Extracted.
cls

start Astral.bat

pause