@echo off
echo Compiling...
nuitka --onefile --windows-console-mode=disable --output-dir=build\app --remove-output --windows-icon-from-ico=src\app\icon.ico --jobs=2 --standalone src\app\main.py
echo Compiled!
echo Your result in: build\app\main.exe.
pause