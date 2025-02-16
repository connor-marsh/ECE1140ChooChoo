# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ctc_uiWdmYPJ.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(696, 720)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_4 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(3)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.Panel)

        self.horizontalLayout_3.addWidget(self.label)

        self.active_train_number_label = QLabel(self.frame)
        self.active_train_number_label.setObjectName(u"active_train_number_label")
        self.active_train_number_label.setFrameShape(QFrame.Box)

        self.horizontalLayout_3.addWidget(self.active_train_number_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.current_time_label = QLabel(self.frame)
        self.current_time_label.setObjectName(u"current_time_label")
        sizePolicy.setHeightForWidth(self.current_time_label.sizePolicy().hasHeightForWidth())
        self.current_time_label.setSizePolicy(sizePolicy)
        self.current_time_label.setFrameShape(QFrame.Box)
        self.current_time_label.setScaledContents(False)
        self.current_time_label.setAlignment(Qt.AlignCenter)
        self.current_time_label.setIndent(1)

        self.horizontalLayout_3.addWidget(self.current_time_label)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)


        self.verticalLayout_2.addWidget(self.frame)

        self.groupBox_4 = QGroupBox(self.centralwidget)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.main_track_view = QGraphicsView(self.groupBox_4)
        self.main_track_view.setObjectName(u"main_track_view")

        self.horizontalLayout_5.addWidget(self.main_track_view)


        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)


        self.verticalLayout_2.addWidget(self.groupBox_4)

        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_2)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Plain)
        self.frame_3.setLineWidth(2)
        self.verticalLayout_3 = QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.groupBox_41 = QGroupBox(self.frame_3)
        self.groupBox_41.setObjectName(u"groupBox_41")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox_41)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.main_key = QLabel(self.groupBox_41)
        self.main_key.setObjectName(u"main_key")
        self.main_key.setPixmap(QPixmap(u"key3.PNG"))
        self.main_key.setScaledContents(True)

        self.verticalLayout_5.addWidget(self.main_key)


        self.horizontalLayout_7.addLayout(self.verticalLayout_5)


        self.verticalLayout.addWidget(self.groupBox_41)

        self.groupBox_5 = QGroupBox(self.frame_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setAutoFillBackground(False)
        self.horizontalLayout_8 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_8.setSpacing(1)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.groupBox_5)
        self.label_3.setObjectName(u"label_3")
        font = QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_3)

        self.main_line_slider = QSlider(self.groupBox_5)
        self.main_line_slider.setObjectName(u"main_line_slider")
        self.main_line_slider.setMaximum(1)
        self.main_line_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_8.addWidget(self.main_line_slider)

        self.label_4 = QLabel(self.groupBox_5)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)

        self.horizontalLayout_8.addWidget(self.label_4)

        self.line = QFrame(self.groupBox_5)
        self.line.setObjectName(u"line")
        self.line.setWindowModality(Qt.WindowModal)
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy1)
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QFrame.VLine)

        self.horizontalLayout_8.addWidget(self.line)

        self.label_5 = QLabel(self.groupBox_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_5)

        self.main_mode_slider = QSlider(self.groupBox_5)
        self.main_mode_slider.setObjectName(u"main_mode_slider")
        self.main_mode_slider.setMaximum(1)
        self.main_mode_slider.setOrientation(Qt.Horizontal)

        self.horizontalLayout_8.addWidget(self.main_mode_slider)

        self.label_6 = QLabel(self.groupBox_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setFont(font)
        self.label_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_8.addWidget(self.label_6)


        self.verticalLayout.addWidget(self.groupBox_5)

        self.groupBox_3 = QGroupBox(self.frame_3)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_10 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, -1)
        self.widget = QWidget(self.groupBox_3)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.main_active_block_id = QLabel(self.widget)
        self.main_active_block_id.setObjectName(u"main_active_block_id")
        self.main_active_block_id.setFrameShape(QFrame.StyledPanel)
        self.main_active_block_id.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.main_active_block_id, 0, 1, 1, 1)

        self.main_active_block_status = QLabel(self.widget)
        self.main_active_block_status.setObjectName(u"main_active_block_status")
        self.main_active_block_status.setFrameShape(QFrame.StyledPanel)
        self.main_active_block_status.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.main_active_block_status, 1, 1, 1, 1)

        self.main_active_block_speed_limit = QLabel(self.widget)
        self.main_active_block_speed_limit.setObjectName(u"main_active_block_speed_limit")
        self.main_active_block_speed_limit.setFrameShape(QFrame.StyledPanel)
        self.main_active_block_speed_limit.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.main_active_block_speed_limit, 2, 1, 1, 1)

        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setFrameShape(QFrame.StyledPanel)

        self.gridLayout.addWidget(self.label_10, 1, 0, 1, 1)

        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setFrameShape(QFrame.StyledPanel)

        self.gridLayout.addWidget(self.label_11, 2, 0, 1, 1)

        self.label_9 = QLabel(self.widget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setFrameShape(QFrame.StyledPanel)

        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.horizontalLayout_10.addWidget(self.widget)

        self.line_2 = QFrame(self.groupBox_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QFrame.VLine)

        self.horizontalLayout_10.addWidget(self.line_2)

        self.widget_2 = QWidget(self.groupBox_3)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_7 = QVBoxLayout(self.widget_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_15 = QLabel(self.widget_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setAlignment(Qt.AlignCenter)

        self.verticalLayout_6.addWidget(self.label_15)

        self.main_switch_knob = QDial(self.widget_2)
        self.main_switch_knob.setObjectName(u"main_switch_knob")
        self.main_switch_knob.setEnabled(False)
        self.main_switch_knob.setMaximum(2)
        self.main_switch_knob.setSliderPosition(1)
        self.main_switch_knob.setOrientation(Qt.Horizontal)
        self.main_switch_knob.setInvertedAppearance(False)
        self.main_switch_knob.setInvertedControls(False)
        self.main_switch_knob.setWrapping(False)
        self.main_switch_knob.setNotchesVisible(True)

        self.verticalLayout_6.addWidget(self.main_switch_knob)


        self.verticalLayout_7.addLayout(self.verticalLayout_6)


        self.horizontalLayout_10.addWidget(self.widget_2)


        self.verticalLayout.addWidget(self.groupBox_3)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.horizontalLayout_2.addWidget(self.frame_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.stackedWidget = QStackedWidget(self.frame_2)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setFrameShape(QFrame.StyledPanel)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_9 = QVBoxLayout(self.page)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.main_active_trains = QTableWidget(self.page)
        if (self.main_active_trains.columnCount() < 4):
            self.main_active_trains.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.main_active_trains.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.main_active_trains.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.main_active_trains.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.main_active_trains.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        if (self.main_active_trains.rowCount() < 5):
            self.main_active_trains.setRowCount(5)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.main_active_trains.setVerticalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.main_active_trains.setVerticalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.main_active_trains.setVerticalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.main_active_trains.setVerticalHeaderItem(3, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.main_active_trains.setVerticalHeaderItem(4, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.main_active_trains.setItem(0, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.main_active_trains.setItem(0, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.main_active_trains.setItem(0, 2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.main_active_trains.setItem(0, 3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.main_active_trains.setItem(1, 0, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.main_active_trains.setItem(1, 1, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.main_active_trains.setItem(1, 2, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.main_active_trains.setItem(1, 3, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.main_active_trains.setItem(2, 0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.main_active_trains.setItem(2, 1, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.main_active_trains.setItem(2, 2, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.main_active_trains.setItem(2, 3, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.main_active_trains.setItem(3, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.main_active_trains.setItem(3, 1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.main_active_trains.setItem(3, 2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.main_active_trains.setItem(3, 3, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.main_active_trains.setItem(4, 0, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.main_active_trains.setItem(4, 1, __qtablewidgetitem26)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.main_active_trains.setItem(4, 2, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.main_active_trains.setItem(4, 3, __qtablewidgetitem28)
        self.main_active_trains.setObjectName(u"main_active_trains")

        self.verticalLayout_9.addWidget(self.main_active_trains)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.widget_3 = QWidget(self.page)
        self.widget_3.setObjectName(u"widget_3")
        self.gridLayout_4 = QGridLayout(self.widget_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.main_switch_to_upload = QPushButton(self.widget_3)
        self.main_switch_to_upload.setObjectName(u"main_switch_to_upload")
        sizePolicy.setHeightForWidth(self.main_switch_to_upload.sizePolicy().hasHeightForWidth())
        self.main_switch_to_upload.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.main_switch_to_upload, 1, 1, 1, 1)

        self.main_switch_to_maintenance = QPushButton(self.widget_3)
        self.main_switch_to_maintenance.setObjectName(u"main_switch_to_maintenance")
        sizePolicy.setHeightForWidth(self.main_switch_to_maintenance.sizePolicy().hasHeightForWidth())
        self.main_switch_to_maintenance.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.main_switch_to_maintenance, 1, 0, 1, 1)

        self.main_switch_to_dispatch = QPushButton(self.widget_3)
        self.main_switch_to_dispatch.setObjectName(u"main_switch_to_dispatch")
        sizePolicy.setHeightForWidth(self.main_switch_to_dispatch.sizePolicy().hasHeightForWidth())
        self.main_switch_to_dispatch.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.main_switch_to_dispatch, 0, 0, 1, 1)

        self.main_switch_to_select = QPushButton(self.widget_3)
        self.main_switch_to_select.setObjectName(u"main_switch_to_select")
        sizePolicy.setHeightForWidth(self.main_switch_to_select.sizePolicy().hasHeightForWidth())
        self.main_switch_to_select.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.main_switch_to_select, 0, 1, 1, 1)


        self.gridLayout_4.addLayout(self.gridLayout_3, 1, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.widget_3)

        self.verticalLayout_8.setStretch(0, 1)

        self.verticalLayout_9.addLayout(self.verticalLayout_8)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_11 = QVBoxLayout(self.page_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.widget_4 = QWidget(self.page_2)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_9 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.sub_return = QPushButton(self.widget_4)
        self.sub_return.setObjectName(u"sub_return")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.sub_return.sizePolicy().hasHeightForWidth())
        self.sub_return.setSizePolicy(sizePolicy2)
        self.sub_return.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout.addWidget(self.sub_return)

        self.label_17 = QLabel(self.widget_4)
        self.label_17.setObjectName(u"label_17")
        sizePolicy.setHeightForWidth(self.label_17.sizePolicy().hasHeightForWidth())
        self.label_17.setSizePolicy(sizePolicy)
        self.label_17.setFrameShape(QFrame.Box)
        self.label_17.setLineWidth(2)
        self.label_17.setAlignment(Qt.AlignCenter)
        self.label_17.setMargin(0)

        self.horizontalLayout.addWidget(self.label_17)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.horizontalLayout_9.addLayout(self.horizontalLayout)


        self.verticalLayout_10.addWidget(self.widget_4)

        self.sub_train_select = QTableWidget(self.page_2)
        self.sub_train_select.setObjectName(u"sub_train_select")

        self.verticalLayout_10.addWidget(self.sub_train_select)

        self.widget_5 = QWidget(self.page_2)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_12 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.sub_dispatch_overide = QRadioButton(self.widget_5)
        self.sub_dispatch_overide.setObjectName(u"sub_dispatch_overide")

        self.horizontalLayout_11.addWidget(self.sub_dispatch_overide)

        self.sub_block_letter = QComboBox(self.widget_5)
        self.sub_block_letter.addItem("")
        self.sub_block_letter.addItem("")
        self.sub_block_letter.addItem("")
        self.sub_block_letter.addItem("")
        self.sub_block_letter.addItem("")
        self.sub_block_letter.setObjectName(u"sub_block_letter")

        self.horizontalLayout_11.addWidget(self.sub_block_letter)

        self.sub_block_number = QComboBox(self.widget_5)
        self.sub_block_number.addItem("")
        self.sub_block_number.addItem("")
        self.sub_block_number.addItem("")
        self.sub_block_number.addItem("")
        self.sub_block_number.addItem("")
        self.sub_block_number.setObjectName(u"sub_block_number")

        self.horizontalLayout_11.addWidget(self.sub_block_number)


        self.horizontalLayout_12.addLayout(self.horizontalLayout_11)


        self.verticalLayout_10.addWidget(self.widget_5)

        self.sub_dispatch_confirm = QPushButton(self.page_2)
        self.sub_dispatch_confirm.setObjectName(u"sub_dispatch_confirm")
        sizePolicy.setHeightForWidth(self.sub_dispatch_confirm.sizePolicy().hasHeightForWidth())
        self.sub_dispatch_confirm.setSizePolicy(sizePolicy)

        self.verticalLayout_10.addWidget(self.sub_dispatch_confirm)

        self.verticalLayout_10.setStretch(0, 1)
        self.verticalLayout_10.setStretch(1, 5)
        self.verticalLayout_10.setStretch(2, 3)
        self.verticalLayout_10.setStretch(3, 3)

        self.verticalLayout_11.addLayout(self.verticalLayout_10)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_13 = QVBoxLayout(self.page_3)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.widget_6 = QWidget(self.page_3)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_13 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.sub_return_2 = QPushButton(self.widget_6)
        self.sub_return_2.setObjectName(u"sub_return_2")
        sizePolicy2.setHeightForWidth(self.sub_return_2.sizePolicy().hasHeightForWidth())
        self.sub_return_2.setSizePolicy(sizePolicy2)
        self.sub_return_2.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_14.addWidget(self.sub_return_2)

        self.label_18 = QLabel(self.widget_6)
        self.label_18.setObjectName(u"label_18")
        sizePolicy.setHeightForWidth(self.label_18.sizePolicy().hasHeightForWidth())
        self.label_18.setSizePolicy(sizePolicy)
        self.label_18.setFrameShape(QFrame.Box)
        self.label_18.setLineWidth(2)
        self.label_18.setAlignment(Qt.AlignCenter)
        self.label_18.setMargin(0)

        self.horizontalLayout_14.addWidget(self.label_18)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_4)


        self.horizontalLayout_13.addLayout(self.horizontalLayout_14)


        self.verticalLayout_12.addWidget(self.widget_6)

        self.sub_train_select_2 = QTableWidget(self.page_3)
        self.sub_train_select_2.setObjectName(u"sub_train_select_2")

        self.verticalLayout_12.addWidget(self.sub_train_select_2)

        self.widget_7 = QWidget(self.page_3)
        self.widget_7.setObjectName(u"widget_7")
        self.gridLayout_6 = QGridLayout(self.widget_7)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.sub_current_authority = QLabel(self.widget_7)
        self.sub_current_authority.setObjectName(u"sub_current_authority")
        self.sub_current_authority.setFrameShape(QFrame.Box)

        self.gridLayout_5.addWidget(self.sub_current_authority, 1, 1, 1, 1)

        self.label_27 = QLabel(self.widget_7)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setFrameShape(QFrame.Box)

        self.gridLayout_5.addWidget(self.label_27, 1, 2, 1, 1)

        self.label_19 = QLabel(self.widget_7)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setFrameShape(QFrame.Box)

        self.gridLayout_5.addWidget(self.label_19, 0, 0, 1, 1)

        self.label_26 = QLabel(self.widget_7)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setFrameShape(QFrame.Box)

        self.gridLayout_5.addWidget(self.label_26, 0, 2, 1, 1)

        self.label_20 = QLabel(self.widget_7)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setFrameShape(QFrame.Box)

        self.gridLayout_5.addWidget(self.label_20, 1, 0, 1, 1)

        self.sub_enter_speed = QDoubleSpinBox(self.widget_7)
        self.sub_enter_speed.setObjectName(u"sub_enter_speed")

        self.gridLayout_5.addWidget(self.sub_enter_speed, 0, 3, 1, 1)

        self.sub_enter_authority = QDoubleSpinBox(self.widget_7)
        self.sub_enter_authority.setObjectName(u"sub_enter_authority")

        self.gridLayout_5.addWidget(self.sub_enter_authority, 1, 3, 1, 1)

        self.sub_current_speed = QLabel(self.widget_7)
        self.sub_current_speed.setObjectName(u"sub_current_speed")
        self.sub_current_speed.setFrameShape(QFrame.Box)

        self.gridLayout_5.addWidget(self.sub_current_speed, 0, 1, 1, 1)


        self.gridLayout_6.addLayout(self.gridLayout_5, 0, 0, 1, 1)


        self.verticalLayout_12.addWidget(self.widget_7)

        self.pushButton_9 = QPushButton(self.page_3)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.verticalLayout_12.addWidget(self.pushButton_9)


        self.verticalLayout_13.addLayout(self.verticalLayout_12)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_15 = QVBoxLayout(self.page_4)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_14 = QVBoxLayout()
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.widget_8 = QWidget(self.page_4)
        self.widget_8.setObjectName(u"widget_8")
        self.horizontalLayout_15 = QHBoxLayout(self.widget_8)
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.pushButton_8 = QPushButton(self.widget_8)
        self.pushButton_8.setObjectName(u"pushButton_8")
        sizePolicy2.setHeightForWidth(self.pushButton_8.sizePolicy().hasHeightForWidth())
        self.pushButton_8.setSizePolicy(sizePolicy2)
        self.pushButton_8.setMaximumSize(QSize(16777215, 16777215))

        self.horizontalLayout_16.addWidget(self.pushButton_8)

        self.label_23 = QLabel(self.widget_8)
        self.label_23.setObjectName(u"label_23")
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setFrameShape(QFrame.Box)
        self.label_23.setLineWidth(2)
        self.label_23.setAlignment(Qt.AlignCenter)
        self.label_23.setMargin(0)

        self.horizontalLayout_16.addWidget(self.label_23)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_5)


        self.horizontalLayout_15.addLayout(self.horizontalLayout_16)


        self.verticalLayout_14.addWidget(self.widget_8)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer)

        self.widget_10 = QWidget(self.page_4)
        self.widget_10.setObjectName(u"widget_10")
        self.horizontalLayout_20 = QHBoxLayout(self.widget_10)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_24 = QLabel(self.widget_10)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setFrameShape(QFrame.Box)

        self.horizontalLayout_19.addWidget(self.label_24)

        self.label_25 = QLabel(self.widget_10)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setFrameShape(QFrame.Box)

        self.horizontalLayout_19.addWidget(self.label_25)


        self.horizontalLayout_20.addLayout(self.horizontalLayout_19)


        self.verticalLayout_14.addWidget(self.widget_10)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_14.addItem(self.verticalSpacer_2)

        self.widget_9 = QWidget(self.page_4)
        self.widget_9.setObjectName(u"widget_9")
        self.horizontalLayout_17 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.pushButton_10 = QPushButton(self.widget_9)
        self.pushButton_10.setObjectName(u"pushButton_10")
        sizePolicy.setHeightForWidth(self.pushButton_10.sizePolicy().hasHeightForWidth())
        self.pushButton_10.setSizePolicy(sizePolicy)

        self.horizontalLayout_18.addWidget(self.pushButton_10)

        self.horizontalSpacer_6 = QSpacerItem(5, 10, QSizePolicy.Preferred, QSizePolicy.Minimum)

        self.horizontalLayout_18.addItem(self.horizontalSpacer_6)

        self.pushButton_11 = QPushButton(self.widget_9)
        self.pushButton_11.setObjectName(u"pushButton_11")
        sizePolicy.setHeightForWidth(self.pushButton_11.sizePolicy().hasHeightForWidth())
        self.pushButton_11.setSizePolicy(sizePolicy)

        self.horizontalLayout_18.addWidget(self.pushButton_11)


        self.horizontalLayout_17.addLayout(self.horizontalLayout_18)


        self.verticalLayout_14.addWidget(self.widget_9)

        self.verticalLayout_14.setStretch(0, 1)
        self.verticalLayout_14.setStretch(2, 5)
        self.verticalLayout_14.setStretch(4, 5)

        self.verticalLayout_15.addLayout(self.verticalLayout_14)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Preferred)

        self.verticalLayout_15.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.page_4)

        self.horizontalLayout_2.addWidget(self.stackedWidget)


        self.verticalLayout_2.addWidget(self.frame_2)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Centralized Traffic Control", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Active Trains:", None))
        self.active_train_number_label.setText(QCoreApplication.translate("MainWindow", u"7", None))
        self.current_time_label.setText(QCoreApplication.translate("MainWindow", u"12:00 am", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"Map", None))
        self.groupBox_41.setTitle(QCoreApplication.translate("MainWindow", u"Key", None))
        self.main_key.setText("")
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Mode Selections", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Green Line", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Red Line", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Automatic", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Manual", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Block Data", None))
        self.main_active_block_id.setText(QCoreApplication.translate("MainWindow", u"ID #", None))
        self.main_active_block_status.setText(QCoreApplication.translate("MainWindow", u"STATUS", None))
        self.main_active_block_speed_limit.setText(QCoreApplication.translate("MainWindow", u"MPH", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Block Status:", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Speed Limit", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Block ID:", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Left Track | AUTO | Right Track", None))
        ___qtablewidgetitem = self.main_active_trains.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Designation", None));
        ___qtablewidgetitem1 = self.main_active_trains.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Remaining Stops", None));
        ___qtablewidgetitem2 = self.main_active_trains.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Current Stop", None));
        ___qtablewidgetitem3 = self.main_active_trains.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Next Stop", None));

        __sortingEnabled = self.main_active_trains.isSortingEnabled()
        self.main_active_trains.setSortingEnabled(False)
        ___qtablewidgetitem4 = self.main_active_trains.item(0, 0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Train #1", None));
        ___qtablewidgetitem5 = self.main_active_trains.item(0, 1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"3", None));
        ___qtablewidgetitem6 = self.main_active_trains.item(0, 2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Station A", None));
        ___qtablewidgetitem7 = self.main_active_trains.item(0, 3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Station B", None));
        ___qtablewidgetitem8 = self.main_active_trains.item(1, 0)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Train #2", None));
        ___qtablewidgetitem9 = self.main_active_trains.item(1, 1)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"2", None));
        ___qtablewidgetitem10 = self.main_active_trains.item(1, 2)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Station B", None));
        ___qtablewidgetitem11 = self.main_active_trains.item(1, 3)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"Station C", None));
        ___qtablewidgetitem12 = self.main_active_trains.item(2, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Train #3", None));
        ___qtablewidgetitem13 = self.main_active_trains.item(2, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"5", None));
        ___qtablewidgetitem14 = self.main_active_trains.item(2, 2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"Station C", None));
        ___qtablewidgetitem15 = self.main_active_trains.item(2, 3)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Station D", None));
        ___qtablewidgetitem16 = self.main_active_trains.item(3, 0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Train #4", None));
        ___qtablewidgetitem17 = self.main_active_trains.item(3, 1)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"4", None));
        ___qtablewidgetitem18 = self.main_active_trains.item(3, 2)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Station D", None));
        ___qtablewidgetitem19 = self.main_active_trains.item(3, 3)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Station E", None));
        ___qtablewidgetitem20 = self.main_active_trains.item(4, 0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"Train #5", None));
        ___qtablewidgetitem21 = self.main_active_trains.item(4, 1)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem22 = self.main_active_trains.item(4, 2)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Station E", None));
        ___qtablewidgetitem23 = self.main_active_trains.item(4, 3)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"Yard", None));
        self.main_active_trains.setSortingEnabled(__sortingEnabled)

        self.main_switch_to_upload.setText(QCoreApplication.translate("MainWindow", u"Upload Schedule File", None))
        self.main_switch_to_maintenance.setText(QCoreApplication.translate("MainWindow", u"Maintenance", None))
        self.main_switch_to_dispatch.setText(QCoreApplication.translate("MainWindow", u"Dispatch Train", None))
        self.main_switch_to_select.setText(QCoreApplication.translate("MainWindow", u"Select Train", None))
        self.sub_return.setText(QCoreApplication.translate("MainWindow", u"<- Back", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Dispatch Train", None))
        self.sub_dispatch_overide.setText(QCoreApplication.translate("MainWindow", u"Send new train to block:", None))
        self.sub_block_letter.setItemText(0, QCoreApplication.translate("MainWindow", u"A", None))
        self.sub_block_letter.setItemText(1, QCoreApplication.translate("MainWindow", u"B", None))
        self.sub_block_letter.setItemText(2, QCoreApplication.translate("MainWindow", u"C", None))
        self.sub_block_letter.setItemText(3, QCoreApplication.translate("MainWindow", u"D", None))
        self.sub_block_letter.setItemText(4, QCoreApplication.translate("MainWindow", u"E", None))

        self.sub_block_number.setItemText(0, QCoreApplication.translate("MainWindow", u"1", None))
        self.sub_block_number.setItemText(1, QCoreApplication.translate("MainWindow", u"2", None))
        self.sub_block_number.setItemText(2, QCoreApplication.translate("MainWindow", u"3", None))
        self.sub_block_number.setItemText(3, QCoreApplication.translate("MainWindow", u"4", None))
        self.sub_block_number.setItemText(4, QCoreApplication.translate("MainWindow", u"5", None))

        self.sub_dispatch_confirm.setText(QCoreApplication.translate("MainWindow", u"Dispatch Train", None))
        self.sub_return_2.setText(QCoreApplication.translate("MainWindow", u"<- Back", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Select Train", None))
        self.sub_current_authority.setText(QCoreApplication.translate("MainWindow", u"MI", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Enter Suggested Authority", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Current Speed", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Enter Suggested Speed", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Current Authority", None))
        self.sub_current_speed.setText(QCoreApplication.translate("MainWindow", u"MPH", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"Confirm", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"<- Back", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Maintenance", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Chosen Block ID:", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"LETTER | NUM", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"Start Maintenance", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"End Maintenance", None))
    # retranslateUi

