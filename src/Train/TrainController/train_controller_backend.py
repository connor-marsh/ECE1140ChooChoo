"""
Author: Aragya Goyal
Date: 03-20-2025
Description:

"""
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import QTimer, QTime
import globals.global_clock as global_clock
import globals.track_data_class as global_track_data
import math

class TrainController(QMainWindow):
    MPS_TO_MPH  = 2.23694
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
        self.speed_limit = 20.0 #TODO: PLEASE MAKE THIS NORMAL
        self.wayside_speed = 0.0
        self.wayside_authority = 0.0
        self.commanded_power = 0.0
        self.passenger_emergency_stop = False
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
        self.door_right = False # Closed default state
        self.door_left = False # Close default state
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
        self.travel_direction = self.track_data.sections[self.current_section].increasing

        # Default for power calculation
        self.integral_error = 0.0
        self.Kp = 20000.0
        self.Ki = 75.0

        self.global_clock = global_clock.clock

        if not train_integrated:
            # Set up timer for callback/update function
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update)
            self.timer.start(self.global_clock.train_dt)


    def update(self):
        # Calculate distance within the block
        distance_within_block = self.position - self.block_distance_traveled
        if distance_within_block > self.current_block.length:
            self.block_distance_traveled += self.current_block.length
            self.current_block = self.track_data.blocks[int(self.current_block.id[1:])+(self.travel_direction*2-1)-1]
            if self.current_block.switch:
                QTimer.singleShot((500/self.global_clock.time_multiplier), self.process_beacon_data())
            elif self.current_block.switch_exit:
                switch = self.track_data.switches[self.track_data.switch_exits[self.current_block.id].switch_entrance]
                self.current_block = switch.positions[0].split("-")[0]

        # Check for failures
        if (self.signal_failure or self.brake_failure or self.engine_failure):
            self.emergency_brake = True
        
        # Check if auto or manual mode and calculate power
        if self.manual_mode:
            self.target_speed = min(self.driver_target_speed, self.speed_limit*0.9)
        else:
            self.target_speed = min(self.wayside_speed, self.speed_limit*0.9)

        self.error = self.target_speed - self.actual_speed
        self.integral_error += self.error * self.global_clock.train_dt/1000 * self.global_clock.time_multiplier
        commanded_power_1 = (self.Kp * self.error) + (self.Ki * self.integral_error)
        commanded_power_2 = (self.Kp * self.error) + (self.Ki * self.integral_error)
        commanded_power_3 = (self.Kp * self.error) + (self.Ki * self.integral_error) # TODO: need something for integral wind up
        if (commanded_power_1 == commanded_power_2 and commanded_power_1 == commanded_power_3 and commanded_power_2 == commanded_power_3):
            self.commanded_power = commanded_power_1
        else:
            self.commanded_power = 0

        # Check for invalid power commands
        new_service_state = False
        if (self.commanded_power < 0):
            self.commanded_power = 0.0
            new_service_state = True
        elif (self.commanded_power > 120000):
            self.commanded_power = 120000.0
        
        if not self.manual_mode:
            self.service_brake=new_service_state

        if (self.emergency_brake):
            self.commanded_power = 0.0 # Kill engine if emergency brake is activated
            self.integral_error = 0

        if (self.service_brake):
            self.commanded_power = 0.0 # Kill engine if emergency brake is activated
            self.integral_error = 0

        # TODO: Check authority and stopping distance and override speed calcs
        theta = math.atan(self.current_block.grade / 100)
        service_dist = ((self.actual_speed/self.MPS_TO_MPH) ** 2) / (2 * (self.SERVICE_BRAKE_DECEL + (self.GRAVITY * math.sin(theta * (math.pi/180)))))
        service_dist *= self.MPS_TO_MPH

        if (self.wayside_authority < service_dist):
            self.emergency_brake = True
        elif (self.wayside_authority < (1.5*service_dist)):
            self.service_brake = True

        # Set the HVAC Signals
        self.air_conditioning_signal = self.actual_temperature > self.desired_temperature
        self.heating_signal = self.actual_temperature < self.desired_temperature

        # Check time for lights
        if (not self.manual_mode):
            if (self.global_clock.hour >= 19 and self.global_clock.hour <= 24) or (self.global_clock.hour >= 0 and self.global_clock.hour < 7):
                self.interior_lights = True
                self.headlights = True
            else:
                self.interior_lights = False
                self.headlights = False

        # check underground for lights
        # TODO

        # check for stopping at stations/do announcements
        # TODO

    def process_beacon_data(self):
        switch = self.track_data.switches[self.track_data.switch_exits[self.current_block.id].switch_entrance]
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
            self.actual_speed = selected_data["actual_speed"]
            self.wayside_speed = selected_data["wayside_speed"]
            self.wayside_authority = selected_data["wayside_authority"]
            self.position = selected_data.get("position", self.position)

            if self.beacon_data != selected_data["beacon_data"]:
                self.beacon_data = selected_data["beacon data"]
                self.beacon_data_recieved = True

            # Passengers can turn on the ebrake but not turn it off
            self.emergency_brake = selected_data.get("emergency_brake", self.emergency_brake)

            self.actual_temperature = selected_data["actual_temperature"]
            self.signal_failure = selected_data["signal_failure"]
            self.brake_failure = selected_data["brake_failure"]
            self.engine_failure = selected_data["engine_failure"]

    def get_output_data(self):
        data = {}
        data["commanded_power"] = self.commanded_power
        data["service_brake"] = self.service_brake
        data["emergency_brake"] = self.emergency_brake
        data["left_doors"] = self.door_left
        data["right_doors"] = self.door_right
        data["interior_lights"] = self.interior_lights
        data["headlights"] = self.headlights
        data["heating_signal"] = self.heating_signal
        data["air_conditioning_signal"] = self.air_conditioning_signal
        data["announcements"] = self.next_station
        return data