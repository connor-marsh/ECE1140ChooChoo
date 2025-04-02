# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TrainModel_UI_TestBench_Iteration_1.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

# pyright: ignorefile
# mypy: ignore-errors

from PyQt5.QtCore import * # type: ignore
from PyQt5.QtGui import * # type: ignore
from PyQt5.QtWidgets import * # type: ignore

import os
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class Ui_TestMainWindow(object):
    def setupUi(self, MainWindow): # type: ignore
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(732, 833)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(30, 10, 671, 771))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        # ------------------
        # Outputs Layout
        # ------------------
        self.Outputs = QFormLayout()
        self.Outputs.setObjectName("Outputs")
        # Row 0: Actual Velocity Label
        self.ActualVelocityLabel = QLabel(self.gridLayoutWidget)
        self.ActualVelocityLabel.setObjectName("ActualVelocityLabel")
        self.Outputs.setWidget(0, QFormLayout.LabelRole, self.ActualVelocityLabel)
        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Outputs.setItem(1, QFormLayout.LabelRole, self.verticalSpacer_13)
        # Row 2: Speed Limit Label
        # self.SpeedLimitLabel_2 = QLabel(self.gridLayoutWidget)
        # self.SpeedLimitLabel_2.setObjectName("SpeedLimitLabel_2")
        # self.Outputs.setWidget(2, QFormLayout.LabelRole, self.SpeedLimitLabel_2)
        # self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        # self.Outputs.setItem(3, QFormLayout.LabelRole, self.verticalSpacer_14)
        # Row 4: Wayside Speed Label
        self.WaysideSpeedLabel_2 = QLabel(self.gridLayoutWidget)
        self.WaysideSpeedLabel_2.setObjectName("WaysideSpeedLabel_2")
        self.Outputs.setWidget(4, QFormLayout.LabelRole, self.WaysideSpeedLabel_2)
        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Outputs.setItem(5, QFormLayout.LabelRole, self.verticalSpacer_15)
        # Row 6: Wayside Authority Label
        self.WaysideAuthorityLabel_2 = QLabel(self.gridLayoutWidget)
        self.WaysideAuthorityLabel_2.setObjectName("WaysideAuthorityLabel_2")
        self.Outputs.setWidget(6, QFormLayout.LabelRole, self.WaysideAuthorityLabel_2)
        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Outputs.setItem(7, QFormLayout.LabelRole, self.verticalSpacer_16)
        # Row 8: Passenger Emergency Stop Label
        self.PEmergencyStopLabel = QLabel(self.gridLayoutWidget)
        self.PEmergencyStopLabel.setObjectName("PEmergencyStopLabel")
        self.Outputs.setWidget(8, QFormLayout.LabelRole, self.PEmergencyStopLabel)
        self.verticalSpacer_17 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Outputs.setItem(9, QFormLayout.LabelRole, self.verticalSpacer_17)
        # Row 10: Signal Failure Label
        self.SignalFailureLabel = QLabel(self.gridLayoutWidget)
        self.SignalFailureLabel.setObjectName("SignalFailureLabel")
        self.Outputs.setWidget(10, QFormLayout.LabelRole, self.SignalFailureLabel)
        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Outputs.setItem(11, QFormLayout.LabelRole, self.verticalSpacer_18)
        # Row 12: Brake Failure Label
        self.BrakeFailureLabel = QLabel(self.gridLayoutWidget)
        self.BrakeFailureLabel.setObjectName("BrakeFailureLabel")
        self.Outputs.setWidget(12, QFormLayout.LabelRole, self.BrakeFailureLabel)
        self.verticalSpacer_19 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Outputs.setItem(13, QFormLayout.LabelRole, self.verticalSpacer_19)
        # Row 14: Engine Failure Label
        self.EngineFailureLabel = QLabel(self.gridLayoutWidget)
        self.EngineFailureLabel.setObjectName("EngineFailureLabel")
        self.Outputs.setWidget(14, QFormLayout.LabelRole, self.EngineFailureLabel)
        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Outputs.setItem(15, QFormLayout.LabelRole, self.verticalSpacer_20)
        # Note: ACSignal and HeatingSignal have been removed from Outputs

        self.TemperatureLabel = QLabel(self.gridLayoutWidget)
        self.TemperatureLabel.setObjectName("TemperatureLabel")
        self.Outputs.setWidget(16, QFormLayout.LabelRole, self.TemperatureLabel)
        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Outputs.setItem(17, QFormLayout.LabelRole, self.verticalSpacer_21)

        # Now add the corresponding output fields
        self.ActualVelocity = QLabel(self.gridLayoutWidget)
        self.ActualVelocity.setObjectName("ActualVelocity")
        self.Outputs.setWidget(0, QFormLayout.FieldRole, self.ActualVelocity)
        # self.SpeedLimit_2 = QLabel(self.gridLayoutWidget)
        # self.SpeedLimit_2.setObjectName("SpeedLimit_2")
        # self.Outputs.setWidget(2, QFormLayout.FieldRole, self.SpeedLimit_2)
        self.WaysideSpeed_2 = QLabel(self.gridLayoutWidget)
        self.WaysideSpeed_2.setObjectName("WaysideSpeed_2")
        self.Outputs.setWidget(4, QFormLayout.FieldRole, self.WaysideSpeed_2)
        self.WaysideAuthority_2 = QLabel(self.gridLayoutWidget)
        self.WaysideAuthority_2.setObjectName("WaysideAuthority_2")
        self.Outputs.setWidget(6, QFormLayout.FieldRole, self.WaysideAuthority_2)
        self.PEmergencyStop = QLabel(self.gridLayoutWidget)
        self.PEmergencyStop.setObjectName("PEmergencyStop")
        self.Outputs.setWidget(8, QFormLayout.FieldRole, self.PEmergencyStop)
        self.SignalFailure = QLabel(self.gridLayoutWidget)
        self.SignalFailure.setObjectName("SignalFailure")
        self.Outputs.setWidget(10, QFormLayout.FieldRole, self.SignalFailure)
        self.BrakeFailure = QLabel(self.gridLayoutWidget)
        self.BrakeFailure.setObjectName("BrakeFailure")
        self.Outputs.setWidget(12, QFormLayout.FieldRole, self.BrakeFailure)
        self.EngineFailure = QLabel(self.gridLayoutWidget)
        self.EngineFailure.setObjectName("EngineFailure")
        self.Outputs.setWidget(14, QFormLayout.FieldRole, self.EngineFailure)
        self.Temperature = QLabel(self.gridLayoutWidget)
        self.Temperature.setObjectName("Temperature")
        self.Outputs.setWidget(16, QFormLayout.FieldRole, self.Temperature)

        self.gridLayout.addLayout(self.Outputs, 1, 1, 1, 1)

        self.OUTPUTS = QLabel(self.gridLayoutWidget)
        self.OUTPUTS.setObjectName("OUTPUTS")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.OUTPUTS.setFont(font)
        self.OUTPUTS.setStyleSheet("background-color: rgb(151, 152, 119);")
        self.gridLayout.addWidget(self.OUTPUTS, 0, 1, 1, 1)

        # ------------------
        # Inputs Layout (reordered)
        # ------------------
        self.Inputs = QFormLayout()
        self.Inputs.setObjectName("Inputs")
        # Row 0: Wayside Speed
        self.WaysideSpeedLabel = QLabel(self.gridLayoutWidget)
        self.WaysideSpeedLabel.setObjectName("WaysideSpeedLabel")
        self.Inputs.setWidget(0, QFormLayout.LabelRole, self.WaysideSpeedLabel)
        self.WaysideSpeed = QLineEdit(self.gridLayoutWidget)
        self.WaysideSpeed.setObjectName("WaysideSpeed")
        self.Inputs.setWidget(0, QFormLayout.FieldRole, self.WaysideSpeed)
        # Row 1: Spacer
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(1, QFormLayout.LabelRole, self.verticalSpacer)
        # Row 2: Wayside Authority
        self.WaysideAuthorityLabel = QLabel(self.gridLayoutWidget)
        self.WaysideAuthorityLabel.setObjectName("WaysideAuthorityLabel")
        self.Inputs.setWidget(2, QFormLayout.LabelRole, self.WaysideAuthorityLabel)
        self.WaysideAuthority = QLineEdit(self.gridLayoutWidget)
        self.WaysideAuthority.setObjectName("WaysideAuthority")
        self.Inputs.setWidget(2, QFormLayout.FieldRole, self.WaysideAuthority)
        # Row 3: Spacer
        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(3, QFormLayout.LabelRole, self.verticalSpacer_2)
        # Row 4: Commanded Power
        self.CommandedPowerLabel = QLabel(self.gridLayoutWidget)
        self.CommandedPowerLabel.setObjectName("CommandedPowerLabel")
        self.Inputs.setWidget(4, QFormLayout.LabelRole, self.CommandedPowerLabel)
        self.CommandedPower = QLineEdit(self.gridLayoutWidget)
        self.CommandedPower.setObjectName("CommandedPower")
        self.Inputs.setWidget(4, QFormLayout.FieldRole, self.CommandedPower)
        # Row 5: Spacer
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(5, QFormLayout.LabelRole, self.verticalSpacer_5)
        # Row 6: Speed Limit
        # self.SpeedLimitLabel = QLabel(self.gridLayoutWidget)
        # self.SpeedLimitLabel.setObjectName("SpeedLimitLabel")
        # self.Inputs.setWidget(6, QFormLayout.LabelRole, self.SpeedLimitLabel)
        # self.SpeedLimit = QLineEdit(self.gridLayoutWidget)
        # self.SpeedLimit.setObjectName("SpeedLimit")
        # self.Inputs.setWidget(6, QFormLayout.FieldRole, self.SpeedLimit)
        # Row 7: Spacer
        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(7, QFormLayout.LabelRole, self.verticalSpacer_8)
        # Row 8: Beacon Data
        self.BeaconDataLabel = QLabel(self.gridLayoutWidget)
        self.BeaconDataLabel.setObjectName("BeaconDataLabel")
        self.Inputs.setWidget(8, QFormLayout.LabelRole, self.BeaconDataLabel)
        self.BeaconData = QLineEdit(self.gridLayoutWidget)
        self.BeaconData.setObjectName("BeaconData")
        self.Inputs.setWidget(8, QFormLayout.FieldRole, self.BeaconData)
        # Row 9: Spacer
        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(9, QFormLayout.LabelRole, self.verticalSpacer_7)
        # Row 10: Service Brakes
        self.ServiceBrakesLabel = QLabel(self.gridLayoutWidget)
        self.ServiceBrakesLabel.setObjectName("ServiceBrakesLabel")
        self.Inputs.setWidget(10, QFormLayout.LabelRole, self.ServiceBrakesLabel)
        self.ServiceBrakes = QCheckBox(self.gridLayoutWidget)
        self.ServiceBrakes.setObjectName("ServiceBrakes")
        self.Inputs.setWidget(10, QFormLayout.FieldRole, self.ServiceBrakes)
        # Row 11: Spacer
        self.verticalSpacer_30 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(11, QFormLayout.LabelRole, self.verticalSpacer_30)
        # Row 12: Exterior Lights
        self.ExtLightsLabel = QLabel(self.gridLayoutWidget)
        self.ExtLightsLabel.setObjectName("ExtLightsLabel")
        self.Inputs.setWidget(12, QFormLayout.LabelRole, self.ExtLightsLabel)
        self.ExtLights = QCheckBox(self.gridLayoutWidget)
        self.ExtLights.setObjectName("ExtLights")
        self.Inputs.setWidget(12, QFormLayout.FieldRole, self.ExtLights)
        # Row 13: Spacer
        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(13, QFormLayout.LabelRole, self.verticalSpacer_6)
        # Row 14: Interior Lights
        self.IntLightsLabel = QLabel(self.gridLayoutWidget)
        self.IntLightsLabel.setObjectName("IntLightsLabel")
        self.Inputs.setWidget(14, QFormLayout.LabelRole, self.IntLightsLabel)
        self.IntLights = QCheckBox(self.gridLayoutWidget)
        self.IntLights.setObjectName("IntLights")
        self.Inputs.setWidget(14, QFormLayout.FieldRole, self.IntLights)
        # Row 15: Spacer
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(15, QFormLayout.LabelRole, self.verticalSpacer_9)
        # Row 16: Left Doors
        self.LeftDoorsLabel = QLabel(self.gridLayoutWidget)
        self.LeftDoorsLabel.setObjectName("LeftDoorsLabel")
        self.Inputs.setWidget(16, QFormLayout.LabelRole, self.LeftDoorsLabel)
        self.LeftDoors = QCheckBox(self.gridLayoutWidget)
        self.LeftDoors.setObjectName("LeftDoors")
        self.Inputs.setWidget(16, QFormLayout.FieldRole, self.LeftDoors)
        # Row 17: Spacer
        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(17, QFormLayout.LabelRole, self.verticalSpacer_10)
        # Row 18: Right Doors
        self.RightDoorsLabel = QLabel(self.gridLayoutWidget)
        self.RightDoorsLabel.setObjectName("RightDoorsLabel")
        self.Inputs.setWidget(18, QFormLayout.LabelRole, self.RightDoorsLabel)
        self.RightDoors = QCheckBox(self.gridLayoutWidget)
        self.RightDoors.setObjectName("RightDoors")
        self.Inputs.setWidget(18, QFormLayout.FieldRole, self.RightDoors)
        # Row 19: Spacer
        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(19, QFormLayout.LabelRole, self.verticalSpacer_11)
        # Row 20: Emergency Stop and Train Driver
        self.EmergencyLabel = QLabel(self.gridLayoutWidget)
        self.EmergencyLabel.setObjectName("EmergencyStopLabel")
        self.Inputs.setWidget(20, QFormLayout.LabelRole, self.EmergencyLabel)
        self.EmergencyContainer = QWidget(self.gridLayoutWidget)
        self.horizontalLayout_Emergency = QHBoxLayout(self.EmergencyContainer)
        self.horizontalLayout_Emergency.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_Emergency.setObjectName("horizontalLayout_Emergency")
        self.EmergencyStop = QCheckBox(self.EmergencyContainer)
        self.EmergencyStop.setObjectName("EmergencyStop")
        self.horizontalLayout_Emergency.addWidget(self.EmergencyStop)
        self.TrainDriver = QCheckBox(self.EmergencyContainer)
        self.TrainDriver.setObjectName("TrainDriver")
        self.horizontalLayout_Emergency.addWidget(self.TrainDriver)
        self.Inputs.setWidget(20, QFormLayout.FieldRole, self.EmergencyContainer)
        # Row 21: Spacer
        self.verticalSpacer_31 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(21, QFormLayout.LabelRole, self.verticalSpacer_31)
        # Row 22: AC Signal (moved from Outputs)
        self.ACSignalLabel = QLabel(self.gridLayoutWidget)
        self.ACSignalLabel.setObjectName("ACSignalLabel")
        self.Inputs.setWidget(22, QFormLayout.LabelRole, self.ACSignalLabel)
        self.ACSignal = QCheckBox(self.gridLayoutWidget)
        self.ACSignal.setObjectName("ACSignal")
        self.Inputs.setWidget(22, QFormLayout.FieldRole, self.ACSignal)
        # Row 23: Spacer
        self.verticalSpacer_AC = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(23, QFormLayout.LabelRole, self.verticalSpacer_AC)
        # Row 24: Heating Signal (moved from Outputs)
        self.HeatingSignalLabel = QLabel(self.gridLayoutWidget)
        self.HeatingSignalLabel.setObjectName("HeatingSignalLabel")
        self.Inputs.setWidget(24, QFormLayout.LabelRole, self.HeatingSignalLabel)
        self.HeatingSignal = QCheckBox(self.gridLayoutWidget)
        self.HeatingSignal.setObjectName("HeatingSignal")
        self.Inputs.setWidget(24, QFormLayout.FieldRole, self.HeatingSignal)
        # Row 25: Spacer
        self.verticalSpacer_Heating = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(25, QFormLayout.LabelRole, self.verticalSpacer_Heating)
        # Row 26: Announcements
        self.AnnounementsLabel = QLabel(self.gridLayoutWidget)
        self.AnnounementsLabel.setObjectName("AnnounementsLabel")
        self.Inputs.setWidget(26, QFormLayout.LabelRole, self.AnnounementsLabel)
        self.Announcements = QLineEdit(self.gridLayoutWidget)
        self.Announcements.setObjectName("Announcements")
        self.Inputs.setWidget(26, QFormLayout.FieldRole, self.Announcements)
        # Row 27: Spacer
        self.verticalSpacer_29 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(27, QFormLayout.LabelRole, self.verticalSpacer_29)
        # Row 28: Length of Vehicle
        self.LengthVehicleLabel = QLabel(self.gridLayoutWidget)
        self.LengthVehicleLabel.setObjectName("LengthVehicleLabel")
        self.Inputs.setWidget(28, QFormLayout.LabelRole, self.LengthVehicleLabel)
        self.LengthVehicle = QLineEdit(self.gridLayoutWidget)
        self.LengthVehicle.setObjectName("LengthVehicle")
        self.Inputs.setWidget(28, QFormLayout.FieldRole, self.LengthVehicle)
        # Row 29: Spacer
        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(29, QFormLayout.LabelRole, self.verticalSpacer_12)
        # Row 30: Height of Vehicle
        self.HeightVehicleLabel = QLabel(self.gridLayoutWidget)
        self.HeightVehicleLabel.setObjectName("HeightVehicleLabel")
        self.Inputs.setWidget(30, QFormLayout.LabelRole, self.HeightVehicleLabel)
        self.HeightVehicle = QLineEdit(self.gridLayoutWidget)
        self.HeightVehicle.setObjectName("HeightVehicle")
        self.Inputs.setWidget(30, QFormLayout.FieldRole, self.HeightVehicle)
        # Row 31: Spacer
        self.verticalSpacer_23 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(31, QFormLayout.LabelRole, self.verticalSpacer_23)
        # Row 32: Width of Vehicle
        self.WidthVehicleLabel = QLabel(self.gridLayoutWidget)
        self.WidthVehicleLabel.setObjectName("WidthVehicleLabel")
        self.Inputs.setWidget(32, QFormLayout.LabelRole, self.WidthVehicleLabel)
        self.WidthVehicle = QLineEdit(self.gridLayoutWidget)
        self.WidthVehicle.setObjectName("WidthVehicle")
        self.Inputs.setWidget(32, QFormLayout.FieldRole, self.WidthVehicle)
        # Row 33: Spacer
        self.verticalSpacer_24 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(33, QFormLayout.LabelRole, self.verticalSpacer_24)
        # Row 34: Grade Percent
        self.GradePercentLabel = QLabel(self.gridLayoutWidget)
        self.GradePercentLabel.setObjectName("GradePercentLabel")
        self.Inputs.setWidget(34, QFormLayout.LabelRole, self.GradePercentLabel)
        self.GradePercent = QLineEdit(self.gridLayoutWidget)
        self.GradePercent.setObjectName("GradePercent")
        self.Inputs.setWidget(34, QFormLayout.FieldRole, self.GradePercent)
        # Row 35: Spacer
        self.verticalSpacer_25 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(35, QFormLayout.LabelRole, self.verticalSpacer_25)
        # Row 36: Mass of Vehicle
        self.MassVehicleLabel = QLabel(self.gridLayoutWidget)
        self.MassVehicleLabel.setObjectName("MassVehicleLabel")
        self.Inputs.setWidget(36, QFormLayout.LabelRole, self.MassVehicleLabel)
        self.MassVehicle = QLineEdit(self.gridLayoutWidget)
        self.MassVehicle.setObjectName("MassVehicle")
        self.Inputs.setWidget(36, QFormLayout.FieldRole, self.MassVehicle)
        # Row 37: Spacer
        self.verticalSpacer_26 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(37, QFormLayout.LabelRole, self.verticalSpacer_26)
        # Row 38: Passenger Count
        self.PassengerCountLabel = QLabel(self.gridLayoutWidget)
        self.PassengerCountLabel.setObjectName("PassengerCountLabel")
        self.Inputs.setWidget(38, QFormLayout.LabelRole, self.PassengerCountLabel)
        self.PassengerCount = QLineEdit(self.gridLayoutWidget)
        self.PassengerCount.setObjectName("PassengerCount")
        self.Inputs.setWidget(38, QFormLayout.FieldRole, self.PassengerCount)
        # Row 39: Spacer
        self.verticalSpacer_27 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(39, QFormLayout.LabelRole, self.verticalSpacer_27)
        # Row 40: Crew Count
        self.CrewCountLabel = QLabel(self.gridLayoutWidget)
        self.CrewCountLabel.setObjectName("CrewCountLabel")
        self.Inputs.setWidget(40, QFormLayout.LabelRole, self.CrewCountLabel)
        self.CrewCount = QLineEdit(self.gridLayoutWidget)
        self.CrewCount.setObjectName("CrewCount")
        self.Inputs.setWidget(40, QFormLayout.FieldRole, self.CrewCount)
        # Row 41: Spacer
        self.verticalSpacer_28 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.Inputs.setItem(41, QFormLayout.LabelRole, self.verticalSpacer_28)

        self.gridLayout.addLayout(self.Inputs, 1, 0, 1, 1)

        self.INPUTS = QLabel(self.gridLayoutWidget)
        self.INPUTS.setObjectName("INPUTS")
        self.INPUTS.setFont(font)
        self.INPUTS.setStyleSheet("background-color: rgb(151, 152, 119);")
        self.INPUTS.setFrameShape(QFrame.NoFrame)
        self.gridLayout.addWidget(self.INPUTS, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 732, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        # Outputs translations
        self.ActualVelocityLabel.setText(QCoreApplication.translate("MainWindow", "Actual Velocity (mph)", None))
        # self.SpeedLimitLabel_2.setText(QCoreApplication.translate("MainWindow", "Speed Limit (mph)", None))
        self.WaysideSpeedLabel_2.setText(QCoreApplication.translate("MainWindow", "Wayside Speed (mph)", None))
        self.WaysideAuthorityLabel_2.setText(QCoreApplication.translate("MainWindow", "Wayside Authority (feet)", None))
        self.PEmergencyStopLabel.setText(QCoreApplication.translate("MainWindow", "Passenger Emergency Stop", None))
        self.SignalFailureLabel.setText(QCoreApplication.translate("MainWindow", "Signal Failure (bool)", None))
        self.BrakeFailureLabel.setText(QCoreApplication.translate("MainWindow", "Brake Failure (bool)", None))
        self.EngineFailureLabel.setText(QCoreApplication.translate("MainWindow", "Enginer Failure (bool)", None))
        self.TemperatureLabel.setText(QCoreApplication.translate("MainWindow", "Temperature", None))
        # Inputs translations
        self.WaysideSpeedLabel.setText(QCoreApplication.translate("MainWindow", "Wayside Speed (mph)", None))
        self.WaysideAuthorityLabel.setText(QCoreApplication.translate("MainWindow", "Wayside Authority (yard)", None))
        self.CommandedPowerLabel.setText(QCoreApplication.translate("MainWindow", "Commanded Power (W)", None))
        # self.SpeedLimitLabel.setText(QCoreApplication.translate("MainWindow", "Speed Limit (mph)", None))
        self.BeaconDataLabel.setText(QCoreApplication.translate("MainWindow", "Beacon Data (128 Bytes)", None))
        self.ServiceBrakesLabel.setText(QCoreApplication.translate("MainWindow", "Service Brakes", None))
        self.ExtLightsLabel.setText(QCoreApplication.translate("MainWindow", "Exterior Lights (bool)", None))
        self.IntLightsLabel.setText(QCoreApplication.translate("MainWindow", "Interior Lights (bool)", None))
        self.LeftDoorsLabel.setText(QCoreApplication.translate("MainWindow", "Left Doors", None))
        self.RightDoorsLabel.setText(QCoreApplication.translate("MainWindow", "Right Doors", None))
        self.EmergencyLabel.setText(QCoreApplication.translate("MainWindow", "Emergency Stop (bool)", None))
        self.ACSignalLabel.setText(QCoreApplication.translate("MainWindow", "Air Conditioning Signal (bool)", None))
        self.HeatingSignalLabel.setText(QCoreApplication.translate("MainWindow", "Heating Signal (bool)", None))
        self.AnnounementsLabel.setText(QCoreApplication.translate("MainWindow", "Announcements", None))
        self.LengthVehicleLabel.setText(QCoreApplication.translate("MainWindow", "Length of Vehicle (ft)", None))
        self.HeightVehicleLabel.setText(QCoreApplication.translate("MainWindow", "Height of Vehicle (ft)", None))
        self.WidthVehicleLabel.setText(QCoreApplication.translate("MainWindow", "Width of Vehicle (ft)", None))
        self.GradePercentLabel.setText(QCoreApplication.translate("MainWindow", "Grade (%)", None))
        self.MassVehicleLabel.setText(QCoreApplication.translate("MainWindow", "Mass of Vehicle (lb)", None))
        self.PassengerCountLabel.setText(QCoreApplication.translate("MainWindow", "Passeneger Count", None))
        self.CrewCountLabel.setText(QCoreApplication.translate("MainWindow", "Crew Count", None))
        # Checkboxes
        self.ExtLights.setText(QCoreApplication.translate("MainWindow", "ENABLE", None))
        self.IntLights.setText(QCoreApplication.translate("MainWindow", "ENABLE", None))
        self.LeftDoors.setText(QCoreApplication.translate("MainWindow", "ENABLE", None))
        self.RightDoors.setText(QCoreApplication.translate("MainWindow", "ENABLE", None))
        self.ServiceBrakes.setText(QCoreApplication.translate("MainWindow", "ENABLE", None))
        self.EmergencyStop.setText(QCoreApplication.translate("MainWindow", "DISABLE", None))
        self.TrainDriver.setText(QCoreApplication.translate("MainWindow", "TRAIN DRIVER", None))
        self.ACSignal.setText(QCoreApplication.translate("MainWindow", "ENABLE", None))
        self.HeatingSignal.setText(QCoreApplication.translate("MainWindow", "ENABLE", None))
        self.OUTPUTS.setText(QCoreApplication.translate("MainWindow", "OUTPUTS", None))
        self.INPUTS.setText(QCoreApplication.translate("MainWindow", "INPUTS", None))

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_TestMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
