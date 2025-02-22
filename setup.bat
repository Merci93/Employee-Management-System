@ECHO OFF

docker_image_exists() (
    docker images -q %1 2>nul
)

@REM Check if the image 'docker/ems' exists
FOR /F "tokens=*" %%i IN ('docker images -q docker/ems') DO SET IMAGE_EXISTS=%%i

IF NOT DEFINED IMAGE_EXISTS (
    echo Image not found, building docker/ems ...
    docker build -t docker/ems .
    echo Image build complete.
) ELSE (
    echo Image docker/ems already exists.
)

@REM Setup Docker Environment and Containers
echo Starting Image ...
@REM docker-compose up
docker-compose up -d

@REM Activate the virtual environment and spin up the UI
ECHO Starting up UI ...
CALL env\Scripts\activate
streamlit run src\ems.py
