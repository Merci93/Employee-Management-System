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
docker-compose up
@REM @REM docker-compose up -d

@REM @REM Call virtual environment setup
@REM CALL virtual-env.bat

@REM @REM Copy ems icon and replace default tkinter icon
@REM COPY img\CustomTkinter_icon_Windows.ico env\Lib\site-packages\customtkinter\assets\icons

@REM @REM @REM Activate the virtual environment and spin up the UI
@REM @REM ECHO Starting up UI ...
@REM @REM CALL env\Scripts\activate
@REM @REM python src\user_interface\main.py
