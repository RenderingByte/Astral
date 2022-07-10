@echo off
title RhythmGame Parser
echo All your osu! mania maps are being parsed.
echo Please be patient as this process can take time depending on how many maps you have.
echo Currently, maps that have already been parsed will not be reparsed.
echo > nul
echo If you just installed Astral, you can either let this finish or,
echo just let it run for a bit and then close it.
echo Afterwards, you must restart your PC.
echo Then you can finally play Astral by opening Astral.bat!
echo ------------------------------------------------------------------------------------
node parser.js
pause