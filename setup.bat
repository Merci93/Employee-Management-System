@ECHO OFF
REM Force execution from the batch file's folder (project root)
cd /d "%~dp0"

SET IMAGE_NAME=ems-app

REM ----------------------------------------
REM Select mode (dev or prod)
REM Usage: setup.bat dev   OR   setup.bat prod
REM Default = dev
REM ----------------------------------------
SET MODE=%1
IF "%MODE%"=="" SET MODE=dev

IF /I "%MODE%"=="dev" (
    ECHO Running in DEVELOPMENT mode...
    
    FOR /F "tokens=*" %%i IN ('docker images -q %IMAGE_NAME%') DO (
        ECHO Deleting old image %%i...
        docker rmi -f %%i
    )

    REM Build Docker image (always fresh build)
    ECHO Building Docker image %IMAGE_NAME%...
    docker build --no-cache -t %IMAGE_NAME% .

) ELSE (
    ECHO Running in PRODUCTION mode...

    REM Use timestamp as version tag (yyyy-mm-dd_HHMM)
    FOR /F "tokens=2 delims==" %%i IN ('wmic os get localdatetime /value') DO SET DTS=%%i
    SET VERSION=%DTS:~0,8%_%DTS:~8,4%

    ECHO Building Docker image %IMAGE_NAME%:%VERSION% ...
    docker build -t %IMAGE_NAME%:%VERSION% .

    docker tag %IMAGE_NAME%:%VERSION% %IMAGE_NAME%:latest
)

ECHO Starting Docker containers...
docker-compose up -d
