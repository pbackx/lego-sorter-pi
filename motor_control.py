import rpyc
from time import sleep

class MotorControl:
    def __init__(self, ev3_ip, pixels_per_rotation = 90):
        self.ev3_ip = ev3_ip
        self.pixels_per_rotation = pixels_per_rotation
        self.ev3_connection = rpyc.classic.connect(self.ev3_ip)
        self.ev3dev2_motor = self.ev3_connection.modules['ev3dev2.motor']
        self.ev3dev2_sensor = self.ev3_connection.modules['ev3dev2.sensor']
        self.ev3dev2_sensor_lego = self.ev3_connection.modules['ev3dev2.sensor.lego']
        
        self.camera_belt = self.ev3dev2_motor.MediumMotor(self.ev3dev2_motor.OUTPUT_A)
        self.main_belt = self.ev3dev2_motor.LargeMotor(self.ev3dev2_motor.OUTPUT_B)
        self.hopper_belt = self.ev3dev2_motor.LargeMotor(self.ev3dev2_motor.OUTPUT_C)
        self.turntable = self.ev3dev2_motor.MediumMotor(self.ev3dev2_motor.OUTPUT_D)
        self.turntable_rotations_per_bucket = 3.3
        self.turntable_current_position = 0
        
        self.color_sensor = self.ev3dev2_sensor_lego.ColorSensor(self.ev3dev2_sensor.INPUT_4)
        self.color_sensor.mode = self.color_sensor.MODE_COL_REFLECT
        
        self.move_turntable_to_next_bucket()
        
    def on_all(self):
        self.hopper_belt.on(self.ev3dev2_motor.SpeedPercent(60))
        self.main_belt.on(self.ev3dev2_motor.SpeedPercent(-50))
        self.camera_belt.on(self.ev3dev2_motor.SpeedPercent(70))
        
    def stop_all(self):
        self.hopper_belt.stop()
        self.main_belt.stop()
        self.camera_belt.stop()
    
    def move_to_center(self, x):
        diff = 320 - x
        self.camera_belt.on_for_rotations(self.ev3dev2_motor.SpeedPercent(25), -diff/self.pixels_per_rotation)
        
    def clear_camera_belt(self):
        self.camera_belt.on_for_rotations(self.ev3dev2_motor.SpeedPercent(50), 10)
    
    def move_turntable_to_next_bucket(self, direction = 1):
        if direction > 0: 
            self.turntable.speed_sp = self.turntable.max_speed/2
        else:
            self.turntable.speed_sp = -self.turntable.max_speed/2
        self.turntable.run_forever()
        sleep(0.5)
        found_bucket = False
        for i in range(100):
            intensity = self.color_sensor.reflected_light_intensity
            if intensity > 10:
                self.turntable.stop()
                found_bucket = True
                break
            sleep(0.25)
        if not found_bucket:
            self.turntable.stop()
            raise Exception("Could not find next bucket.")
            
    def move_turntable(self, position):
        # convert to degrees
        current_position_degrees = self.turntable_current_position * 60
        position_degrees = position * 60
        # angle between them
        diff_degrees = position_degrees - current_position_degrees
        diff_degrees = ((diff_degrees + 180) % 360) - 180
        # convert back
        positions_to_move = diff_degrees / 60
        self.turntable_current_position = position
        
        if positions_to_move != 0:
            direction = 1 if positions_to_move > 0 else -1
            for i in range(int(abs(positions_to_move))):
                self.move_turntable_to_next_bucket(direction)
                sleep(0.1)
