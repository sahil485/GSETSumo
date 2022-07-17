#!/usr/bin/env python3
from ev3dev.ev3 import *
import math
import time
from constants import *

class MotorHandler:
    def __init__(self, motors):
        self.motors = motors

    # Speed should be a dictionary of values referring to port and value (ex: {'outA': 100, 'outB': 100})
    def drive_speed(self, speed):
        for motor_port in speed.keys():
            self.motors[motor_port].run_forever(speed_sp=speed[motor_port])
        
    # Straight drive for a set distance; Speed should be a single value and distance in cm
    def drive_distance(self, speed, distance):
        print("distance and speed", distance, speed)
        time = self.calc_time(distance, speed)
        print("waiting for ", time)
        self.drive_time(speed, time)
    
    # Straight drive for a set amount of time
    def drive_time(self, speed, time_to_wait, stop_action='brake'):
        self.drive_speed({RIGHT_MOTOR_PORT: speed, LEFT_MOTOR_PORT: speed})
        time.sleep(time_to_wait)
        self.stop_motors(stop_action)

    def turn(self, speed, degrees):
        left_motor_dir = -1 if degrees >= 0 else 1
        right_motor_dir = -1 if degrees < 0 else 1

        time_to_wait = abs(degrees) / speed

        self.drive_speed({RIGHT_MOTOR_PORT: speed * right_motor_dir,
                        LEFT_MOTOR_PORT: speed * left_motor_dir}, time_to_wait)
        time.sleep(time_to_wait)
        
    def turn_90(direction, dur = 0.68):
        if direction == "right":
            multiplier = -1
        elif direction == "left":
            multiplier = 1
        right.run_forever(speed_sp=300 * multiplier)
        left.run_forever(speed_sp=-300 * multiplier)
        time.sleep(dur)
        right.stop(stop_action='hold')
        left.stop(stop_action='hold')
    
    def turn_180(self):
        for i in range(2):
            self.turn_90("right")
    
    def stop_motors(self, stop_action):
        for motor in self.motors.values():
            motor.stop(stop_action=stop_action)

    # Distance in cm and speed should be a single value
    def calc_time(self, distance, speed):
        angle = (distance / (2 * math.pi * WHEEL_RADIUS)) * 2 * math.pi
        time = angle / speed
        return time