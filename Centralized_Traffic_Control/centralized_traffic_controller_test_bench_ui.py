# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'centralized_traffic_controller_test_bench_uiOdJoAA.ui'
##
## Created by: Qt User Interface Compiler version 5.15.8
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *  # type: ignore
from PySide2.QtGui import *  # type: ignore
from PySide2.QtWidgets import *  # type: ignore


class Ui_ctc_TestBench(object):
    def setupUi(self, ctc_TestBench):
        if not ctc_TestBench.objectName():
            ctc_TestBench.setObjectName(u"ctc_TestBench")
        ctc_TestBench.resize(455, 244)
        self.centralwidget = QWidget(ctc_TestBench)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line, 1, 0, 1, 1)

        self.tb_block_occupancy_label = QLabel(self.centralwidget)
        self.tb_block_occupancy_label.setObjectName(u"tb_block_occupancy_label")
        self.tb_block_occupancy_label.setFrameShape(QFrame.Panel)
        self.tb_block_occupancy_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.tb_block_occupancy_label, 0, 0, 1, 1)

        self.tb_confirm_crossing_state_button = QPushButton(self.centralwidget)
        self.tb_confirm_crossing_state_button.setObjectName(u"tb_confirm_crossing_state_button")

        self.gridLayout.addWidget(self.tb_confirm_crossing_state_button, 2, 2, 1, 1)

        self.tb_crossing_state = QTextEdit(self.centralwidget)
        self.tb_crossing_state.setObjectName(u"tb_crossing_state")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tb_crossing_state.sizePolicy().hasHeightForWidth())
        self.tb_crossing_state.setSizePolicy(sizePolicy)
        self.tb_crossing_state.setMaximumSize(QSize(200, 25))
        self.tb_crossing_state.setLineWrapMode(QTextEdit.WidgetWidth)

        self.gridLayout.addWidget(self.tb_crossing_state, 2, 1, 1, 1)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShadow(QFrame.Plain)
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_2, 1, 1, 1, 1)

        self.tb_traffic_light_label = QLabel(self.centralwidget)
        self.tb_traffic_light_label.setObjectName(u"tb_traffic_light_label")
        self.tb_traffic_light_label.setFrameShape(QFrame.Panel)
        self.tb_traffic_light_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.tb_traffic_light_label, 4, 0, 1, 1)

        self.tb_railway_crossing_label = QLabel(self.centralwidget)
        self.tb_railway_crossing_label.setObjectName(u"tb_railway_crossing_label")
        self.tb_railway_crossing_label.setFrameShape(QFrame.Panel)
        self.tb_railway_crossing_label.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.tb_railway_crossing_label, 2, 0, 1, 1)

        self.tb_confirm_block_occupancy_button = QPushButton(self.centralwidget)
        self.tb_confirm_block_occupancy_button.setObjectName(u"tb_confirm_block_occupancy_button")

        self.gridLayout.addWidget(self.tb_confirm_block_occupancy_button, 0, 2, 1, 1)

        self.tb_confirm_traffic_light_button = QPushButton(self.centralwidget)
        self.tb_confirm_traffic_light_button.setObjectName(u"tb_confirm_traffic_light_button")

        self.gridLayout.addWidget(self.tb_confirm_traffic_light_button, 4, 2, 1, 1)

        self.tb_block_occupancy = QTextEdit(self.centralwidget)
        self.tb_block_occupancy.setObjectName(u"tb_block_occupancy")
        sizePolicy.setHeightForWidth(self.tb_block_occupancy.sizePolicy().hasHeightForWidth())
        self.tb_block_occupancy.setSizePolicy(sizePolicy)
        self.tb_block_occupancy.setMaximumSize(QSize(200, 25))
        self.tb_block_occupancy.setLineWrapMode(QTextEdit.WidgetWidth)

        self.gridLayout.addWidget(self.tb_block_occupancy, 0, 1, 1, 1)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShadow(QFrame.Plain)
        self.line_3.setLineWidth(2)
        self.line_3.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_3, 1, 2, 1, 1)

        self.tb_traffic_light_state = QTextEdit(self.centralwidget)
        self.tb_traffic_light_state.setObjectName(u"tb_traffic_light_state")
        sizePolicy.setHeightForWidth(self.tb_traffic_light_state.sizePolicy().hasHeightForWidth())
        self.tb_traffic_light_state.setSizePolicy(sizePolicy)
        self.tb_traffic_light_state.setMaximumSize(QSize(200, 25))
        self.tb_traffic_light_state.setLineWrapMode(QTextEdit.WidgetWidth)

        self.gridLayout.addWidget(self.tb_traffic_light_state, 4, 1, 1, 1)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShadow(QFrame.Plain)
        self.line_4.setLineWidth(2)
        self.line_4.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_4, 3, 0, 1, 1)

        self.line_5 = QFrame(self.centralwidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShadow(QFrame.Plain)
        self.line_5.setLineWidth(2)
        self.line_5.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_5, 3, 1, 1, 1)

        self.line_6 = QFrame(self.centralwidget)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShadow(QFrame.Plain)
        self.line_6.setLineWidth(2)
        self.line_6.setFrameShape(QFrame.HLine)

        self.gridLayout.addWidget(self.line_6, 3, 2, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        ctc_TestBench.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(ctc_TestBench)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 455, 21))
        ctc_TestBench.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(ctc_TestBench)
        self.statusbar.setObjectName(u"statusbar")
        ctc_TestBench.setStatusBar(self.statusbar)

        self.retranslateUi(ctc_TestBench)

        QMetaObject.connectSlotsByName(ctc_TestBench)
    # setupUi

    def retranslateUi(self, ctc_TestBench):
        ctc_TestBench.setWindowTitle(QCoreApplication.translate("ctc_TestBench", u"MainWindow", None))
        self.tb_block_occupancy_label.setText(QCoreApplication.translate("ctc_TestBench", u"Block Occupancies\n"
" [vector of enumerated types]", None))
        self.tb_confirm_crossing_state_button.setText(QCoreApplication.translate("ctc_TestBench", u"Confirm", None))
        self.tb_traffic_light_label.setText(QCoreApplication.translate("ctc_TestBench", u"Traffic Light States\n"
" [vector of booleans]", None))
        self.tb_railway_crossing_label.setText(QCoreApplication.translate("ctc_TestBench", u"Railway Crossing States\n"
" [vector of booleans]", None))
        self.tb_confirm_block_occupancy_button.setText(QCoreApplication.translate("ctc_TestBench", u"Confirm", None))
        self.tb_confirm_traffic_light_button.setText(QCoreApplication.translate("ctc_TestBench", u"Confirm", None))
    # retranslateUi

