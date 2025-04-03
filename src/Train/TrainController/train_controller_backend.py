"""
Author: Aragya Goyal and Connor Marsh
Date: 03-20-2025
Description:

"""
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
import globals.global_clock as global_clock
import globals.track_data_class as global_track_data
import math
import time

class TrainController(QMainWindow):
    MPS_TO_MPH  = 2.23694
    M_TO_YARDS = 1.09361
    MI_TO_YARDS = 1760
    SERVICE_BRAKE_DECEL = 1.2 # (m/s²)
    EMERGENCY_BRAKE_DECEL = 2.73 # (m/s²)
    GRAVITY = 9.81 # (m/s²)

    def __init__(self, train_integrated=False, line_name="Green"):
        super().__init__()

        # Set up static memory
        self.line_name = line_name
        self.track_data = global_track_data.lines[self.line_name]

        # Set up defaults
        self.actual_speed = 0.0
        self.speed_limit = 0.0
        self.wayside_speed = 0.0
        self.wayside_authority = 0.0
        self.commanded_power = 0.0
        self.beacon_data = ""
        self.actual_temperature = 77.0 # Farenheight
        self.desired_temperature = 77.0 # Farenheight
        self.signal_failure = False
        self.brake_failure = False
        self.engine_failure = False
        self.air_conditioning_signal = False
        self.heating_signal = False
        self.headlights = False
        self.interior_lights = False
        self.right_doors = False # Closed default state
        self.left_doors = False # Close default state
        self.emergency_brake = False
        self.driver_target_speed = 0.0
        self.service_brake = False
        self.position = 0.0
        self.block_distance_traveled = 0.0
        self.next_station = "Edgebrook"
        self.announcement = False
        self.manual_mode = False
        self.target_speed = 0.0
        self.beacon_data_recieved = False
        
        #TODO: these defaults should be fixed - currently hard-coded
        self.current_block = self.track_data.blocks[63-1]
        self.current_section = self.current_block.id[0]
        self.previous_switch_entrance = False
        self.previous_switch_exit = True
        self.travel_direction = self.track_data.sections[self.current_section].increasing

        # Default for power calculation
        self.integral_error = 0.0
        self.Kp = 20000.0
        self.Ki = 75.0

        # For Dwelling
        self.stopping = False
        self.dwell = False

        self.global_clock = global_clock.clock

        if not train_integrated:
            # Set up timer for callback/update function
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update)
            self.timer.start(self.global_clock.train_dt)
    
    def update(self):
        # Check if auto or manual mode and calculate power
        self.speed_limit - self.current_block.speed_limit
        if self.manual_mode:
            self.target_speed = self.driver_target_speed
        else:
            self.target_speed = self.wayside_speed
        self.target_speed = min(self.target_speed, self.current_block.speed_limit*0.9)

        self.error = self.target_speed - self.actual_speed
        dt = self.global_clock.train_dt/1000 * self.global_clock.time_multiplier
        self.integral_error += self.error * dt
        commanded_power_1 = (self.Kp * self.error) + (self.Ki * self.integral_error)
        commanded_power_2 = (self.Kp * self.error) + (self.Ki * self.integral_error)
        commanded_power_3 = (self.Kp * self.error) + (self.Ki * self.integral_error)
        if (commanded_power_1 == commanded_power_2 and commanded_power_1 == commanded_power_3 and commanded_power_2 == commanded_power_3):
            self.unramped_commanded_power = commanded_power_1
        else:
            self.commanded_power = 0

        self.update_track_location()
        self.update_safety()
        self.update_auxiliary()

    def update_track_location(self):
        # Calculate distance within the block
        distance_within_block = self.position - self.block_distance_traveled
        if distance_within_block > self.current_block.length:
            self.block_distance_traveled += self.current_block.length
            if self.current_block.switch and not self.previous_switch_exit:
                self.previous_switch_exit = True
                self.previous_switch_entrance = True
                QTimer.singleShot(int(500/self.global_clock.time_multiplier), self.process_beacon_data)
            elif self.current_block.switch_exit and not self.previous_switch_entrance:
                self.previous_switch_exit = True
                self.previous_switch_entrance = False
                switch = self.track_data.switches[self.track_data.switch_exits[self.current_block.id].switch_entrance]
                self.current_block = self.track_data.blocks[int(switch.positions[0].split("-")[0])-1]
            elif not (self.previous_switch_entrance and self.previous_switch_exit):
                self.current_block = self.track_data.blocks[int(self.current_block.id[1:])+(self.travel_direction*2-1)-1]
                self.previous_switch_exit = False
                self.previous_switch_entrance = False

        # Move to new section
        if self.current_block.id[0] != self.current_section:
            increasing = self.track_data.sections[self.current_block.id[0]].increasing
            if increasing == 2:
                self.travel_direction = 1 if self.current_block.id[0] > self.current_section else 0
            else:
                self.travel_direction = increasing
            self.current_section = self.current_block.id[0]

    def update_safety(self):
        # Ramp up power for passenger comfort
        if self.unramped_commanded_power > self.commanded_power:
            ramp_rate = 10000.0
            power_diff = self.unramped_commanded_power - self.commanded_power
            dt = self.global_clock.train_dt/1000 * self.global_clock.time_multiplier
            max_delta = ramp_rate * dt
            if abs(power_diff) < max_delta:
                self.commanded_power = self.unramped_commanded_power
            else:
                self.commanded_power += math.copysign(max_delta, power_diff)
        else:
            self.commanded_power = self.unramped_commanded_power

        # Check for failures
        if (self.signal_failure or self.brake_failure or self.engine_failure):
            self.emergency_brake = True

        # Check for invalid power commands
        new_service_state = False
        if (self.commanded_power <= 0):
            self.commanded_power = 0.0
            new_service_state = True
        elif (self.commanded_power > 120000):
            self.commanded_power = 120000.0
        
        if not self.manual_mode:
            self.service_brake=new_service_state

        # Check authority and stopping distance and override speed calcs
        self.wayside_authority -= (self.actual_speed/self.MPS_TO_MPH * self.global_clock.train_dt/1000*self.global_clock.time_multiplier)*self.M_TO_YARDS

        theta = math.atan(self.current_block.grade / 100)
        service_dist = ((self.actual_speed/self.MPS_TO_MPH) ** 2) / (2 * (self.SERVICE_BRAKE_DECEL + (self.GRAVITY * math.sin(theta * (math.pi/180)))))
        service_dist *= self.M_TO_YARDS

        if (self.wayside_authority < service_dist and self.wayside_authority > 10):
            self.emergency_brake = True
        elif (self.wayside_authority < (3*service_dist)):
            self.service_brake = True
        if self.wayside_authority < 5:
            self.service_brake = True
        # else:
        #     self.service_brake = False #TODO: Ask profeta how we should handle manual mode service brakes if he wants a toggle but also wants it vital.

        if (self.emergency_brake):
            self.commanded_power = 0.0 # Kill engine if emergency brake is activated
            self.integral_error = 0

        if (self.service_brake):
            self.commanded_power = 0.0 # Kill engine if emergency brake is activated
            self.integral_error = 0

    def update_auxiliary(self):
        # Set the HVAC Signals
        self.air_conditioning_signal = self.actual_temperature > self.desired_temperature
        self.heating_signal = self.actual_temperature < self.desired_temperature

        # Check time for lights
        if (not self.manual_mode):
            if (self.global_clock.hour >= 19 and self.global_clock.hour <= 24) or (self.global_clock.hour >= 0 and self.global_clock.hour < 7) or self.current_block.underground:
                self.interior_lights = True
                self.headlights = True
            else:
                self.interior_lights = False
                self.headlights = False

        # Close doors if we are moving
        if (self.actual_speed > 0):
            self.left_doors = False
            self.right_doors = False

        # check for stopping at stations/do announcements
        if (self.wayside_authority < 50):
            self.stopping = True
        
        if self.stopping and self.current_block.station:
            QTimer.singleShot(int(500/self.global_clock.time_multiplier), self.start_dwell)
            QTimer.singleShot(int(30500/self.global_clock.time_multiplier), self.end_dwell)
        if self.dwell:
            self.service_brake = True

    def start_dwell(self):
        self.dwell = True
        if self.actual_speed == 0.0:
            if not self.manual_mode:
                if self.track_data.stations[self.current_block].doors == 0:
                    self.left_doors = True
                elif self.track_data.stations[self.current_block].doors == 1:
                    self.right_doors = True
                else:
                    self.left_doors = True
                    self.right_doors = True

    def end_dwell(self):
        self.left_doors = False
        self.right_doors = False
        self.dwell = False
        self.stopping = False

    def process_beacon_data(self):
        self.previous_switch_entrance = True
        self.previous_switch_exit = False
        switch = self.track_data.switches[self.current_block.id]
        switch_block_0 = switch.positions[0].split("-")[1]
        switch_block_1 = switch.positions[1].split("-")[1]
        if self.beacon_data_recieved:
            if self.track_data.blocks[int(switch_block_0)-1].beacon:
                self.current_block = self.track_data.blocks[int(switch_block_0)-1]
            else:
                self.current_block = self.track_data.blocks[int(switch_block_1)-1]
            self.beacon_data_recieved = False
        else:
            if not self.track_data.blocks[int(switch_block_0)].beacon:
                self.current_block = self.track_data.blocks[int(switch_block_0)-1]
            else:
                self.current_block = self.track_data.blocks[int(switch_block_1)-1]

    def set_input_data(self, testbench_data=None, train_model_data=None):
        selected_data = None
        selected = ""

        if testbench_data:
            selected_data = testbench_data
            selected = "testbench"
        elif train_model_data:
            selected_data = train_model_data
            selected = "train_model"

        if selected == "testbench" or selected == "train_model":
            self.actual_speed = selected_data.get("actual_speed", self.actual_speed)
            self.wayside_speed = selected_data.get("wayside_speed", self.wayside_speed)
            # self.wayside_authority = selected_data.get("wayside_authority", self.wayside_authority)
            self.position = selected_data.get("position", self.position)

            if self.beacon_data != selected_data.get("beacon_data", self.beacon_data):
                self.beacon_data_recieved = True
            self.beacon_data = selected_data.get("beacon data", self.beacon_data)

            # Passengers can turn on the ebrake but not turn it off
            passengerEbrake = selected_data.get("emergency_brake", False)
            if passengerEbrake:
                self.emergency_brake = True

            self.actual_temperature = selected_data.get("actual_temperature", self.actual_temperature)
            self.signal_failure = selected_data.get("signal_failure", self.signal_failure)
            self.brake_failure = selected_data.get("brake_failure", self.brake_failure)
            self.engine_failure = selected_data.get("engine_failure", self.engine_failure)

    def get_output_data(self):
        data = {}
        data["commanded_power"] = self.commanded_power
        data["service_brake"] = self.service_brake
        data["emergency_brake"] = self.emergency_brake
        data["left_doors"] = self.left_doors
        data["right_doors"] = self.right_doors
        data["interior_lights"] = self.interior_lights
        data["headlights"] = self.headlights
        data["heating_signal"] = self.heating_signal
        data["air_conditioning_signal"] = self.air_conditioning_signal
        data["announcements"] = self.next_station
        return data