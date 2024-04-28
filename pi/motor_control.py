import paho.mqtt.client as mqtt

class MotorControl:
    def __init__(self, ev3_host = 'ev3dev.local', ev3_port = 1883):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.connect(ev3_host, ev3_port, 60)
        self.client.loop_start()

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_all(self):
        self.client.publish('sorter/on')
        
    def stop_all(self):
        self.client.publish('sorter/off')
    
    def move_to_center(self, x):
        self.client.publish('sorter/move_to_center', x)
        
    def clear_camera_belt(self):
        self.client.publish('sorter/clear_camera_belt')
    
    def move_turntable(self, position):
        self.client.publish('sorter/move_turntable', position)