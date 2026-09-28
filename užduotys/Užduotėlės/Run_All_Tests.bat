@echo off
setlocal enabledelayedexpansion

for /L %%i in (1,1,66) do (
    set "folder=Problem_%%i"
    if %%i LSS 10 set "folder=Problem_0%%i"

    if exist "!folder!\__main__.py" (
        echo Running "!folder!\__main__.py" in directory "!folder!"...
        pushd "!folder!" > nul
        python "__main__.py"
        popd > nul
        echo.
    ) else (
        echo Warning: "!folder!\__main__.py" not found, skipping.
    )
)

endlocal
pause
