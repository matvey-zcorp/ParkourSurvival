@echo off
echo Compiling...
nuitka --onefile --windows-console-mode=disable --output-dir=..\build\app --remove-output --standalone main.py
echo Compiled!
Your result in: build\app\main.exe.
pause