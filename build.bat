@echo off
echo Compiling...
nuitka --onefile --windows-console-mode=disable --output-dir=build\app --remove-output --windows-icon-from-ico=src\app\icon.ico --jobs=2 --standalone src\app\main.py
copy src\app\icon.ico build\app\icon.ico
xcopy src\app\resources build\app\resources /E /I
rename build\app\main.exe build\app\parkoursurvival.exe
echo Compiled!
echo Your result in: build\app\parkoursurvival.exe.