First install system dependencies (not sure if these are really needed?)

    sudo apt update
    sudo apt install -y python3-picamera python3-opencv

Create and setup virtual env

    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt

Start Jupyter

    jupyter lab --no-browser --ip=*
