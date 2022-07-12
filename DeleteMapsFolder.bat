title Astral Maps Folder Deleter

@echo off

cls

echo Do you want to delete your WHOLE maps folder?

rd /s "%~dp0maps\"
echo Maps Folder Deleted.
pause > nul