# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'centralized_traffic_controller_test_bench_uibVibve.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import *  # type: ignore
from PyQt5.QtGui import *  # type: ignore
from PyQt5.QtWidgets import *  # type: ignore


class Ui_ctc_TestBench(object):
    def setupUi(self, ctc_TestBench):
        if not ctc_TestBench.objectName():
            ctc_TestBench.setObjectName(u"ctc_TestBench")
        ctc_TestBench.resize(649, 490)
        self.centralwidget = QWidget(ctc_TestBench)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.horizontalLayout_3 = QHBoxLayout(self.widget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        self.label.setFrameShape(QFrame.Box)
        self.label.setLineWidth(2)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFrameShape(QFrame.Box)
        self.label_2.setLineWidth(2)
        self.label_2.setTextFormat(Qt.AutoText)
        self.label_2.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_2)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)

        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addWidget(self.widget)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout_2 = QGridLayout(self.widget_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_8 = QGridLayout()
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.label_30 = QLabel(self.widget_2)
        self.label_30.setObjectName(u"label_30")
        self.label_30.setFrameShape(QFrame.Box)
        self.label_30.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.label_30, 0, 3, 1, 1)

        self.line_8 = QFrame(self.widget_2)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShadow(QFrame.Plain)
        self.line_8.setLineWidth(2)
        self.line_8.setFrameShape(QFrame.VLine)

        self.gridLayout_8.addWidget(self.line_8, 1, 2, 1, 1)

        self.tb_out_switch_states = QLabel(self.widget_2)
        self.tb_out_switch_states.setObjectName(u"tb_out_switch_states")
        self.tb_out_switch_states.setFrameShape(QFrame.Box)

        self.gridLayout_8.addWidget(self.tb_out_switch_states, 3, 4, 1, 1)

        self.label_28 = QLabel(self.widget_2)
        self.label_28.setObjectName(u"label_28")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_28.sizePolicy().hasHeightForWidth())
        self.label_28.setSizePolicy(sizePolicy)
        font = QFont()
        font.setKerning(True)
        self.label_28.setFont(font)
        self.label_28.setFrameShape(QFrame.Box)
        self.label_28.setAlignment(Qt.AlignCenter)
        self.label_28.setWordWrap(True)

        self.gridLayout_8.addWidget(self.label_28, 0, 0, 1, 1)

        self.label_8 = QLabel(self.widget_2)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setFrameShape(QFrame.Box)
        self.label_8.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.label_8, 1, 3, 1, 1)

        self.label_22 = QLabel(self.widget_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setFrameShape(QFrame.Box)
        self.label_22.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.label_22, 3, 3, 1, 1)

        self.tb_in_crossing_states = QTextEdit(self.widget_2)
        self.tb_in_crossing_states.setObjectName(u"tb_in_crossing_states")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tb_in_crossing_states.sizePolicy().hasHeightForWidth())
        self.tb_in_crossing_states.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.tb_in_crossing_states, 1, 1, 1, 1)

        self.line_5 = QFrame(self.widget_2)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShadow(QFrame.Plain)
        self.line_5.setLineWidth(2)
        self.line_5.setFrameShape(QFrame.VLine)

        self.gridLayout_8.addWidget(self.line_5, 3, 2, 1, 1)

        self.label_25 = QLabel(self.widget_2)
        self.label_25.setObjectName(u"label_25")
        sizePolicy.setHeightForWidth(self.label_25.sizePolicy().hasHeightForWidth())
        self.label_25.setSizePolicy(sizePolicy)
        self.label_25.setFrameShape(QFrame.Box)
        self.label_25.setAlignment(Qt.AlignCenter)
        self.label_25.setWordWrap(True)

        self.gridLayout_8.addWidget(self.label_25, 1, 0, 1, 1)

        self.line_6 = QFrame(self.widget_2)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShadow(QFrame.Plain)
        self.line_6.setLineWidth(2)
        self.line_6.setFrameShape(QFrame.VLine)

        self.gridLayout_8.addWidget(self.line_6, 2, 2, 1, 1)

        self.tb_out_maintenance = QLabel(self.widget_2)
        self.tb_out_maintenance.setObjectName(u"tb_out_maintenance")
        self.tb_out_maintenance.setFrameShape(QFrame.Box)

        self.gridLayout_8.addWidget(self.tb_out_maintenance, 2, 4, 1, 1)

        self.tb_out_speed = QLabel(self.widget_2)
        self.tb_out_speed.setObjectName(u"tb_out_speed")
        self.tb_out_speed.setFrameShape(QFrame.Box)

        self.gridLayout_8.addWidget(self.tb_out_speed, 0, 4, 1, 1)

        self.label_16 = QLabel(self.widget_2)
        self.label_16.setObjectName(u"label_16")
        sizePolicy.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy)
        self.label_16.setFrameShape(QFrame.Box)
        self.label_16.setAlignment(Qt.AlignCenter)
        self.label_16.setWordWrap(True)

        self.gridLayout_8.addWidget(self.label_16, 3, 0, 1, 1)

        self.label_13 = QLabel(self.widget_2)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setFrameShape(QFrame.Box)
        self.label_13.setAlignment(Qt.AlignCenter)

        self.gridLayout_8.addWidget(self.label_13, 2, 3, 1, 1)

        self.line_7 = QFrame(self.widget_2)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShadow(QFrame.Plain)
        self.line_7.setLineWidth(2)
        self.line_7.setFrameShape(QFrame.VLine)

        self.gridLayout_8.addWidget(self.line_7, 0, 2, 1, 1)

        self.tb_in_light_states = QTextEdit(self.widget_2)
        self.tb_in_light_states.setObjectName(u"tb_in_light_states")
        sizePolicy1.setHeightForWidth(self.tb_in_light_states.sizePolicy().hasHeightForWidth())
        self.tb_in_light_states.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.tb_in_light_states, 2, 1, 1, 1)

        self.tb_out_authority = QLabel(self.widget_2)
        self.tb_out_authority.setObjectName(u"tb_out_authority")
        self.tb_out_authority.setFrameShape(QFrame.Box)

        self.gridLayout_8.addWidget(self.tb_out_authority, 1, 4, 1, 1)

        self.tb_in_switch_states = QTextEdit(self.widget_2)
        self.tb_in_switch_states.setObjectName(u"tb_in_switch_states")
        sizePolicy1.setHeightForWidth(self.tb_in_switch_states.sizePolicy().hasHeightForWidth())
        self.tb_in_switch_states.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.tb_in_switch_states, 3, 1, 1, 1)

        self.label_7 = QLabel(self.widget_2)
        self.label_7.setObjectName(u"label_7")
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setFrameShape(QFrame.Box)
        self.label_7.setAlignment(Qt.AlignCenter)
        self.label_7.setWordWrap(True)

        self.gridLayout_8.addWidget(self.label_7, 2, 0, 1, 1)

        self.tb_in_block_states = QTextEdit(self.widget_2)
        self.tb_in_block_states.setObjectName(u"tb_in_block_states")
        sizePolicy1.setHeightForWidth(self.tb_in_block_states.sizePolicy().hasHeightForWidth())
        self.tb_in_block_states.setSizePolicy(sizePolicy1)

        self.gridLayout_8.addWidget(self.tb_in_block_states, 0, 1, 1, 1)

        self.tb_in_confirm_vals = QPushButton(self.widget_2)
        self.tb_in_confirm_vals.setObjectName(u"tb_in_confirm_vals")

        self.gridLayout_8.addWidget(self.tb_in_confirm_vals, 4, 1, 1, 1)

        self.gridLayout_8.setRowStretch(0, 1)
        self.gridLayout_8.setRowStretch(1, 1)
        self.gridLayout_8.setRowStretch(2, 1)
        self.gridLayout_8.setRowStretch(3, 1)
        self.gridLayout_8.setColumnStretch(0, 5)
        self.gridLayout_8.setColumnStretch(1, 5)
        self.gridLayout_8.setColumnStretch(2, 1)
        self.gridLayout_8.setColumnStretch(3, 5)
        self.gridLayout_8.setColumnStretch(4, 5)

        self.gridLayout_2.addLayout(self.gridLayout_8, 0, 0, 1, 1)


        self.verticalLayout_2.addWidget(self.widget_2)

        ctc_TestBench.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ctc_TestBench)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 649, 21))
        ctc_TestBench.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ctc_TestBench)
        self.statusbar.setObjectName(u"statusbar")
        ctc_TestBench.setStatusBar(self.statusbar)

        self.retranslateUi(ctc_TestBench)

        QMetaObject.connectSlotsByName(ctc_TestBench)
    # setupUi

    def retranslateUi(self, ctc_TestBench):
        ctc_TestBench.setWindowTitle(QCoreApplication.translate("ctc_TestBench", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("ctc_TestBench", u"Inputs", None))
        self.label_2.setText(QCoreApplication.translate("ctc_TestBench", u"Outputs", None))
        self.label_30.setText(QCoreApplication.translate("ctc_TestBench", u"Suggested Speed (km/hr)", None))
        self.tb_out_switch_states.setText(QCoreApplication.translate("ctc_TestBench", u"DATA", None))
        self.label_28.setText(QCoreApplication.translate("ctc_TestBench", u"Enter Block State\n"
"[List of Enums: Unoccipied, Occupied, Error]", None))
        self.label_8.setText(QCoreApplication.translate("ctc_TestBench", u"Suggested Authority (m)", None))
        self.label_22.setText(QCoreApplication.translate("ctc_TestBench", u"Override Switch States", None))
        self.label_25.setText(QCoreApplication.translate("ctc_TestBench", u"Enter Railway Crossing State\n"
"[List of Bools]", None))
        self.tb_out_maintenance.setText(QCoreApplication.translate("ctc_TestBench", u"DATA", None))
        self.tb_out_speed.setText(QCoreApplication.translate("ctc_TestBench", u"DATA", None))
        self.label_16.setText(QCoreApplication.translate("ctc_TestBench", u"Enter Switch States\n"
"[List of Bools]", None))
        self.label_13.setText(QCoreApplication.translate("ctc_TestBench", u"Maintenance Requests", None))
        self.tb_out_authority.setText(QCoreApplication.translate("ctc_TestBench", u"DATA", None))
        self.label_7.setText(QCoreApplication.translate("ctc_TestBench", u"Enter Light State\n"
"[List of Enum: Green, Yellow, Red]", None))
        self.tb_in_confirm_vals.setText(QCoreApplication.translate("ctc_TestBench", u"Confirm", None))
    # retranslateUi


