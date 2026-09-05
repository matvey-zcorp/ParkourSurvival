REQUIREMENTS = requirements.txt
UPGRADER = upgrade.py
SCRIPT = main.py
SRC_DLL = localization.c
DLL = localization.dll
SHELL = cmd.exe
SRC_DIR = src
OUT_DIR = build
APP_DIR = app
SETUP_DIR = setup
VENV_DIR = venv
TEMP_DIR = temp

.PHONY: all createVenv install run compile compileDll
.SILENT:

all: createVenv install run compile compileDll

createVenv:
	echo Creating venv...
	python -m venv $(VENV_DIR)
	echo Complete!

install:
	echo Activating venv...
	$(VENV_DIR)/Scripts/activate.bat
	echo Activated!
	echo Installing dependencies...
	pip install -r $(REQUIREMENTS)
	echo Installed!

compileDll:
	echo Compiling...
	gcc -shared -o $(SRC_DIR)/$(APP_DIR)/$(DLL) $(SRC_DIR)/$(APP_DIR)/$(SRC_DLL)
	echo Compiled!

run:
	echo Running $(SCRIPT)...
	$(VENV_DIR)/Scripts/activate.bat
	cd $(SRC_DIR)/$(APP_DIR) & python $(SCRIPT)

compile:
	echo Compiling...
	nuitka --onefile --windows-console-mode=disable --output-dir=$(OUT_DIR)\$(APP_DIR) --remove-output --windows-icon-from-ico=$(SRC_DIR)/$(APP_DIR)/icon.ico --standalone $(SRC_DIR)/$(APP_DIR)/$(SCRIPT)
	gcc -shared -o $(OUT_DIR)/$(APP_DIR)/$(DLL) $(SRC_DIR)/$(APP_DIR)/$(SRC_DLL)
	copy $(SRC_DIR)/$(APP_DIR)/icon.ico $(OUT_DIR)/$(APP_DIR)/icon.ico
	xcopy $(SRC_DIR)/$(APP_DIR)/resources $(OUT_DIR)/$(APP_DIR)/resources /E /I
	rename $(OUT_DIR)/$(APP_DIR)/main.exe $(OUT_DIR)/$(APP_DIR)/parkoursurvival.exe
	echo Compiled!
	echo Your result in: $(OUT_DIR)/$(APP_DIR)/parkoursurvival.exe.