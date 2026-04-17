@echo off
REM DiagnoReport Test Runner Script (Windows)
REM Quick start for running the test suite

echo ======================================================
echo DiagnoReport - Test Suite Execution
echo ======================================================
echo.

REM Check if GEMINI_API_KEY is set
if "%GEMINI_API_KEY%"=="" (
    echo Error: GEMINI_API_KEY environment variable not set
    echo.
    echo Please set your Gemini API key:
    echo   set GEMINI_API_KEY=your-api-key-here
    echo.
    echo Get your free API key from:
    echo   https://aistudio.google.com/app/apikeys
    exit /b 1
)

echo GEMINI_API_KEY is set
echo.

REM Check if running from correct directory
if not exist "requirements.txt" (
    echo Error: requirements.txt not found
    echo Please run this script from the project root directory
    exit /b 1
)

echo Project structure verified
echo.

REM Install/update dependencies
echo Checking dependencies...
pip install -q -r requirements.txt

if %errorlevel% neq 0 (
    echo Failed to install dependencies
    exit /b 1
)

echo Dependencies installed
echo.

REM Run tests
echo Running DiagnoReport Test Suite...
echo ======================================================
echo.

python tests/test_runner.py

if %errorlevel% equ 0 (
    echo.
    echo ======================================================
    echo Test suite completed successfully
    echo.
    echo Test Results Summary:
    if exist "tests\test_summary.json" (
        echo   See: tests\test_summary.json
    )
    echo.
    echo Generated Reports:
    for %%f in (tests\output_*.json) do echo   %%f
    echo.
) else (
    echo.
    echo ======================================================
    echo Test suite failed
    exit /b 1
)

echo ======================================================
pause
