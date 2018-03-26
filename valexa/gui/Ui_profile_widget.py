# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kdesrosiers/Documents/valexa/scripts/../valexa/gui/Ui_profile_widget.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_profileWidget(object):
    def setupUi(self, profileWidget):
        profileWidget.setObjectName("profileWidget")
        profileWidget.resize(400, 300)
        self.main_layout = QtWidgets.QVBoxLayout(profileWidget)
        self.main_layout.setSpacing(5)
        self.main_layout.setObjectName("main_layout")
        self.frame = QtWidgets.QFrame(profileWidget)
        self.frame.setAutoFillBackground(True)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_layout = QtWidgets.QVBoxLayout(self.frame)
        self.frame_layout.setObjectName("frame_layout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name_label = QtWidgets.QLabel(self.frame)
        self.name_label.setAutoFillBackground(False)
        self.name_label.setObjectName("name_label")
        self.horizontalLayout.addWidget(self.name_label)
        self.correction_label = QtWidgets.QLabel(self.frame)
        self.correction_label.setObjectName("correction_label")
        self.horizontalLayout.addWidget(self.correction_label)
        self.frame_layout.addLayout(self.horizontalLayout)
        self.table_widget = QtWidgets.QTableWidget(self.frame)
        self.table_widget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.table_widget.verticalHeader().setVisible(False)
        self.frame_layout.addWidget(self.table_widget)
        self.main_layout.addWidget(self.frame)

        self.retranslateUi(profileWidget)
        QtCore.QMetaObject.connectSlotsByName(profileWidget)

    def retranslateUi(self, profileWidget):
        _translate = QtCore.QCoreApplication.translate
        self.name_label.setText(_translate("profileWidget", "NameLabel"))
        self.correction_label.setText(_translate("profileWidget", "CorrectionLabel"))

