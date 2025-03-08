
@echo off
setlocal enabledelayedexpansion

REM Exit the script if there is some error (Windows batch equivalent)
REM Define Some Variables for Re-Use
set TARGET_SCRIPT=ml-version.py
set VENV_DIR=env

REM Colors for Windows cmd
set GREEN=^[92m
set YELLOW=^[93m
set BLUE=^[94m
set RED=^[91m
set NC=^[0m

REM Ask For python or python3
set PYTHON_CMD=python
echo %YELLOW%Would you like to use python3? (y/n)%NC%
set /p response=
if /i "%response%"=="y" (
    set PYTHON_CMD=python3
)

echo %BLUE%Starting setup with %PYTHON_CMD%...%NC%
echo %YELLOW%Creating virtual environment...%NC%
%PYTHON_CMD% -m venv "%VENV_DIR%"

echo %YELLOW%Activating virtual environment...%NC%
call "%VENV_DIR%\Scripts\activate.bat"

echo %YELLOW%Upgrading pip...%NC%
pip install --upgrade pip

echo %YELLOW%Installing dependencies...%NC%
pip install -r requirements.txt

echo %YELLOW%Running the script: %TARGET_SCRIPT%%NC%
%PYTHON_CMD% "%TARGET_SCRIPT%"

echo %YELLOW%Deactivating virtual environment...%NC%
call deactivate

echo %YELLOW%Cleaning...%NC%
rmdir /s /q "%VENV_DIR%"

echo %GREEN%Demo complete%NC%

