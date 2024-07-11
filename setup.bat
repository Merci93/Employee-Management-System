@ECHO OFF

@REM @REM Setup Docker Environment and Containers
echo Setting up Docker ...
docker build -t docker/ems .
docker-compose up

@REM Call virtual environment setup
CALL virtual-env-setup.bat

@REM Activate the virtual environment and spin up the UI
ECHO Starting up UI ...
CALL env\Scripts\activate
python user_interface\src\ems.py
ECHO UI started successfully
