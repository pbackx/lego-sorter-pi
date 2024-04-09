import paho.mqtt.client as mqtt
from ev3dev2.motor import OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, LargeMotor, MediumMotor, SpeedPercent
from ev3dev2.sensor import INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from time import sleep

pixels_per_rotation = 90

camera_belt = MediumMotor(OUTPUT_A)
main_belt = LargeMotor(OUTPUT_B)
hopper_belt = LargeMotor(OUTPUT_C)
turntable = MediumMotor(OUTPUT_D)

color_sensor = ColorSensor(INPUT_4)
color_sensor.mode = ColorSensor.MODE_COL_REFLECT

turntable_current_position = 0


def on_all():
    hopper_belt.on(SpeedPercent(60))
    main_belt.on(SpeedPercent(-50))
    camera_belt.on(SpeedPercent(70))


def stop_all():
    hopper_belt.stop()
    main_belt.stop()
    camera_belt.stop()


def move_to_center(x):
    diff = 320 - x
    camera_belt.on_for_rotations(SpeedPercent(25), -diff / pixels_per_rotation)


def clear_camera_belt():
    camera_belt.on_for_rotations(SpeedPercent(50), 10)


def move_turntable_to_next_bucket(direction=1):
    if direction > 0:
        turntable.speed_sp = turntable.max_speed / 2
    else:
        turntable.speed_sp = -turntable.max_speed / 2
    turntable.run_forever()
    sleep(0.5)
    found_bucket = False
    for i in range(100):
        intensity = color_sensor.reflected_light_intensity
        if intensity > 10:
            turntable.stop()
            found_bucket = True
            break
        sleep(0.25)
    if not found_bucket:
        turntable.stop()
        raise Exception("Could not find next bucket.")


def move_turntable(position):
    global turntable_current_position
    # convert to degrees
    current_position_degrees = turntable_current_position * 60
    position_degrees = position * 60
    # angle between them
    diff_degrees = position_degrees - current_position_degrees
    diff_degrees = ((diff_degrees + 180) % 360) - 180
    # convert back
    positions_to_move = diff_degrees / 60
    turntable_current_position = position

    if positions_to_move != 0:
        direction = 1 if positions_to_move > 0 else -1
        for i in range(int(abs(positions_to_move))):
            move_turntable_to_next_bucket(direction)
            sleep(0.1)


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sorter/#")


def on_message(client, userdata, msg):
    if msg.topic == "sorter/off":
        stop_all()
    elif msg.topic == "sorter/on":
        on_all()
    elif msg.topic == "sorter/move_to_center":
        move_to_center(int(msg.payload))
    elif msg.topic == "sorter/clear_camera_belt":
        clear_camera_belt()
    elif msg.topic == "sorter/move_turntable":
        move_turntable(int(msg.payload))


move_turntable_to_next_bucket()

client = mqtt.Client()
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
