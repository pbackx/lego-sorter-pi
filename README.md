# Automated LEGO sorting machine

![A picture of the built machine, going from left to right: a hopper feeds the bricks into a belt that moves them to a camera, ending up in a wheel consisting of 6 buckets where the sorted bricks are stored](https://raw.githubusercontent.com/pbackx/lego-sorter-pi/main/lego_sorter_overview.jpg "Deep learning automated LEGO sorting machine")

This repository contains the code that is needed to make [my deep learning automated LEGO sorting machine](https://rebrickable.com/mocs/MOC-90902/pbackx/automated-lego-sorting-machine/#details) work. The code is completely free, however, I ask a small contribution for the instructions to build the machine. 

It has been a lot of work and I am currently completely overhauling this repository to make it easier to get started. However, at this point the machine is not plug and play. You will need some knowledge of Linux and Python to get it up and running.

[You can find the MOC model on Rebrickable](https://rebrickable.com/mocs/MOC-90902/pbackx/automated-lego-sorting-machine/#details).

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

If you feel this document is not clear or steps are missing, feel free to open [a new discussion](https://github.com/pbackx/lego-sorter-pi/discussions.

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

# Raspberry Pi (part 1)

Coming soon. I am updating the code to use picamera2 instead of the old and unsupported picamera. 
This will take some time.
