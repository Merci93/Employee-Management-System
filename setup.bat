@ECHO OFF

REM Force execution from the batch file's folder (project root)
cd /d "%~dp0"


@REM Check if image 'docker/ems' exists
SET IMAGE_NAME=docker/ems
FOR /F "tokens=*" %%i IN ('docker images -q %IMAGE_NAME%') DO SET IMAGE_EXISTS=%%i

IF NOT DEFINED IMAGE_EXISTS (
    echo Image %IMAGE_NAME% found, building %IMAGE_NAME% ...
    docker build -t %IMAGE_NAME% .
    echo Image build complete.
) ELSE (
    echo Image %IMAGE_NAME% already exists.
)

@REM Start Docker Containers
echo Starting Docker Containers...
docker-compose up -d

@REM Activate the virtual environment
CALL env\Scripts\activate

@REM Running Streamlit UI
ECHO Starting Streamlit UI ...
python -m streamlit run src/ems.py