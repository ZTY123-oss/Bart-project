@echo off
rem Launch the guessing game. Prefer system Python, fall back to the DSH bundled Python.
setlocal
set "SCRIPT=%~dp0number_guessing.py"
where pythonw >nul 2>nul
if %errorlevel%==0 (
    start "" pythonw "%SCRIPT%"
) else (
    start "" "G:\deepseek api\resources\runtime\primary-runtime\dependencies\python\pythonw.exe" "%SCRIPT%"
)
endlocal
