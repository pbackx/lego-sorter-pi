import rpyc

class MotorControl:
    def __init__(self, ev3_ip, pixels_per_rotation = 90):
        self.ev3_ip = ev3_ip
        self.pixels_per_rotation = pixels_per_rotation
        self.ev3_connection = rpyc.classic.connect(self.ev3_ip)
        self.ev3dev2_motor = self.ev3_connection.modules['ev3dev2.motor']
        self.camera_belt = self.ev3dev2_motor.MediumMotor(self.ev3dev2_motor.OUTPUT_A)
        self.main_belt = self.ev3dev2_motor.LargeMotor(self.ev3dev2_motor.OUTPUT_B)
        self.hopper_belt = self.ev3dev2_motor.LargeMotor(self.ev3dev2_motor.OUTPUT_C)
        self.turntable = self.ev3dev2_motor.MediumMotor(self.ev3dev2_motor.OUTPUT_D)
        self.turntable_rotations_per_bucket = 3.3
        self.turntable_current_position = 0
        
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
    
    def tune_turntable(self, amount = -0.1):
        turntable.on_for_rotations(motor_control.ev3dev2_motor.SpeedPercent(50), amount)
        
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
        self.turntable.on_for_rotations(self.ev3dev2_motor.SpeedPercent(50), positions_to_move * 3.3)
