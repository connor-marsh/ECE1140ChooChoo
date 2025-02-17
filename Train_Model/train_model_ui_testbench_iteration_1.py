# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TrainModel_UI_TestBench_Iteration_1.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore

# from PyQt5.QtCore import *  # type: ignore
# from PyQt5.QtGui import *  # type: ignore
# from PyQt5.QtWidgets import *  # type: ignore

import os
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class Ui_TestMainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(732, 833)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(30, 10, 671, 771))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.Outputs = QFormLayout()
        self.Outputs.setObjectName(u"Outputs")
        self.ActualVelocityLabel = QLabel(self.gridLayoutWidget)
        self.ActualVelocityLabel.setObjectName(u"ActualVelocityLabel")

        self.Outputs.setWidget(0, QFormLayout.LabelRole, self.ActualVelocityLabel)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(1, QFormLayout.LabelRole, self.verticalSpacer_13)

        self.SpeedLimitLabel_2 = QLabel(self.gridLayoutWidget)
        self.SpeedLimitLabel_2.setObjectName(u"SpeedLimitLabel_2")

        self.Outputs.setWidget(2, QFormLayout.LabelRole, self.SpeedLimitLabel_2)

        self.verticalSpacer_14 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(3, QFormLayout.LabelRole, self.verticalSpacer_14)

        self.WaysideSpeedLabel_2 = QLabel(self.gridLayoutWidget)
        self.WaysideSpeedLabel_2.setObjectName(u"WaysideSpeedLabel_2")

        self.Outputs.setWidget(4, QFormLayout.LabelRole, self.WaysideSpeedLabel_2)

        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(5, QFormLayout.LabelRole, self.verticalSpacer_15)

        self.WaysideAuthorityLabel_2 = QLabel(self.gridLayoutWidget)
        self.WaysideAuthorityLabel_2.setObjectName(u"WaysideAuthorityLabel_2")

        self.Outputs.setWidget(6, QFormLayout.LabelRole, self.WaysideAuthorityLabel_2)

        self.verticalSpacer_16 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(7, QFormLayout.LabelRole, self.verticalSpacer_16)

        self.PEmergencyStopLabel = QLabel(self.gridLayoutWidget)
        self.PEmergencyStopLabel.setObjectName(u"PEmergencyStopLabel")

        self.Outputs.setWidget(8, QFormLayout.LabelRole, self.PEmergencyStopLabel)

        self.verticalSpacer_17 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(9, QFormLayout.LabelRole, self.verticalSpacer_17)

        self.SignalFailureLabel = QLabel(self.gridLayoutWidget)
        self.SignalFailureLabel.setObjectName(u"SignalFailureLabel")

        self.Outputs.setWidget(10, QFormLayout.LabelRole, self.SignalFailureLabel)

        self.verticalSpacer_18 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(11, QFormLayout.LabelRole, self.verticalSpacer_18)

        self.BrakeFailureLabel = QLabel(self.gridLayoutWidget)
        self.BrakeFailureLabel.setObjectName(u"BrakeFailureLabel")

        self.Outputs.setWidget(12, QFormLayout.LabelRole, self.BrakeFailureLabel)

        self.verticalSpacer_19 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(13, QFormLayout.LabelRole, self.verticalSpacer_19)

        self.EngineFailureLabel = QLabel(self.gridLayoutWidget)
        self.EngineFailureLabel.setObjectName(u"EngineFailureLabel")

        self.Outputs.setWidget(14, QFormLayout.LabelRole, self.EngineFailureLabel)

        self.verticalSpacer_20 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(15, QFormLayout.LabelRole, self.verticalSpacer_20)

        self.ACSignalLabel = QLabel(self.gridLayoutWidget)
        self.ACSignalLabel.setObjectName(u"ACSignalLabel")

        self.Outputs.setWidget(16, QFormLayout.LabelRole, self.ACSignalLabel)

        self.verticalSpacer_21 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(17, QFormLayout.LabelRole, self.verticalSpacer_21)

        self.HeatingSignalLabel = QLabel(self.gridLayoutWidget)
        self.HeatingSignalLabel.setObjectName(u"HeatingSignalLabel")

        self.Outputs.setWidget(18, QFormLayout.LabelRole, self.HeatingSignalLabel)

        self.verticalSpacer_22 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Outputs.setItem(19, QFormLayout.LabelRole, self.verticalSpacer_22)

        self.ActualVelocity = QLabel(self.gridLayoutWidget)
        self.ActualVelocity.setObjectName(u"ActualVelocity")

        self.Outputs.setWidget(0, QFormLayout.FieldRole, self.ActualVelocity)

        self.SpeedLimit_2 = QLabel(self.gridLayoutWidget)
        self.SpeedLimit_2.setObjectName(u"SpeedLimit_2")

        self.Outputs.setWidget(2, QFormLayout.FieldRole, self.SpeedLimit_2)

        self.WaysideSpeed_2 = QLabel(self.gridLayoutWidget)
        self.WaysideSpeed_2.setObjectName(u"WaysideSpeed_2")

        self.Outputs.setWidget(4, QFormLayout.FieldRole, self.WaysideSpeed_2)

        self.WaysideAuthority_2 = QLabel(self.gridLayoutWidget)
        self.WaysideAuthority_2.setObjectName(u"WaysideAuthority_2")

        self.Outputs.setWidget(6, QFormLayout.FieldRole, self.WaysideAuthority_2)

        self.PEmergencyStop = QLabel(self.gridLayoutWidget)
        self.PEmergencyStop.setObjectName(u"PEmergencyStop")

        self.Outputs.setWidget(8, QFormLayout.FieldRole, self.PEmergencyStop)

        self.SignalFailure = QLabel(self.gridLayoutWidget)
        self.SignalFailure.setObjectName(u"SignalFailure")

        self.Outputs.setWidget(10, QFormLayout.FieldRole, self.SignalFailure)

        self.BrakeFailure = QLabel(self.gridLayoutWidget)
        self.BrakeFailure.setObjectName(u"BrakeFailure")

        self.Outputs.setWidget(12, QFormLayout.FieldRole, self.BrakeFailure)

        self.EngineFailure = QLabel(self.gridLayoutWidget)
        self.EngineFailure.setObjectName(u"EngineFailure")

        self.Outputs.setWidget(14, QFormLayout.FieldRole, self.EngineFailure)

        self.ACSignal = QCheckBox(self.gridLayoutWidget)
        self.ACSignal.setObjectName(u"ACSignal")

        self.Outputs.setWidget(16, QFormLayout.FieldRole, self.ACSignal)

        self.HeatingSignal = QCheckBox(self.gridLayoutWidget)
        self.HeatingSignal.setObjectName(u"HeatingSignal")

        self.Outputs.setWidget(18, QFormLayout.FieldRole, self.HeatingSignal)


        self.gridLayout.addLayout(self.Outputs, 1, 1, 1, 1)

        self.OUTPUTS = QLabel(self.gridLayoutWidget)
        self.OUTPUTS.setObjectName(u"OUTPUTS")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.OUTPUTS.setFont(font)
        self.OUTPUTS.setStyleSheet(u"background-color: rgb(151, 152, 119);")

        self.gridLayout.addWidget(self.OUTPUTS, 0, 1, 1, 1)

        self.Inputs = QFormLayout()
        self.Inputs.setObjectName(u"Inputs")
        self.WaysideSpeedLabel = QLabel(self.gridLayoutWidget)
        self.WaysideSpeedLabel.setObjectName(u"WaysideSpeedLabel")

        self.Inputs.setWidget(0, QFormLayout.LabelRole, self.WaysideSpeedLabel)

        self.WaysideSpeed = QLineEdit(self.gridLayoutWidget)
        self.WaysideSpeed.setObjectName(u"WaysideSpeed")

        self.Inputs.setWidget(0, QFormLayout.FieldRole, self.WaysideSpeed)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(1, QFormLayout.LabelRole, self.verticalSpacer)

        self.WaysideAuthorityLabel = QLabel(self.gridLayoutWidget)
        self.WaysideAuthorityLabel.setObjectName(u"WaysideAuthorityLabel")

        self.Inputs.setWidget(2, QFormLayout.LabelRole, self.WaysideAuthorityLabel)

        self.WaysideAuthority = QLineEdit(self.gridLayoutWidget)
        self.WaysideAuthority.setObjectName(u"WaysideAuthority")

        self.Inputs.setWidget(2, QFormLayout.FieldRole, self.WaysideAuthority)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(3, QFormLayout.LabelRole, self.verticalSpacer_2)

        self.CommandedPowerLabel = QLabel(self.gridLayoutWidget)
        self.CommandedPowerLabel.setObjectName(u"CommandedPowerLabel")

        self.Inputs.setWidget(4, QFormLayout.LabelRole, self.CommandedPowerLabel)

        self.CommandedPower = QLineEdit(self.gridLayoutWidget)
        self.CommandedPower.setObjectName(u"CommandedPower")

        self.Inputs.setWidget(4, QFormLayout.FieldRole, self.CommandedPower)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(5, QFormLayout.LabelRole, self.verticalSpacer_5)

        self.SpeedLimitLabel = QLabel(self.gridLayoutWidget)
        self.SpeedLimitLabel.setObjectName(u"SpeedLimitLabel")

        self.Inputs.setWidget(6, QFormLayout.LabelRole, self.SpeedLimitLabel)

        self.SpeedLimit = QLineEdit(self.gridLayoutWidget)
        self.SpeedLimit.setObjectName(u"SpeedLimit")

        self.Inputs.setWidget(6, QFormLayout.FieldRole, self.SpeedLimit)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(7, QFormLayout.LabelRole, self.verticalSpacer_8)

        self.BeaconData = QLineEdit(self.gridLayoutWidget)
        self.BeaconData.setObjectName(u"BeaconData")

        self.Inputs.setWidget(8, QFormLayout.FieldRole, self.BeaconData)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(9, QFormLayout.LabelRole, self.verticalSpacer_7)

        self.ExtLightsLabel = QLabel(self.gridLayoutWidget)
        self.ExtLightsLabel.setObjectName(u"ExtLightsLabel")

        self.Inputs.setWidget(12, QFormLayout.LabelRole, self.ExtLightsLabel)

        self.ExtLights = QCheckBox(self.gridLayoutWidget)
        self.ExtLights.setObjectName(u"ExtLights")

        self.Inputs.setWidget(12, QFormLayout.FieldRole, self.ExtLights)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(13, QFormLayout.LabelRole, self.verticalSpacer_6)

        self.IntLightsLabel = QLabel(self.gridLayoutWidget)
        self.IntLightsLabel.setObjectName(u"IntLightsLabel")

        self.Inputs.setWidget(14, QFormLayout.LabelRole, self.IntLightsLabel)

        self.IntLights = QCheckBox(self.gridLayoutWidget)
        self.IntLights.setObjectName(u"IntLights")

        self.Inputs.setWidget(14, QFormLayout.FieldRole, self.IntLights)

        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(15, QFormLayout.LabelRole, self.verticalSpacer_9)

        self.LeftDoorsLabel = QLabel(self.gridLayoutWidget)
        self.LeftDoorsLabel.setObjectName(u"LeftDoorsLabel")

        self.Inputs.setWidget(16, QFormLayout.LabelRole, self.LeftDoorsLabel)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(17, QFormLayout.LabelRole, self.verticalSpacer_10)

        self.RightDoorsLabel = QLabel(self.gridLayoutWidget)
        self.RightDoorsLabel.setObjectName(u"RightDoorsLabel")

        self.Inputs.setWidget(18, QFormLayout.LabelRole, self.RightDoorsLabel)

        self.verticalSpacer_11 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(19, QFormLayout.LabelRole, self.verticalSpacer_11)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.Inputs.setItem(22, QFormLayout.SpanningRole, self.horizontalSpacer)

        self.AnnounementsLabel = QLabel(self.gridLayoutWidget)
        self.AnnounementsLabel.setObjectName(u"AnnounementsLabel")

        self.Inputs.setWidget(23, QFormLayout.LabelRole, self.AnnounementsLabel)

        self.Announcements = QLineEdit(self.gridLayoutWidget)
        self.Announcements.setObjectName(u"Announcements")

        self.Inputs.setWidget(23, QFormLayout.FieldRole, self.Announcements)

        self.verticalSpacer_29 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(24, QFormLayout.LabelRole, self.verticalSpacer_29)

        self.LengthVehicleLabel = QLabel(self.gridLayoutWidget)
        self.LengthVehicleLabel.setObjectName(u"LengthVehicleLabel")

        self.Inputs.setWidget(25, QFormLayout.LabelRole, self.LengthVehicleLabel)

        self.LengthVehicle = QLineEdit(self.gridLayoutWidget)
        self.LengthVehicle.setObjectName(u"LengthVehicle")

        self.Inputs.setWidget(25, QFormLayout.FieldRole, self.LengthVehicle)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(26, QFormLayout.LabelRole, self.verticalSpacer_12)

        self.HeightVehicleLabel = QLabel(self.gridLayoutWidget)
        self.HeightVehicleLabel.setObjectName(u"HeightVehicleLabel")

        self.Inputs.setWidget(27, QFormLayout.LabelRole, self.HeightVehicleLabel)

        self.HeightVehicle = QLineEdit(self.gridLayoutWidget)
        self.HeightVehicle.setObjectName(u"HeightVehicle")

        self.Inputs.setWidget(27, QFormLayout.FieldRole, self.HeightVehicle)

        self.verticalSpacer_23 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(28, QFormLayout.LabelRole, self.verticalSpacer_23)

        self.WidthVehicleLabel = QLabel(self.gridLayoutWidget)
        self.WidthVehicleLabel.setObjectName(u"WidthVehicleLabel")

        self.Inputs.setWidget(29, QFormLayout.LabelRole, self.WidthVehicleLabel)

        self.WidthVehicle = QLineEdit(self.gridLayoutWidget)
        self.WidthVehicle.setObjectName(u"WidthVehicle")

        self.Inputs.setWidget(29, QFormLayout.FieldRole, self.WidthVehicle)

        self.verticalSpacer_24 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(30, QFormLayout.LabelRole, self.verticalSpacer_24)

        self.GradePercentLabel = QLabel(self.gridLayoutWidget)
        self.GradePercentLabel.setObjectName(u"GradePercentLabel")

        self.Inputs.setWidget(31, QFormLayout.LabelRole, self.GradePercentLabel)

        self.GradePercent = QLineEdit(self.gridLayoutWidget)
        self.GradePercent.setObjectName(u"GradePercent")

        self.Inputs.setWidget(31, QFormLayout.FieldRole, self.GradePercent)

        self.verticalSpacer_25 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(32, QFormLayout.LabelRole, self.verticalSpacer_25)

        self.MassVehicleLabel = QLabel(self.gridLayoutWidget)
        self.MassVehicleLabel.setObjectName(u"MassVehicleLabel")

        self.Inputs.setWidget(33, QFormLayout.LabelRole, self.MassVehicleLabel)

        self.MassVehicle = QLineEdit(self.gridLayoutWidget)
        self.MassVehicle.setObjectName(u"MassVehicle")

        self.Inputs.setWidget(33, QFormLayout.FieldRole, self.MassVehicle)

        self.verticalSpacer_26 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(34, QFormLayout.LabelRole, self.verticalSpacer_26)

        self.PassengerCountLabel = QLabel(self.gridLayoutWidget)
        self.PassengerCountLabel.setObjectName(u"PassengerCountLabel")

        self.Inputs.setWidget(35, QFormLayout.LabelRole, self.PassengerCountLabel)

        self.PassengerCount = QLineEdit(self.gridLayoutWidget)
        self.PassengerCount.setObjectName(u"PassengerCount")

        self.Inputs.setWidget(35, QFormLayout.FieldRole, self.PassengerCount)

        self.verticalSpacer_27 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(36, QFormLayout.LabelRole, self.verticalSpacer_27)

        self.CrewCountLabel = QLabel(self.gridLayoutWidget)
        self.CrewCountLabel.setObjectName(u"CrewCountLabel")

        self.Inputs.setWidget(37, QFormLayout.LabelRole, self.CrewCountLabel)

        self.CrewCount = QLineEdit(self.gridLayoutWidget)
        self.CrewCount.setObjectName(u"CrewCount")

        self.Inputs.setWidget(37, QFormLayout.FieldRole, self.CrewCount)

        self.verticalSpacer_28 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(38, QFormLayout.LabelRole, self.verticalSpacer_28)

        self.BeaconDataLabel = QLabel(self.gridLayoutWidget)
        self.BeaconDataLabel.setObjectName(u"BeaconDataLabel")

        self.Inputs.setWidget(8, QFormLayout.LabelRole, self.BeaconDataLabel)

        self.LeftDoors = QCheckBox(self.gridLayoutWidget)
        self.LeftDoors.setObjectName(u"LeftDoors")

        self.Inputs.setWidget(16, QFormLayout.FieldRole, self.LeftDoors)

        self.RightDoors = QCheckBox(self.gridLayoutWidget)
        self.RightDoors.setObjectName(u"RightDoors")

        self.Inputs.setWidget(18, QFormLayout.FieldRole, self.RightDoors)

        self.ServiceBrakesLabel = QLabel(self.gridLayoutWidget)
        self.ServiceBrakesLabel.setObjectName(u"ServiceBrakesLabel")

        self.Inputs.setWidget(10, QFormLayout.LabelRole, self.ServiceBrakesLabel)

        self.ServiceBrakes = QCheckBox(self.gridLayoutWidget)
        self.ServiceBrakes.setObjectName(u"ServiceBrakes")

        self.Inputs.setWidget(10, QFormLayout.FieldRole, self.ServiceBrakes)

        self.verticalSpacer_30 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(11, QFormLayout.LabelRole, self.verticalSpacer_30)

        self.EmergencyLabel = QLabel(self.gridLayoutWidget)
        self.EmergencyLabel.setObjectName(u"EmergencyStopLabel")

        self.Inputs.setWidget(20, QFormLayout.LabelRole, self.EmergencyLabel)

        self.EmergencyStop = QCheckBox(self.gridLayoutWidget)
        self.EmergencyStop.setObjectName(u"EmergencyStop")

        self.Inputs.setWidget(20, QFormLayout.FieldRole, self.EmergencyStop)

        self.verticalSpacer_31 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.Inputs.setItem(21, QFormLayout.LabelRole, self.verticalSpacer_31)


        self.gridLayout.addLayout(self.Inputs, 1, 0, 1, 1)

        self.INPUTS = QLabel(self.gridLayoutWidget)
        self.INPUTS.setObjectName(u"INPUTS")
        self.INPUTS.setFont(font)
        self.INPUTS.setStyleSheet(u"background-color: rgb(151, 152, 119);")
        self.INPUTS.setFrameShape(QFrame.NoFrame)

        self.gridLayout.addWidget(self.INPUTS, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 732, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.ActualVelocityLabel.setText(QCoreApplication.translate("MainWindow", u"Actual Velocity (mph)", None))
        self.SpeedLimitLabel_2.setText(QCoreApplication.translate("MainWindow", u"Speed Limit (mph)", None))
        self.WaysideSpeedLabel_2.setText(QCoreApplication.translate("MainWindow", u"Wayside Speed (mph)", None))
        self.WaysideAuthorityLabel_2.setText(QCoreApplication.translate("MainWindow", u"Wayside Authority (feet)", None))
        self.PEmergencyStopLabel.setText(QCoreApplication.translate("MainWindow", u"Passenger Emergency Stop", None))
        self.SignalFailureLabel.setText(QCoreApplication.translate("MainWindow", u"Signal Failure (bool)", None))
        self.BrakeFailureLabel.setText(QCoreApplication.translate("MainWindow", u"Brake Failure (bool)", None))
        self.EngineFailureLabel.setText(QCoreApplication.translate("MainWindow", u"Enginer Failure (bool)", None))
        self.ACSignalLabel.setText(QCoreApplication.translate("MainWindow", u"Air Conditioning Signal (bool)", None))
        self.HeatingSignalLabel.setText(QCoreApplication.translate("MainWindow", u"Heating Signal (bool)", None))
        self.ActualVelocity.setText(QCoreApplication.translate("MainWindow", u"Displayed?", None))
        self.SpeedLimit_2.setText(QCoreApplication.translate("MainWindow", u"Displayed?", None))
        self.WaysideSpeed_2.setText(QCoreApplication.translate("MainWindow", u"Displayed?", None))
        self.WaysideAuthority_2.setText(QCoreApplication.translate("MainWindow", u"Displayed?", None))
        self.PEmergencyStop.setText(QCoreApplication.translate("MainWindow", u"Displayed?", None))
        self.SignalFailure.setText(QCoreApplication.translate("MainWindow", u"Displayed?", None))
        self.BrakeFailure.setText(QCoreApplication.translate("MainWindow", u"Displayed?", None))
        self.EngineFailure.setText(QCoreApplication.translate("MainWindow", u"Displayed?", None))
        self.ACSignal.setText(QCoreApplication.translate("MainWindow", u"ENABLE", None))
        self.HeatingSignal.setText(QCoreApplication.translate("MainWindow", u"ENABLE", None))
        self.OUTPUTS.setText(QCoreApplication.translate("MainWindow", u"OUTPUTS", None))
        self.WaysideSpeedLabel.setText(QCoreApplication.translate("MainWindow", u"Wayside Speed (m/s)", None))
        self.WaysideAuthorityLabel.setText(QCoreApplication.translate("MainWindow", u"Wayside Authority (m)", None))
        self.CommandedPowerLabel.setText(QCoreApplication.translate("MainWindow", u"Commanded Power (W)", None))
        self.SpeedLimitLabel.setText(QCoreApplication.translate("MainWindow", u"Speed Limit (m/s)", None))
        self.ExtLightsLabel.setText(QCoreApplication.translate("MainWindow", u"Exterior Lights (bool)", None))
        self.ExtLights.setText(QCoreApplication.translate("MainWindow", u"ENABLE", None))
        self.IntLightsLabel.setText(QCoreApplication.translate("MainWindow", u"Interior Lights (bool)", None))
        self.IntLights.setText(QCoreApplication.translate("MainWindow", u"ENABLE", None))
        self.LeftDoorsLabel.setText(QCoreApplication.translate("MainWindow", u"Left Doors", None))
        self.RightDoorsLabel.setText(QCoreApplication.translate("MainWindow", u"Right Doors", None))
        self.AnnounementsLabel.setText(QCoreApplication.translate("MainWindow", u"Announcements", None))
        self.LengthVehicleLabel.setText(QCoreApplication.translate("MainWindow", u"Length of Vehicle (m)", None))
        self.HeightVehicleLabel.setText(QCoreApplication.translate("MainWindow", u"Height of Vehicle (m)", None))
        self.WidthVehicleLabel.setText(QCoreApplication.translate("MainWindow", u"Width of Vehicle (m)", None))
        self.GradePercentLabel.setText(QCoreApplication.translate("MainWindow", u"Grade (%)", None))
        self.MassVehicleLabel.setText(QCoreApplication.translate("MainWindow", u"Mass of Vehicle (t)", None))
        self.PassengerCountLabel.setText(QCoreApplication.translate("MainWindow", u"Passeneger Count", None))
        self.CrewCountLabel.setText(QCoreApplication.translate("MainWindow", u"Crew Count", None))
        self.BeaconDataLabel.setText(QCoreApplication.translate("MainWindow", u"Beacon Data (128 Bytes)", None))
        self.LeftDoors.setText(QCoreApplication.translate("MainWindow", u"ENABLE", None))
        self.RightDoors.setText(QCoreApplication.translate("MainWindow", u"ENABLE", None))
        self.ServiceBrakesLabel.setText(QCoreApplication.translate("MainWindow", u"Service Brakes", None))
        self.ServiceBrakes.setText(QCoreApplication.translate("MainWindow", u"ENABLE", None))
        self.EmergencyLabel.setText(QCoreApplication.translate("MainWindow", u"Emergency Stop (bool)", None))
        self.EmergencyStop.setText(QCoreApplication.translate("MainWindow", u"DISABLE", None))
        self.INPUTS.setText(QCoreApplication.translate("MainWindow", u"INPUTS", None))
    # retranslateUi

# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     MainWindow = QMainWindow()
#     ui = Ui_TestMainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())