# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app/gui/indicator_dialog_design.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_indicator_add_dialog(object):
    def setupUi(self, indicator_add_dialog):
        indicator_add_dialog.setObjectName("indicator_add_dialog")
        indicator_add_dialog.setSizeGripEnabled(False)
        indicator_add_dialog.setModal(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(indicator_add_dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.ind_model_label = QtWidgets.QLabel(indicator_add_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ind_model_label.sizePolicy().hasHeightForWidth())
        self.ind_model_label.setSizePolicy(sizePolicy)
        self.ind_model_label.setObjectName("ind_model_label")
        self.horizontalLayout.addWidget(self.ind_model_label)
        self.ind_model_comboBox = QtWidgets.QComboBox(indicator_add_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ind_model_comboBox.sizePolicy().hasHeightForWidth())
        self.ind_model_comboBox.setSizePolicy(sizePolicy)
        self.ind_model_comboBox.setObjectName("ind_model_comboBox")
        self.horizontalLayout.addWidget(self.ind_model_comboBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.line = QtWidgets.QFrame(indicator_add_dialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.parameters_verticalLayout = QtWidgets.QVBoxLayout()
        self.parameters_verticalLayout.setObjectName("parameters_verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(indicator_add_dialog)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(indicator_add_dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.parameters_verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(indicator_add_dialog)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(indicator_add_dialog)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.parameters_verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.parameters_verticalLayout)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(indicator_add_dialog)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setMouseTracking(False)
        self.buttonBox.setAcceptDrops(False)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(indicator_add_dialog)
        self.buttonBox.accepted.connect(indicator_add_dialog.accept)
        self.buttonBox.rejected.connect(indicator_add_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(indicator_add_dialog)
        indicator_add_dialog.setTabOrder(self.ind_model_comboBox, self.lineEdit)
        indicator_add_dialog.setTabOrder(self.lineEdit, self.comboBox)

    def retranslateUi(self, indicator_add_dialog):
        _translate = QtCore.QCoreApplication.translate
        indicator_add_dialog.setWindowTitle(_translate("indicator_add_dialog", "Add indicator"))
        self.ind_model_label.setText(_translate("indicator_add_dialog", "Model:"))
        self.label_2.setText(_translate("indicator_add_dialog", "TextLabel"))
        self.label.setText(_translate("indicator_add_dialog", "TextLabel"))