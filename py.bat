@echo off
setlocal enabledelayedexpansion
:menu
echo.
echo Virtual Environment Manager
echo --------------------------
echo 1. Create and setup virtual environment
echo 2. Delete virtual environment
echo 3. Run Python file in virtual environment
echo 4. Exit
echo.
set /p choice=Enter your choice (1-4): 

if "%choice%"=="1" goto create
if "%choice%"=="2" goto delete
if "%choice%"=="3" goto runpy
if "%choice%"=="4" goto end
echo Invalid choice. Please try again.
goto menu

:create
echo.
echo Creating Python virtual environment...
python -m venv myenv

echo Activating virtual environment...
call myenv\Scripts\activate.bat

echo Installing requirements...
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pause

echo Deactivating virtual environment...
deactivate

echo.
echo Process completed.
goto menu

:delete
echo.
if exist myenv (
    echo Deleting virtual environment...
    rmdir /s /q myenv
    echo Virtual environment deleted.
) else (
    echo No virtual environment found.
)
goto menu

:runpy
echo.
echo Available Python files:
set count=0
for %%f in (*.py) do (
    set /a count+=1
    echo !count!. %%f
)

if !count!==0 (
    echo No Python files found in the current directory.
    pause
    goto menu
)

echo.
set /p choice=Enter the number of the file to run: 

set filenum=0
set filename=
for %%f in (*.py) do (
    set /a filenum+=1
    if !filenum!==!choice! (
        set filename=%%f
    )
)

if "!filename!"=="" (
    echo Invalid selection.
    pause
    goto menu
)

if not exist myenv (
    echo No virtual environment found. Please create one first.
    pause
    goto menu
)

echo Running !filename! in virtual environment...
call myenv\Scripts\activate.bat
streamlit run !filename!
deactivate
echo.
echo Execution completed.
pause
goto menu

:end
echo Exiting...