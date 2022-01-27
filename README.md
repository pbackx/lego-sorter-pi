This code is for use with my LEGO sorting machine, which can be found on Rebrickable:
https://rebrickable.com/mocs/MOC-90902/pbackx/automated-lego-sorting-machine/

First install system dependencies (not sure if these are really needed?)

    sudo apt update
    sudo apt install -y python3-picamera python3-opencv

Create and setup virtual env

    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt

Start Jupyter

    jupyter lab --no-browser --ip=*
