@ECHO OFF

IF EXIST "env" (
    echo virtual environment found already exists.
) ELSE (
    ECHO Setting up virtual environment ...
    python -m venv env
    env\Scripts\activate
    python.exe -m pip install --upgrade pip
    CALL env\Scripts\activate
    pip install -r user_interface\ui_requirements.txt
    ECHO Virtual environment setup completed.
)
