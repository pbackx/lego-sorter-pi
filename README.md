# Automated LEGO sorting machine

![A picture of the built machine, going from right to left: a hopper feeds the bricks into a belt that moves them to a camera, ending up in a wheel consisting of 6 buckets where the sorted bricks are stored](https://raw.githubusercontent.com/pbackx/lego-sorter-pi/main/lego_sorter_overview.jpg "Deep learning automated LEGO sorting machine")

This repository contains the code that is needed to make [my deep learning automated LEGO sorting machine](https://rebrickable.com/mocs/MOC-90902/pbackx/automated-lego-sorting-machine/#details) work. The code is completely free, however, I ask a small contribution for the instructions to build the machine. 

It has been a lot of work and I am currently completely overhauling this repository to make it easier to get started. However, at this point the machine is not plug and play. You will need some knowledge of Linux and Python to get it up and running.

Important links:
- [You can find the MOC model on Rebrickable](https://rebrickable.com/mocs/MOC-90902/pbackx/automated-lego-sorting-machine/#details).
- [I continuously improve and try new things. Sign up here if you want to receive updates by e-mail.](https://subscribepage.io/sorting-updates)

# Introduction
The software for the sorting machine consists of 3 parts:
- The EV3 is responsible for the mechanics. It will signal the motors to move the belt and rotate the buckets. It also reads the sensor to find the correct bucket position.
- The Raspberry Pi is in control of the operations: It instructs the EV3 to place one LEGO brick in front of the camera. Next, it takes a picture and sends it to the PC for recognition. Based on what brick was recognized it tells the EV3 to put it in the right bucket.
- The PC is the part that is going to run the deep learning network (AI) and recognize the LEGO bricks. Ideally this PC has a proper graphical card (GPU) as this will speed up the execution and training of the deep learning network. There are also ways to do this in the cloud, but this is not yet part of this document.

I have written these pages in an order that will give you results as soon as possible:
1. Move the belts and buckets by setting up the EV3
2. Set up the Raspberry Pi to take pictures
3. Configure the PC to train the deep learning network
4. Run the network for identifying bricks
5. Reconfigure the Raspberry Pi so it can sort the bricks fully automated

# How to get help
Keep in mind that setting up the machine is not easy. It requires knowledge of Linux, programming and a bit about AI (deep learning). Most of all, it requires a lot of patience and the willingness to Google if you encounter trouble (or ask ChatGPT, that can also be incredibly helpful).

If you feel this document is not clear or steps are missing, feel free to open [a new discussion](https://github.com/pbackx/lego-sorter-pi/discussions).

If you have found an issue or want to improve the code or documentation, you can create an issue or pull request.

Should you need a custom, fully functioning solution that works out of the box, you can contact me for bespoke work, but I can't guarantee you I will be able to look into this right away.

# EV3
## Overview
The communication between the EV3 and Raspberry Pi will go over [MQTT](https://mqtt.org/). It is a very lightweight way of communicating and on top of that, it is easy to debug, since many programs can be listening to the messages (we'll see an example of that later on).

A previous version of the code use RPyC, but this no longer works between the old EV3 and newer systems, such as the Raspberry Pi or your computer.

For now, we will control the EV3 from our main PC, no Raspbery Pi is needed at this point.

## Initial Setup
Follow [the ev3dev getting started documentation](https://www.ev3dev.org/docs/getting-started/). Unless you are able to connect to your ev3dev via SSH (step 6) there is no point in continuing the rest of this document.

Some general remarks before we continue:
- All the following commands need to be executed on the EV3 while logged in via SSH.
- The EV3 is a fairly old computer. Compared to your laptop, it is extremely slow. Many operations will take some time to run. I will mention this a few times, because it really is slow.

Ev3dev is based on the Debian Stretch operating system, which is no longer maintained. To be able to install software, we first have to switch `apt` to use the archived repositories. Edit /etc/apt/sources.list to use the archives:

	deb http://archive.debian.org/debian stretch main contrib non-free
	deb http://archive.ev3dev.org/debian stretch main

Now `sudo apt update` should run without errors.

I am not sure if this is absolutely needed, but I took the time to run `sudo apt upgrade` to make sure everything is up-to-date with the latest software that was ever released for Debian Stretch. Keep in mind that this is going to take a long time to run on the ev3.

## Mosquitto MQTT Broker
To send and listen to MQTT messages, we need a central process that will manage the messages. This is called the MQTT broker.

You need to have one in your network. We will run it on the EV3 since it already comes with one preinstalled. The broker software we will use is called Mosquitto.

You can start it with:

	sudo systemctl start mosquitto

And to make sure it will restart when the EV3 is rebooted:

	sudo systemctl enable mosquitto

Finally, you can verify it is running correctly:

	sudo systemctl status mosquitto

You can now connect to this broker from anywhere in your network. One tool we will use for testing later on is [MQTT Explorer](https://mqtt-explorer.com/)

You can download this to your PC and install it. When started, you should be able to connect to `mqtt://ev3dev.local:1883`. Keep it open, because we'll use it in the next section to test the software controlling the motors and sensor.

## Control software
Finally, we can install the software that wil listen for MQTT messages and have the robot perform actions based on those messages.

Start by installing `venv` and `pip`:

	sudo apt install python3-venv python3-pip

(Note that all code for the LEGO sorter will use Python 3, so you must install the Python 3 version of venv and pip)

Now create and activate the virtual environment:

	python3 -m venv --system-site-packages lego-sorter-venv
	source lego-sorter-venv/bin/activate

(for some reason, this is again terribly slow with no progress indication)

Create a folder to hold your code:

	mkdir lego-sorter
	cd lego-sorter

Now copy the files in this project's ev3 folder into that folder. The easiest way is to use secure copy. Run the following commands on your PC:

    scp .\requirements.txt robot@ev3dev.local:./lego-sorter/requirements.txt
    scp .\main.py robot@ev3dev.local:./lego-sorter/main.py

With the files copied over, the next commands are again on the EV3:

    python -m pip install -r requirements.txt

With the libraries installed, you can now run the program. Keep in mind that the turntable with the buckets will
automatically move to the bucket, so be prepared for some movement:

    python main.py

After the buckets have been calibrated, you should see the message `Connected with result code 0`

To test things out, go back to MQTT Explorer and in the public are enter the following message:

    topic: sorter/move_turntable
    payload type: raw
    payload: 1

The turntable should now move to the next bucket. Send a payload of 0 to move it back.

Other commands you can try are `sorter/on` and `sorter/off` to turn the belts on and off. No payload is required for these commands.

## Automatically start the program on boot

The final step is to automatically start the program when the EV3 boots. This is done by creating a systemd service.

Create a file `/etc/systemd/system/robot-control.service` with the following content:

    [Unit]
    Description=Robot Control
    Wants=network-online.target mosquitto.service
    After=network-online.target mosquitto.service
    [Service]
    Type=simple
    User=robot
    Environment=PYTHONUNBUFFERED=1
    WorkingDirectory=/home/robot/lego-sorter
    ExecStart=/home/robot/lego-sorter-venv/bin/python main.py
    Restart=always
    RestartSec=10
    SyslogIdentifier=robot-control
    [Install]
    WantedBy=multi-user.target

Now start and enable the service:

    sudo systemctl start robot-control
    sudo systemctl enable robot-control

You can check the status of the service with `sudo systemctl status robot-control`

From now on, you will know that the EV3 is fully started and ready to receive commands when the turntable moves to 
the first bucket.

# Raspberry Pi (part 1)

## Preparation

Now comes the interesting part. In this first step, we are going to generate as many image as possible of LEGO bricks.
These images will be used to train the deep learning network in the next step.

I would suggest that you start small. Pick about 3 brick types. The more different, the easier. Of each brick type,
find 5 to 10 samples in your LEGO collection. For the documentation, I chose the following:

- [3023 Plate 1x2](https://www.bricklink.com/v2/catalog/catalogitem.page?P=3023)
- [15712 Tile 1x1 with Open Clip](https://www.bricklink.com/v2/catalog/catalogitem.page?P=15712)
- [43857 Liftarm Thick 1x2](https://www.bricklink.com/v2/catalog/catalogitem.page?P=43857)

Any bricks will work, there is absolutely no reason to use exactly the same ones.

## Focusing the camera

Getting the right focus can be a bit tricky. Most lenses have two things you can change: focus and aperture. A good start
is to put the focus all the way to near and play around with aperture.

If you want to have more immediate feedback, the best option is to connect a screen to the Raspberry Pi and use the
`rpicam-hello` tool. This tool allows you to see the camera feed and change the focus and aperture in real-time.

    rpicam-hello -t 100s

(The 100s parameter will keep the app open for 100 seconds, otherwise it will close after 5s)

## Setting up the Raspberry Pi

On the Raspberry Pi, I installed the latest Raspberry Pi OS Lite 64-bit operating system and I gave the Raspberry the `legopi` name.

See the general documentation Raspberry Pi documentation on how to do this, but the [Raspberry Pi Imager](https://www.raspberrypi.org/software/) is the easiest way to get started.

Before you continue, you should have your Pi running and be able to connect to it via SSH. 

As I generally do, I always update the system with `sudo apt update` and `sudo apt upgrade` to make sure the latest software is installed. While this is not strictly necessary, it is good practice.

At this point, you may want to test the camera. The easiest way is to make a picture and start a temporary server:

```
rpicam-jpeg -o test.jpg
python -m http.server 8080
```

On your laptop, you should now be able to view the picture at http://legopi.local:8080/test.jpg

If this does not work, please do not continue. Make this work first.

Now install git and clone this repository:

	sudo apt install git
	git clone git@github.com:pbackx/lego-sorter-pi.git

For the Python code, we'll need a few dependencies. Generally, I would install these with `pip` but these two libraries
use hardware functions, so it is usually a better idea to use `apt` for them:

```
sudo apt install -y gcc python3-dev python3-picamera2 python3-opencv
```

Note that previous versions of the machine used picamera 1. Although picamera2 is still in beta, it appears the first 
version is no longer available. If you are interested, full documentation for picamera2 is available as 
[a giant PDF](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf) (there does not seem to be another format 
available).

Same as on the EV3, we will work inside a Python virtual environment:

	python3 -m venv --system-site-packages ./lego-sorter-venv
	source ./lego-sorter-venv/bin/activate
	pip install -r lego-sorter-pi/pi/requirements.txt

(Note that we include the system packages since this is how picamera2 and opencv were installed)

## Starting Jupyter Lab on the Pi

If you didn't activate the virtual environment yet, do so now:

    source ./lego-sorter-venv/bin/activate

To make it easier to understand and learn about the code, we will perform the next steps in Jupyter Lab:

	jupyter lab --no-browser --ip=*

You can now open Jupyter Lab on your laptop. In the output of this startup process, you'll see a URL that contains a 
token. Copy the token to the clipboard and open the URL:

http://legopi.local:8888/lab

You will be asked to enter the token and log in.

The next steps will happen in your browser. In the pi folder, you can now go over the first 3 notebooks:

- `01_testing_camera.ipynb` is another test of the camera, but this time from Python code.
- `02_motor_control.ipynb` is a demonstration of how to control the EV3 motors from the Raspberry Pi over MQTT.
- `03_taking_pictures.ipynb` is when we actually take pictures of the LEGO bricks.

Run through these 3 notebooks first before continuing with the next section. Ideally, you have about 100 pictures taken
before continuing, but if you are impatient, less will work too, however, the results will be less accurate.

# Training the model

The next step is using the training data to train a deep learning model. All of this work either happens on your PC 
or in the cloud. I will assume you have a PC with a decent GPU, but if you don't, you can use Google Colab or another 
cloud service.

## Cleaning and Labeling the images

First start by copying the images that you have taken on the Raspberry Pi to your PC. You can use `scp` for this:

    scp peter@legopi.local:lego-sorter-pi/data/new/* .\data\new

Inside that folder, create a subfolder for each brick type. The name is not that important. For example this is what
I used:

    mkdir data\new\3023plate1x2
    mkdir data\new\15712tile1x1withopenclip
    mkdir data\new\43857liftarmthick1x2

Now move the images to the correct folder. I like to do this in the Windows file manager, because it allows you to show 
previews of your photos, so you don't need to open them one by one.

Note that there will be images that are not usable. The part may not be clearly visible or there may be 2 parts on the
belt. These images should be removed.

Ideally you have about the same number of images for each brick type. If there is a big difference, it is best to run
just that single type a few times through the machine.

When you are done, move everything into `data/labeled`. The repository contains an example set of my images. You can
reuse these, or, much better, use your own.

## Configuring the Python environment on your PC

The next step is to configure your environment. Ideally, you have an Nvidia GPU in your PC.

To get everything up and running you will want to install the following, Google for specific steps for your operating 
system:
- (Windows only) Install WSL2 and your preferred Linux distribution.
- Install NVida CUDA and cuDNN.
- Install Docker

With these items installed, a simple test to see if the Cuda drivers are correctly configured is to run 

    nvidia-smi

This should show you the status of your GPU.

Next we will check if Docker is correctly installed:

    docker run hello-world

Finally, we need to verify if Docker can access the GPU. Run the following command:

    docker run --rm --gpus all tensorflow/tensorflow:2.18.0-gpu-jupyter nvidia-smi

As before, you should see your GPU listed. You will not see any processes running (as you may have seen when you
initially ran `nvidia-smi`, because the container does not have access to the host's processes.

## Launching the training environment

With these steps completed, you can now start the training environment:

    cd pc_training
    docker compose build
    docker compose up

This will start a Jupyter Lab environment on your PC. You can access it by copying the link that is shown in the output
of the command. It will look something like this:

     http://127.0.0.1:8888/lab?token=...

You can now open the `01_train_model.ipynb` notebook and run through the steps. This will show a basic example of
applying transfer learning to the data you have collected.

## Running the prediction server

Now that we have trained the model, it is time to make the model available to the Raspberry Pi that is controlling the
machine. We will do this through a small Flask server that expose a simple REST API.

First copy the model to the pc_serving folder, so we have a backup and don't have to worry about the model being overwritten:
    
    cp pc_training/model.keras pc_serving/model.keras

Now build and start the server:

    cd pc_serving
    docker compose build
    docker compose up

You can now go to the server documentation at http://localhost:8000/docs#/default/predict_predict_post

On this page, you can test out the server by selecting one of your images and clicking the "Execute" button.

# Raspberry Pi (part 2)

Now we are finally at the point where we can bring everything together and have the machine automatically sort bricks.

Make sure that:

- The EV3 is running and has correctly positioned the buckets.
- The prediction server on your PC is running.

SSh into the Raspberry Pi and start Jupyter Lab:

    source ./lego-sorter-venv/bin/activate
    jupyter lab --no-browser --ip=*

Go to http://legopi.local:8888/lab and open the `04_sorting_bricks.ipynb` notebook and run through the steps.

# Conclusion

You should now have a fully functioning sorting machine. You can now start processing as many bricks as you can.
Every time you do, you will generate new input data for the training algorithm, so be sure to redo the training 
from time to time. 
