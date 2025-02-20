# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TrainModel_UI_Iteration_1'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore

# from PyQt5.QtCore import *  # type: ignore
# from PyQt5.QtGui import *  # type: ignore
# from PyQt5.QtWidgets import *  # type: ignore

import os
os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(710, 655)
        font = QFont()
        font.setPointSize(8)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"")
        self.Main = QWidget(MainWindow)
        self.Main.setObjectName(u"Main")
        font1 = QFont()
        font1.setPointSize(8)
        font1.setBold(True)
        font1.setWeight(75)
        self.Main.setFont(font1)
        self.FailureBox = QGroupBox(self.Main)
        self.FailureBox.setObjectName(u"FailureBox")
        self.FailureBox.setGeometry(QRect(10, 140, 241, 251))
        font2 = QFont()
        font2.setPointSize(13)
        font2.setBold(True)
        font2.setWeight(75)
        self.FailureBox.setFont(font2)
        self.FailureBox.setAutoFillBackground(True)
        self.FailureBox.setStyleSheet(u"")
        self.FailureBox.setFlat(False)
        self.FailBrake = QLabel(self.FailureBox)
        self.FailBrake.setObjectName(u"FailBrake")
        self.FailBrake.setGeometry(QRect(10, 30, 121, 63))
        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(True)
        font3.setWeight(75)
        self.FailBrake.setFont(font3)
        self.FailBrake.setStyleSheet(u"background-color: rgb(254, 53, 53);")
        self.FailBrake.setFrameShape(QFrame.WinPanel)
        self.FailBrake.setFrameShadow(QFrame.Sunken)
        self.FailBrake.setIndent(6)
        self.Enabled1 = QPushButton(self.FailureBox)
        self.Enabled1.setObjectName(u"Enabled1")
        self.Enabled1.setGeometry(QRect(140, 30, 91, 31))
        font4 = QFont()
        font4.setBold(True)
        font4.setWeight(75)
        self.Enabled1.setFont(font4)
        self.Enabled1.setStyleSheet(
                u"""
                QPushButton#Enabled1 {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #6eff66, stop:1 #1e7d1e); /* Light-to-dark green */
                color: black;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #1e7d1e;
                border-radius: 10px;
                padding: 6px;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Raised effect */
                transition: background 0.3s ease;
                }

                /* Pressed momentarily */
                QPushButton#Enabled1:pressed {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #00cc00, stop:1 #006600);
                border: 2px solid #004d00;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Shadow appears inset when pressed */
                }

                /* Toggled on (latched) */
                QPushButton#Enabled1:checked {
                /* Any distinct style to show the button is latched on */
                background-color: #006600;
                border: 2px solid #004d00;
                }
                """
)
        self.Enabled1.setFlat(False)
        self.Disabled1 = QPushButton(self.FailureBox)
        self.Disabled1.setObjectName(u"Disabled1")
        self.Disabled1.setGeometry(QRect(140, 62, 91, 31))
        font5 = QFont()
        font5.setBold(True)
        font5.setWeight(75)
        font5.setStrikeOut(False)
        self.Disabled1.setFont(font5)
        self.Disabled1.setStyleSheet(
                u"""
                QPushButton#Disabled1 {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #ff6a6c, stop:1 #d33032);
                color: black;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #d33032;
                border-radius: 10px;
                padding: 6px;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);
                transition: background 0.3s ease;
                }

                /* Pressed momentarily for #Disabled1 specifically */
                QPushButton#Disabled1:pressed {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #e84547, stop:1 #9c1e1f);
                border: 2px solid #7a1c1d;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
                }

                /* Toggled (latched) ON style for #Disabled1 */
                QPushButton#Disabled1:checked {
                background-color: #cc0000;
                border: 2px solid #7a1c1d;
                }
                """
)
        self.Disabled1.setFlat(False)
        self.FailSignal = QLabel(self.FailureBox)
        self.FailSignal.setObjectName(u"FailSignal")
        self.FailSignal.setGeometry(QRect(10, 100, 121, 63))
        self.FailSignal.setFont(font3)
        self.FailSignal.setStyleSheet(u"background-color: rgb(254, 53, 53);")
        self.FailSignal.setFrameShape(QFrame.WinPanel)
        self.FailSignal.setFrameShadow(QFrame.Sunken)
        self.FailSignal.setIndent(6)
        self.FailEngine = QLabel(self.FailureBox)
        self.FailEngine.setObjectName(u"FailEngine")
        self.FailEngine.setGeometry(QRect(10, 170, 121, 63))
        self.FailEngine.setFont(font3)
        self.FailEngine.setStyleSheet(u"background-color: rgb(254, 53, 53);")
        self.FailEngine.setFrameShape(QFrame.WinPanel)
        self.FailEngine.setFrameShadow(QFrame.Sunken)
        self.FailEngine.setIndent(3)
        self.Enabled2 = QPushButton(self.FailureBox)
        self.Enabled2.setObjectName(u"Enabled2")
        self.Enabled2.setGeometry(QRect(140, 100, 91, 31))
        font6 = QFont()
        font6.setBold(True)
        font6.setWeight(75)
        font6.setKerning(True)
        self.Enabled2.setFont(font6)
        self.Enabled2.setStyleSheet(
                u"""
                QPushButton#Enabled2 {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #6eff66, stop:1 #1e7d1e); /* Light-to-dark green */
                color: black;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #1e7d1e;
                border-radius: 10px;
                padding: 6px;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Raised effect */
                transition: background 0.3s ease;
                }

                /* Pressed momentarily */
                QPushButton#Enabled2:pressed {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #00cc00, stop:1 #006600);
                border: 2px solid #004d00;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Shadow appears inset when pressed */
                }

                /* Toggled on (latched) */
                QPushButton#Enabled2:checked {
                /* Any distinct style to show the button is latched on */
                background-color: #006600;
                border: 2px solid #004d00;
                }
                """
)
        self.Enabled2.setFlat(False)
        self.Disabled2 = QPushButton(self.FailureBox)
        self.Disabled2.setObjectName(u"Disabled2")
        self.Disabled2.setGeometry(QRect(140, 132, 91, 31))
        self.Disabled2.setFont(font5)
        self.Disabled2.setStyleSheet(
                u"""
                QPushButton#Disabled2 {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #ff6a6c, stop:1 #d33032);
                color: black;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #d33032;
                border-radius: 10px;
                padding: 6px;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);
                transition: background 0.3s ease;
                }

                /* Pressed momentarily for #Disabled1 specifically */
                QPushButton#Disabled2:pressed {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #e84547, stop:1 #9c1e1f);
                border: 2px solid #7a1c1d;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
                }

                /* Toggled (latched) ON style for #Disabled1 */
                QPushButton#Disabled2:checked {
                background-color: #cc0000;
                border: 2px solid #7a1c1d;
                }
                """
)
        self.Disabled2.setFlat(False)
        self.Enabled3 = QPushButton(self.FailureBox)
        self.Enabled3.setObjectName(u"Enabled3")
        self.Enabled3.setGeometry(QRect(140, 170, 91, 31))
        self.Enabled3.setFont(font4)
        self.Enabled3.setStyleSheet(
                u"""
                QPushButton#Enabled3 {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #6eff66, stop:1 #1e7d1e); /* Light-to-dark green */
                color: black;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #1e7d1e;
                border-radius: 10px;
                padding: 6px;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5); /* Raised effect */
                transition: background 0.3s ease;
                }

                /* Pressed momentarily */
                QPushButton#Enabled3:pressed {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #00cc00, stop:1 #006600);
                border: 2px solid #004d00;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7); /* Shadow appears inset when pressed */
                }

                /* Toggled on (latched) */
                QPushButton#Enabled3:checked {
                /* Any distinct style to show the button is latched on */
                background-color: #006600;
                border: 2px solid #004d00;
                }
                """
)
        self.Enabled3.setFlat(False)
        self.Disabled3 = QPushButton(self.FailureBox)
        self.Disabled3.setObjectName(u"Disabled3")
        self.Disabled3.setGeometry(QRect(140, 202, 91, 31))
        self.Disabled3.setFont(font5)
        self.Disabled3.setStyleSheet(
                u"""
                QPushButton#Disabled3 {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #ff6a6c, stop:1 #d33032);
                color: black;
                font-size: 16px;
                font-weight: bold;
                border: 2px solid #d33032;
                border-radius: 10px;
                padding: 6px;
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);
                transition: background 0.3s ease;
                }

                /* Pressed momentarily for #Disabled1 specifically */
                QPushButton#Disabled3:pressed {
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1, 
                                                stop:0 #e84547, stop:1 #9c1e1f);
                border: 2px solid #7a1c1d;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.7);
                }

                /* Toggled (latched) ON style for #Disabled1 */
                QPushButton#Disabled3:checked {
                background-color: #cc0000;
                border: 2px solid #7a1c1d;
                }
                """
)
        self.Disabled3.setFlat(False)
        self.Advertisements = QLabel(self.Main)
        self.Advertisements.setObjectName(u"Advertisements")
        self.Advertisements.setPixmap(QPixmap(r"D:\ECE 1140\ECE1140ChooChoo\Train_Model\pizza_hut_ad_1.jpg"))
        self.Advertisements.setScaledContents(True)
        self.Advertisements.setGeometry(QRect(10, 5, 228, 83))
        self.Advertisements.setMinimumSize(QSize(0, 0))
        self.Advertisements.setAutoFillBackground(True)
        self.Advertisements.setStyleSheet(u"")
        self.Advertisements.setFrameShape(QFrame.WinPanel)
        self.Advertisements.setFrameShadow(QFrame.Plain)
        self.Advertisements.setTextFormat(Qt.AutoText)
        self.Advertisements.setScaledContents(False)
        self.Announcement_2 = QLabel(self.Main)
        self.Announcement_2.setObjectName(u"Announcement_2")
        self.Announcement_2.setGeometry(QRect(224, 90, 471, 47))
        self.Announcement_2.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.Announcement_2.setFrameShape(QFrame.WinPanel)
        self.Announcement_2.setFrameShadow(QFrame.Plain)
        self.button_emergency = QPushButton(self.Main)
        self.button_emergency.setObjectName(u"button_emergency")
        self.button_emergency.setGeometry(QRect(30, 400, 206, 206))
        self.button_emergency.setFont(font4)
        self.button_emergency.setStyleSheet(
            u"""
            QPushButton#button_emergency {
                background-color: red;
                color: white;
                font-size: 30px;  /* Bigger text */
                font-weight: bold;
                border: 3px solid black;
                border-radius: 100px;  /* For a circle */
                min-width: 200px;
                min-height: 200px;
                /* 3D Effect using Gradient */
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1,
                                            stop:0 #ff4d4d, stop:1 #cc0000);
                box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.5);
            }

            QPushButton#button_emergency:pressed {
                background-color: darkred;
                border: 3px solid #660000;
                background: qlineargradient(spread:pad, x1:0.3, y1:0.3, x2:1, y2:1,
                                            stop:0 #cc0000, stop:1 #660000);
            }

            /* Style when the button is toggled on (checked) */
            QPushButton#button_emergency:checked {
                background-color: #880000; 
                /* Or any other color to show it’s latched down */
                border: 3px solid #440000;
            }
            """
)
        self.button_emergency.setFlat(False)
        self.line = QFrame(self.Main)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(254, 150, 16, 461))
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(self.Main)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(498, 150, 16, 461))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.LiveTrainData = QGroupBox(self.Main)
        self.LiveTrainData.setObjectName(u"LiveTrainData")
        self.LiveTrainData.setGeometry(QRect(510, 140, 185, 391))
        self.LiveTrainData.setFont(font2)
        self.LiveTrainData.setAutoFillBackground(True)
        self.LiveTrainData.setStyleSheet(u"")
        self.LiveTrainData.setFlat(False)
        self.gridLayoutWidget = QWidget(self.LiveTrainData)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(0, 30, 183, 351))
        self.LiveTrainDataGrid = QGridLayout(self.gridLayoutWidget)
        self.LiveTrainDataGrid.setSpacing(0)
        self.LiveTrainDataGrid.setObjectName(u"LiveTrainDataGrid")
        self.LiveTrainDataGrid.setContentsMargins(5, 0, 0, 0)
        self.MassVehicleLabel = QLabel(self.gridLayoutWidget)
        self.MassVehicleLabel.setObjectName(u"MassVehicleLabel")
        font7 = QFont()
        font7.setPointSize(11)
        font7.setBold(False)
        font7.setWeight(50)
        self.MassVehicleLabel.setFont(font7)
        self.MassVehicleLabel.setFrameShape(QFrame.WinPanel)
        self.MassVehicleLabel.setFrameShadow(QFrame.Sunken)

        self.LiveTrainDataGrid.addWidget(self.MassVehicleLabel, 5, 0, 1, 1)

        self.SpeedLimitValue = QLCDNumber(self.gridLayoutWidget)
        self.SpeedLimitValue.setObjectName(u"SpeedLimitValue")
        self.SpeedLimitValue.setFont(font2)
        self.SpeedLimitValue.setSegmentStyle(QLCDNumber.Flat)

        self.LiveTrainDataGrid.addWidget(self.SpeedLimitValue, 1, 1, 1, 1)

        self.LengthVehicleLabel = QLabel(self.gridLayoutWidget)
        self.LengthVehicleLabel.setObjectName(u"LengthVehicleLabel")
        self.LengthVehicleLabel.setFont(font7)
        self.LengthVehicleLabel.setFrameShape(QFrame.WinPanel)
        self.LengthVehicleLabel.setFrameShadow(QFrame.Sunken)

        self.LiveTrainDataGrid.addWidget(self.LengthVehicleLabel, 2, 0, 1, 1)

        self.LengthVehicleValue = QLCDNumber(self.gridLayoutWidget)
        self.LengthVehicleValue.setObjectName(u"LengthVehicleValue")
        self.LengthVehicleValue.setFont(font2)
        self.LengthVehicleValue.setSegmentStyle(QLCDNumber.Flat)

        self.LiveTrainDataGrid.addWidget(self.LengthVehicleValue, 2, 1, 1, 1)

        self.CommandedSpeedValue = QLCDNumber(self.gridLayoutWidget)
        self.CommandedSpeedValue.setObjectName(u"CommandedSpeedValue")
        self.CommandedSpeedValue.setFont(font2)
        self.CommandedSpeedValue.setSegmentStyle(QLCDNumber.Flat)

        self.LiveTrainDataGrid.addWidget(self.CommandedSpeedValue, 0, 1, 1, 1)

        self.HeightValue = QLCDNumber(self.gridLayoutWidget)
        self.HeightValue.setObjectName(u"HeightValue")
        self.HeightValue.setFont(font2)
        self.HeightValue.setSegmentStyle(QLCDNumber.Flat)

        self.LiveTrainDataGrid.addWidget(self.HeightValue, 3, 1, 1, 1)

        self.HeightLabel = QLabel(self.gridLayoutWidget)
        self.HeightLabel.setObjectName(u"HeightLabel")
        self.HeightLabel.setFont(font7)
        self.HeightLabel.setFrameShape(QFrame.WinPanel)
        self.HeightLabel.setFrameShadow(QFrame.Sunken)

        self.LiveTrainDataGrid.addWidget(self.HeightLabel, 3, 0, 1, 1)

        self.CrewCountValue = QLCDNumber(self.gridLayoutWidget)
        self.CrewCountValue.setObjectName(u"CrewCountValue")
        self.CrewCountValue.setFont(font2)
        self.CrewCountValue.setSegmentStyle(QLCDNumber.Flat)

        self.LiveTrainDataGrid.addWidget(self.CrewCountValue, 7, 1, 1, 1)

        self.SpeedLimitLabel = QLabel(self.gridLayoutWidget)
        self.SpeedLimitLabel.setObjectName(u"SpeedLimitLabel")
        self.SpeedLimitLabel.setFont(font7)
        self.SpeedLimitLabel.setFrameShape(QFrame.WinPanel)
        self.SpeedLimitLabel.setFrameShadow(QFrame.Sunken)

        self.LiveTrainDataGrid.addWidget(self.SpeedLimitLabel, 1, 0, 1, 1)

        self.WidthValue = QLCDNumber(self.gridLayoutWidget)
        self.WidthValue.setObjectName(u"WidthValue")
        self.WidthValue.setFont(font2)
        self.WidthValue.setSegmentStyle(QLCDNumber.Flat)

        self.LiveTrainDataGrid.addWidget(self.WidthValue, 4, 1, 1, 1)

        self.CrewCountLabel = QLabel(self.gridLayoutWidget)
        self.CrewCountLabel.setObjectName(u"CrewCountLabel")
        self.CrewCountLabel.setFont(font7)
        self.CrewCountLabel.setFrameShape(QFrame.WinPanel)
        self.CrewCountLabel.setFrameShadow(QFrame.Sunken)

        self.LiveTrainDataGrid.addWidget(self.CrewCountLabel, 7, 0, 1, 1)

        self.WidthLabel = QLabel(self.gridLayoutWidget)
        self.WidthLabel.setObjectName(u"WidthLabel")
        self.WidthLabel.setFont(font7)
        self.WidthLabel.setFrameShape(QFrame.WinPanel)
        self.WidthLabel.setFrameShadow(QFrame.Sunken)

        self.LiveTrainDataGrid.addWidget(self.WidthLabel, 4, 0, 1, 1)

        self.CommandedSpeedLabel = QLabel(self.gridLayoutWidget)
        self.CommandedSpeedLabel.setObjectName(u"CommandedSpeedLabel")
        self.CommandedSpeedLabel.setFont(font7)
        self.CommandedSpeedLabel.setFrameShape(QFrame.WinPanel)
        self.CommandedSpeedLabel.setFrameShadow(QFrame.Sunken)

        self.LiveTrainDataGrid.addWidget(self.CommandedSpeedLabel, 0, 0, 1, 1)

        self.PassengerCountLabel = QLabel(self.gridLayoutWidget)
        self.PassengerCountLabel.setObjectName(u"PassengerCountLabel")
        self.PassengerCountLabel.setFont(font7)
        self.PassengerCountLabel.setFrameShape(QFrame.WinPanel)
        self.PassengerCountLabel.setFrameShadow(QFrame.Sunken)

        self.LiveTrainDataGrid.addWidget(self.PassengerCountLabel, 6, 0, 1, 1)

        self.MassVehicleValue = QLCDNumber(self.gridLayoutWidget)
        self.MassVehicleValue.setObjectName(u"MassVehicleValue")
        self.MassVehicleValue.setFont(font2)
        self.MassVehicleValue.setSegmentStyle(QLCDNumber.Flat)

        self.LiveTrainDataGrid.addWidget(self.MassVehicleValue, 5, 1, 1, 1)

        self.PassengerCountValue = QLCDNumber(self.gridLayoutWidget)
        self.PassengerCountValue.setObjectName(u"PassengerCountValue")
        self.PassengerCountValue.setFont(font2)
        self.PassengerCountValue.setSegmentStyle(QLCDNumber.Flat)

        self.LiveTrainDataGrid.addWidget(self.PassengerCountValue, 6, 1, 1, 1)

        self.GradePercentage = QLabel(self.gridLayoutWidget)
        self.GradePercentage.setObjectName(u"GradePercentage")
        self.GradePercentage.setFont(font7)
        self.GradePercentage.setFrameShape(QFrame.WinPanel)
        self.GradePercentage.setFrameShadow(QFrame.Sunken)

        self.LiveTrainDataGrid.addWidget(self.GradePercentage, 8, 0, 1, 1)

        self.GradePercentageValue = QLCDNumber(self.gridLayoutWidget)
        self.GradePercentageValue.setObjectName(u"GradePercentageValue")
        self.GradePercentageValue.setFont(font2)
        self.GradePercentageValue.setSegmentStyle(QLCDNumber.Flat)

        self.LiveTrainDataGrid.addWidget(self.GradePercentageValue, 8, 1, 1, 1)

        self.gridLayoutWidget_2 = QWidget(self.Main)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(270, 150, 231, 215))
        self.TrainControllerDetails = QGridLayout(self.gridLayoutWidget_2)
        self.TrainControllerDetails.setObjectName(u"TrainControllerDetails")
        self.TrainControllerDetails.setContentsMargins(0, 0, 0, 0)
        self.Acceleration = QLabel(self.gridLayoutWidget_2)
        self.Acceleration.setObjectName(u"Acceleration")
        self.Acceleration.setFont(font3)
        self.Acceleration.setStyleSheet(u"background-color: rgb(168, 168, 168);")
        self.Acceleration.setFrameShape(QFrame.WinPanel)
        self.Acceleration.setFrameShadow(QFrame.Sunken)

        self.TrainControllerDetails.addWidget(self.Acceleration, 1, 0, 1, 1)

        self.AccValue = QLCDNumber(self.gridLayoutWidget_2)
        self.AccValue.setObjectName(u"AccValue")
        self.AccValue.setFrameShape(QFrame.Panel)
        self.AccValue.setFrameShadow(QFrame.Plain)
        self.AccValue.setSegmentStyle(QLCDNumber.Flat)

        self.TrainControllerDetails.addWidget(self.AccValue, 1, 1, 1, 1)

        self.SpeedValue = QLCDNumber(self.gridLayoutWidget_2)
        self.SpeedValue.setObjectName(u"SpeedValue")
        self.SpeedValue.setFrameShape(QFrame.Panel)
        self.SpeedValue.setFrameShadow(QFrame.Plain)
        self.SpeedValue.setSegmentStyle(QLCDNumber.Flat)

        self.TrainControllerDetails.addWidget(self.SpeedValue, 2, 1, 1, 1)

        self.Power = QLabel(self.gridLayoutWidget_2)
        self.Power.setObjectName(u"Power")
        self.Power.setFont(font3)
        self.Power.setStyleSheet(u"background-color: rgb(168, 168, 168);")
        self.Power.setFrameShape(QFrame.WinPanel)
        self.Power.setFrameShadow(QFrame.Sunken)
        self.Power.setIndent(6)

        self.TrainControllerDetails.addWidget(self.Power, 0, 0, 1, 1)

        self.ActualSpeed = QLabel(self.gridLayoutWidget_2)
        self.ActualSpeed.setObjectName(u"ActualSpeed")
        self.ActualSpeed.setFont(font1)
        self.ActualSpeed.setStyleSheet(u"background-color: rgb(168, 168, 168);")
        self.ActualSpeed.setFrameShape(QFrame.WinPanel)
        self.ActualSpeed.setFrameShadow(QFrame.Sunken)

        self.TrainControllerDetails.addWidget(self.ActualSpeed, 2, 0, 1, 1)

        self.PowerValue = QLCDNumber(self.gridLayoutWidget_2)
        self.PowerValue.setObjectName(u"PowerValue")
        self.PowerValue.setLayoutDirection(Qt.LeftToRight)
        self.PowerValue.setFrameShape(QFrame.Box)
        self.PowerValue.setFrameShadow(QFrame.Plain)
        self.PowerValue.setSegmentStyle(QLCDNumber.Flat)

        self.TrainControllerDetails.addWidget(self.PowerValue, 0, 1, 1, 1)

        self.CabinTemperature = QGroupBox(self.Main)
        self.CabinTemperature.setObjectName(u"CabinTemperature")
        self.CabinTemperature.setGeometry(QRect(510, 530, 181, 81))
        font8 = QFont()
        font8.setPointSize(11)
        font8.setBold(True)
        font8.setWeight(75)
        self.CabinTemperature.setFont(font8)
        self.Temperature = QLabel(self.CabinTemperature)
        self.Temperature.setObjectName(u"Temperature")
        self.Temperature.setGeometry(QRect(16, 23, 151, 51))
        font9 = QFont()
        font9.setPointSize(15)
        font9.setBold(True)
        font9.setWeight(75)
        self.Temperature.setFont(font9)
        self.Temperature.setStyleSheet(u"background-color: rgb(168, 168, 168);")
        self.Temperature.setFrameShape(QFrame.WinPanel)
        self.Temperature.setFrameShadow(QFrame.Raised)
        self.line_3 = QFrame(self.Main)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setGeometry(QRect(273, 365, 221, 16))
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)
        self.gridLayoutWidget_3 = QWidget(self.Main)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(270, 380, 231, 234))
        self.DoorsLightsBrakes = QGridLayout(self.gridLayoutWidget_3)
        self.DoorsLightsBrakes.setObjectName(u"DoorsLightsBrakes")
        self.DoorsLightsBrakes.setContentsMargins(0, 0, 0, 0)
        self.ServiceBrakesOn = QLabel(self.gridLayoutWidget_3)
        self.ServiceBrakesOn.setObjectName(u"ServiceBrakesOn")
        self.ServiceBrakesOn.setFont(font7)
        self.ServiceBrakesOn.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.ServiceBrakesOn, 0, 1, 1, 1)

        self.ExteriorLightsLabel = QLabel(self.gridLayoutWidget_3)
        self.ExteriorLightsLabel.setObjectName(u"ExteriorLightsLabel")
        self.ExteriorLightsLabel.setFont(font8)
        self.ExteriorLightsLabel.setFrameShape(QFrame.WinPanel)
        self.ExteriorLightsLabel.setFrameShadow(QFrame.Sunken)

        self.DoorsLightsBrakes.addWidget(self.ExteriorLightsLabel, 1, 0, 1, 1)

        self.ServiceBrakesOff = QLabel(self.gridLayoutWidget_3)
        self.ServiceBrakesOff.setObjectName(u"ServiceBrakesOff")
        self.ServiceBrakesOff.setFont(font7)
        self.ServiceBrakesOff.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.ServiceBrakesOff, 0, 2, 1, 1)

        self.ServiceBrakesLabel = QLabel(self.gridLayoutWidget_3)
        self.ServiceBrakesLabel.setObjectName(u"ServiceBrakesLabel")
        self.ServiceBrakesLabel.setFont(font8)
        self.ServiceBrakesLabel.setFrameShape(QFrame.WinPanel)
        self.ServiceBrakesLabel.setFrameShadow(QFrame.Sunken)

        self.DoorsLightsBrakes.addWidget(self.ServiceBrakesLabel, 0, 0, 1, 1)

        self.InteriorLightsLabel = QLabel(self.gridLayoutWidget_3)
        self.InteriorLightsLabel.setObjectName(u"InteriorLightsLabel")
        self.InteriorLightsLabel.setFont(font8)
        self.InteriorLightsLabel.setFrameShape(QFrame.WinPanel)
        self.InteriorLightsLabel.setFrameShadow(QFrame.Sunken)

        self.DoorsLightsBrakes.addWidget(self.InteriorLightsLabel, 2, 0, 1, 1)

        self.LeftDoorLabel = QLabel(self.gridLayoutWidget_3)
        self.LeftDoorLabel.setObjectName(u"LeftDoorLabel")
        self.LeftDoorLabel.setFont(font8)
        self.LeftDoorLabel.setFrameShape(QFrame.WinPanel)
        self.LeftDoorLabel.setFrameShadow(QFrame.Sunken)

        self.DoorsLightsBrakes.addWidget(self.LeftDoorLabel, 3, 0, 1, 1)

        self.RightDoorLabel = QLabel(self.gridLayoutWidget_3)
        self.RightDoorLabel.setObjectName(u"RightDoorLabel")
        self.RightDoorLabel.setFont(font8)
        self.RightDoorLabel.setFrameShape(QFrame.WinPanel)
        self.RightDoorLabel.setFrameShadow(QFrame.Sunken)

        self.DoorsLightsBrakes.addWidget(self.RightDoorLabel, 4, 0, 1, 1)

        self.ExteriorLightsOn = QLabel(self.gridLayoutWidget_3)
        self.ExteriorLightsOn.setObjectName(u"ExteriorLightsOn")
        self.ExteriorLightsOn.setFont(font7)
        self.ExteriorLightsOn.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.ExteriorLightsOn, 1, 1, 1, 1)

        self.ExteriorLightsOff = QLabel(self.gridLayoutWidget_3)
        self.ExteriorLightsOff.setObjectName(u"ExteriorLightsOff")
        self.ExteriorLightsOff.setFont(font7)
        self.ExteriorLightsOff.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.ExteriorLightsOff, 1, 2, 1, 1)

        self.InteriorLightsOn = QLabel(self.gridLayoutWidget_3)
        self.InteriorLightsOn.setObjectName(u"InteriorLightsOn")
        self.InteriorLightsOn.setFont(font7)
        self.InteriorLightsOn.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.InteriorLightsOn, 2, 1, 1, 1)

        self.InteriorLightsOff = QLabel(self.gridLayoutWidget_3)
        self.InteriorLightsOff.setObjectName(u"InteriorLightsOff")
        self.InteriorLightsOff.setFont(font7)
        self.InteriorLightsOff.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.InteriorLightsOff, 2, 2, 1, 1)

        self.LeftDoorOpen = QLabel(self.gridLayoutWidget_3)
        self.LeftDoorOpen.setObjectName(u"LeftDoorOpen")
        self.LeftDoorOpen.setFont(font7)
        self.LeftDoorOpen.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.LeftDoorOpen, 3, 1, 1, 1)

        self.LeftDoorClosed = QLabel(self.gridLayoutWidget_3)
        self.LeftDoorClosed.setObjectName(u"LeftDoorClosed")
        self.LeftDoorClosed.setFont(font7)
        self.LeftDoorClosed.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.LeftDoorClosed, 3, 2, 1, 1)

        self.RightDoorOpen = QLabel(self.gridLayoutWidget_3)
        self.RightDoorOpen.setObjectName(u"RightDoorOpen")
        self.RightDoorOpen.setFont(font7)
        self.RightDoorOpen.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.RightDoorOpen, 4, 1, 1, 1)

        self.RightDoorClosed = QLabel(self.gridLayoutWidget_3)
        self.RightDoorClosed.setObjectName(u"RightDoorClosed")
        self.RightDoorClosed.setFont(font7)
        self.RightDoorClosed.setFrameShape(QFrame.Box)

        self.DoorsLightsBrakes.addWidget(self.RightDoorClosed, 4, 2, 1, 1)

        self.Clock_12 = QLCDNumber(self.Main)
        self.Clock_12.setObjectName(u"Clock_12")
        self.Clock_12.setGeometry(QRect(563, 97, 81, 31))
        self.AM_PM = QLabel(self.Main)
        self.AM_PM.setObjectName(u"AM_PM")
        self.AM_PM.setGeometry(QRect(650, 97, 31, 31))
        font10 = QFont()
        font10.setPointSize(14)
        font10.setBold(True)
        font10.setWeight(75)
        self.AM_PM.setFont(font10)
        self.Announcement_1 = QLabel(self.Main)
        self.Announcement_1.setObjectName(u"Announcement_1")
        self.Announcement_1.setGeometry(QRect(10, 90, 211, 47))
        self.Announcement_1.setFont(font10)
        self.Announcement_1.setMouseTracking(True)
        self.Announcement_1.setAutoFillBackground(True)
        self.Announcement_1.setFrameShape(QFrame.WinPanel)
        self.Advertisements_2 = QLabel(self.Main)
        self.Advertisements_2.setObjectName(u"Advertisements_2")
        self.Advertisements_2.setPixmap(QPixmap(r"D:\ECE 1140\ECE1140ChooChoo\Train_Model\McD.jpg"))
        self.Advertisements_2.setScaledContents(True)
        self.Advertisements_2.setGeometry(QRect(240, 5, 228, 83))
        self.Advertisements_2.setMinimumSize(QSize(0, 0))
        self.Advertisements_2.setAutoFillBackground(True)
        self.Advertisements_2.setStyleSheet(u"")
        self.Advertisements_2.setFrameShape(QFrame.WinPanel)
        self.Advertisements_2.setFrameShadow(QFrame.Plain)
        self.Advertisements_2.setTextFormat(Qt.AutoText)
        self.Advertisements_2.setScaledContents(False)
        self.Advertisements_3 = QLabel(self.Main)
        self.Advertisements_3.setObjectName(u"Advertisements_3")
        self.Advertisements_3.setPixmap(QPixmap(r"D:\ECE 1140\ECE1140ChooChoo\Train_Model\whopper.jpg"))
        self.Advertisements_3.setScaledContents(True)
        self.Advertisements_3.setGeometry(QRect(470, 5, 224, 83))
        self.Advertisements_3.setMinimumSize(QSize(0, 0))
        self.Advertisements_3.setAutoFillBackground(True)
        self.Advertisements_3.setStyleSheet(u"")
        self.Advertisements_3.setFrameShape(QFrame.WinPanel)
        self.Advertisements_3.setFrameShadow(QFrame.Plain)
        self.Advertisements_3.setTextFormat(Qt.AutoText)
        self.Advertisements_3.setScaledContents(False)
        MainWindow.setCentralWidget(self.Main)
        self.FailureBox.raise_()
        self.Announcement_2.raise_()
        self.button_emergency.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.LiveTrainData.raise_()
        self.gridLayoutWidget_2.raise_()
        self.CabinTemperature.raise_()
        self.line_3.raise_()
        self.gridLayoutWidget_3.raise_()
        self.Clock_12.raise_()
        self.AM_PM.raise_()
        self.Announcement_1.raise_()
        self.Advertisements.raise_()
        self.Advertisements_2.raise_()
        self.Advertisements_3.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 710, 21))
        self.menuTrain_ID_1 = QMenu(self.menubar)
        self.menuTrain_ID_1.setObjectName(u"menuTrain_ID_1")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuTrain_ID_1.menuAction())

        self.retranslateUi(MainWindow)

        self.Disabled1.setDefault(False)
        self.Disabled2.setDefault(False)
        self.Disabled3.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.FailureBox.setTitle(QCoreApplication.translate("MainWindow", u"Failure Box", None))
        self.FailBrake.setText(QCoreApplication.translate("MainWindow", u"Brake Failure", None))
        self.Enabled1.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.Disabled1.setText(QCoreApplication.translate("MainWindow", u"Disabled", None))
        self.FailSignal.setText(QCoreApplication.translate("MainWindow", u"Signal Failure", None))
        self.FailEngine.setText(QCoreApplication.translate("MainWindow", u"Engine Failure", None))
        self.Enabled2.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.Disabled2.setText(QCoreApplication.translate("MainWindow", u"Disabled", None))
        self.Enabled3.setText(QCoreApplication.translate("MainWindow", u"Enabled", None))
        self.Disabled3.setText(QCoreApplication.translate("MainWindow", u"Disabled", None))
        self.Advertisements.setText("")
        self.Announcement_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">Next stop is Edgebrook</span></p></body></html>", None))
        self.button_emergency.setText(QCoreApplication.translate("MainWindow", u"Emergency \n"
"Brake", None))
        self.LiveTrainData.setTitle(QCoreApplication.translate("MainWindow", u"Live Train Data", None))
        self.MassVehicleLabel.setText(QCoreApplication.translate("MainWindow", u"Mass of Vehicle \n"
"(lbs)", None))
        self.LengthVehicleLabel.setText(QCoreApplication.translate("MainWindow", u"Length of \n"
"Vehicle (ft)", None))
        self.HeightLabel.setText(QCoreApplication.translate("MainWindow", u"Height (ft)", None))
        self.SpeedLimitLabel.setText(QCoreApplication.translate("MainWindow", u"Speed Limit \n"
"(mph)", None))
        self.CrewCountLabel.setText(QCoreApplication.translate("MainWindow", u"Crew Count", None))
        self.WidthLabel.setText(QCoreApplication.translate("MainWindow", u"Width (ft)", None))
        self.CommandedSpeedLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Commanded </p><p>Speed (mph)</p></body></html>", None))
        self.PassengerCountLabel.setText(QCoreApplication.translate("MainWindow", u"Passenger \n"
"Count", None))
        self.GradePercentage.setText(QCoreApplication.translate("MainWindow", u"Grade (%)", None))
        self.Acceleration.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Acceleration </p><p>(ft/s<span style=\" vertical-align:super;\">2</span>)</p></body></html>", None))
        self.Power.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Current Engine</p><p>Power (kW)</p></body></html>", None))
        self.ActualSpeed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">Actual </span></p><p><span style=\" font-size:12pt;\">Velocity (mph)</span></p></body></html>", None))
        self.CabinTemperature.setTitle(QCoreApplication.translate("MainWindow", u"Cabin Temperature", None))
        self.Temperature.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">68 \u00b0F</p></body></html>", None))
        self.ServiceBrakesOn.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">ON</p></body></html>", None))
        self.ExteriorLightsLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Exterior</p><p align=\"center\">Lights</p></body></html>", None))
        self.ServiceBrakesOff.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">OFF</p></body></html>", None))
        self.ServiceBrakesLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Service</p><p align=\"center\">Brakes</p></body></html>", None))
        self.InteriorLightsLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Interior</p><p align=\"center\">Lights</p></body></html>", None))
        self.LeftDoorLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Left Door</p></body></html>", None))
        self.RightDoorLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">Right Door</p></body></html>", None))
        self.ExteriorLightsOn.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">ON</p></body></html>", None))
        self.ExteriorLightsOff.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">OFF</p></body></html>", None))
        self.InteriorLightsOn.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">ON</p></body></html>", None))
        self.InteriorLightsOff.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">OFF</p></body></html>", None))
        self.LeftDoorOpen.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">OPEN</p></body></html>", None))
        self.LeftDoorClosed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">CLOSED</p></body></html>", None))
        self.RightDoorOpen.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">OPEN</p></body></html>", None))
        self.RightDoorClosed.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">CLOSED</p></body></html>", None))
        self.AM_PM.setText(QCoreApplication.translate("MainWindow", u"AM", None))
        self.Announcement_1.setText(QCoreApplication.translate("MainWindow", u"ANNOUNCEMENT: ", None))
        self.Advertisements_2.setText("")
        self.Advertisements_3.setText("")
        self.menuTrain_ID_1.setTitle(QCoreApplication.translate("MainWindow", u"Train ID 1", None))
    # retranslateUi

# if __name__ == "__main__":
#     import sys
#     app = QApplication(sys.argv)
#     MainWindow = QMainWindow()
#     ui = Ui_MainWindow()
#     ui.setupUi(MainWindow)
#     MainWindow.show()
#     sys.exit(app.exec_())
