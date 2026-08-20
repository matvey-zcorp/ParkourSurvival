@echo off
echo Compiling...
nuitka --onefile --windows-console-mode=disable --output-dir=build\app --remove-output --windows-icon-from-ico=src\app\icon.ico --standalone src\app\main.py
echo Compiled!
Your result in: build\app\main.exe.
pause