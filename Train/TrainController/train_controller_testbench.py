"""
Train Controller Testbench
"""
class TrainControllerTestbenchWindow(QMainWindow):
    def __init__(self, train_controller_window):
        super().__init__()
        self.ui = TrainControllerTestbenchUI()
        self.ui.setupUi(self)
        self.train_controller_window = train_controller_window

        # Set up timer for callback/update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_testbench)
        self.timer.start(100)

    def update_testbench(self):
        self.display_air_conditioning()
        self.display_heating()
        self.display_headlights()
        self.display_internal_lights()
        self.display_doors()
        self.display_emergency_brakes()
        self.display_service_brakes()
        self.display_announcement()

    def display_announcement(self):
        if (self.train_controller_window.announcement):
            self.ui.tb_annunciation_system_display.setText(self.train_controller_window.next_station)

    def display_service_brakes(self):
        if (self.train_controller_window.service_brake):
            self.ui.tb_service_brakes_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_service_brakes_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_service_brakes_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_service_brakes_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_emergency_brakes(self):
        if (self.train_controller_window.emergency_brake):
            self.ui.tb_emergency_brake_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_emergency_brake_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_emergency_brake_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_emergency_brake_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_headlights(self):
        if (self.train_controller_window.headlights):
            self.ui.tb_headlight_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_headlight_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_headlight_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_headlight_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_internal_lights(self):
        if (self.train_controller_window.interior_lights):
            self.ui.tb_internal_light_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_internal_light_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_internal_light_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_internal_light_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_air_conditioning(self):
        if (self.train_controller_window.air_conditioning_signal):
            self.ui.tb_air_conditioning_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_air_conditioning_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_air_conditioning_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_air_conditioning_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_heating(self):
        if (self.train_controller_window.heating_signal):
            self.ui.tb_heating_signal_on_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_heating_signal_off_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_heating_signal_on_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_heating_signal_off_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

    def display_doors(self):
        if (self.train_controller_window.door_right):
            self.ui.tb_right_door_open_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_right_door_close_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_right_door_open_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_right_door_close_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")

        if (self.train_controller_window.door_left):
            self.ui.tb_left_door_open_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
            self.ui.tb_left_door_close_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
        else:
            self.ui.tb_left_door_open_light.setStyleSheet("background-color: transparent; font-weight: bold; font-size: 16px;")
            self.ui.tb_left_door_close_light.setStyleSheet("background-color: yellow; font-weight: bold; font-size: 16px;")
