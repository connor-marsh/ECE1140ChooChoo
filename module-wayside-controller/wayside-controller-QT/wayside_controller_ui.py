# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wayside_controller.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(826, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mode_select_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.mode_select_combo_box.setGeometry(QtCore.QRect(410, 10, 401, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.mode_select_combo_box.setFont(font)
        self.mode_select_combo_box.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mode_select_combo_box.setObjectName("mode_select_combo_box")
        self.mode_select_combo_box.addItem("")
        self.mode_select_combo_box.addItem("")
        self.junction_table = QtWidgets.QTableWidget(self.centralwidget)
        self.junction_table.setGeometry(QtCore.QRect(10, 330, 801, 192))
        self.junction_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.junction_table.setObjectName("junction_table")
        self.junction_table.setColumnCount(3)
        self.junction_table.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.junction_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.junction_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.junction_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.junction_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.junction_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.junction_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.junction_table.setItem(0, 2, item)
        self.block_table = QtWidgets.QTableWidget(self.centralwidget)
        self.block_table.setGeometry(QtCore.QRect(10, 100, 801, 221))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.block_table.setFont(font)
        self.block_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.block_table.setObjectName("block_table")
        self.block_table.setColumnCount(5)
        self.block_table.setRowCount(15)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(2, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(3, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.block_table.setItem(4, 4, item)
        self.import_plc_button = QtWidgets.QPushButton(self.centralwidget)
        self.import_plc_button.setGeometry(QtCore.QRect(10, 47, 381, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.import_plc_button.setFont(font)
        self.import_plc_button.setStyleSheet("background-color: rgb(110, 255, 102);")
        self.import_plc_button.setObjectName("import_plc_button")
        self.current_filename_label = QtWidgets.QLabel(self.centralwidget)
        self.current_filename_label.setGeometry(QtCore.QRect(10, 10, 381, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.current_filename_label.setFont(font)
        self.current_filename_label.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.current_filename_label.setObjectName("current_filename_label")
        self.section_select_combo_box = QtWidgets.QComboBox(self.centralwidget)
        self.section_select_combo_box.setGeometry(QtCore.QRect(410, 50, 231, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.section_select_combo_box.setFont(font)
        self.section_select_combo_box.setMaxVisibleItems(10)
        self.section_select_combo_box.setObjectName("section_select_combo_box")
        self.section_select_combo_box.addItem("")
        self.confirm_button = QtWidgets.QPushButton(self.centralwidget)
        self.confirm_button.setGeometry(QtCore.QRect(650, 50, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.confirm_button.setFont(font)
        self.confirm_button.setStyleSheet("background-color: rgb(157, 157, 157);")
        self.confirm_button.setObjectName("confirm_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 26))
        self.menubar.setObjectName("menubar")
        self.menuWayside_Controller_Blue_Line_1 = QtWidgets.QMenu(self.menubar)
        self.menuWayside_Controller_Blue_Line_1.setObjectName("menuWayside_Controller_Blue_Line_1")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuWayside_Controller_Blue_Line_1.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.mode_select_combo_box.setItemText(0, _translate("MainWindow", "Automatic Mode"))
        self.mode_select_combo_box.setItemText(1, _translate("MainWindow", "Maintenance Mode"))
        item = self.junction_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "1"))
        item = self.junction_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Junction"))
        item = self.junction_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Light Signals"))
        item = self.junction_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Switch Position"))
        __sortingEnabled = self.junction_table.isSortingEnabled()
        self.junction_table.setSortingEnabled(False)
        self.junction_table.setSortingEnabled(__sortingEnabled)
        item = self.block_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "A1"))
        item = self.block_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "A2"))
        item = self.block_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "A3"))
        item = self.block_table.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "A4"))
        item = self.block_table.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "A5"))
        item = self.block_table.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "B6"))
        item = self.block_table.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "B7"))
        item = self.block_table.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "B8"))
        item = self.block_table.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "B9"))
        item = self.block_table.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "B10"))
        item = self.block_table.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "C11"))
        item = self.block_table.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "C12"))
        item = self.block_table.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "C13"))
        item = self.block_table.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "C14"))
        item = self.block_table.verticalHeaderItem(14)
        item.setText(_translate("MainWindow", "C15"))
        item = self.block_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Occupancy"))
        item = self.block_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Suggested Speed"))
        item = self.block_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Suggested Authority"))
        item = self.block_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Commanded Speed"))
        item = self.block_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Commanded Authority"))
        __sortingEnabled = self.block_table.isSortingEnabled()
        self.block_table.setSortingEnabled(False)
        self.block_table.setSortingEnabled(__sortingEnabled)
        self.import_plc_button.setText(_translate("MainWindow", "Import PLC File"))
        self.current_filename_label.setText(_translate("MainWindow", "Current Filename:"))
        self.section_select_combo_box.setItemText(0, _translate("MainWindow", "Blue Line #1"))
        self.confirm_button.setText(_translate("MainWindow", "Confirm"))
        self.menuWayside_Controller_Blue_Line_1.setTitle(_translate("MainWindow", "Wayside Controller Blue Line #1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
