from PyQt5 import QtWidgets, QtGui, QtCore
from app.gui.design import Ui_MainWindow
from app.gui.indicator_dialog_design import Ui_indicator_add_dialog

from app.gui.utils import iterate_Qt_items, get_text_from_widget


class IndicatorAddDialogGUI(QtWidgets.QDialog, Ui_indicator_add_dialog):
    def __init__(self, application):
        super().__init__()
        self.app = application
        self.indicator_class = None
        self.indicator = None
        self.parameters_fields_dict = None
        self.setupUi(self)

        self._setup_comboBoxes()
        self._update_parameters_fields()

        self._connect_signals()

    def _connect_signals(self):
        self.ind_model_comboBox.currentTextChanged.connect(self._update_parameters_fields)
        self.accepted.connect(self._accepted)
        self.rejected.connect(self._rejected)

    def _accepted(self):
        params_values_dict = {key: get_text_from_widget(value) for key, value in self.parameters_fields_dict.items()}
        self.indicator = self.indicator_class(**params_values_dict)
        pass

    def _rejected(self):
        pass

    def _setup_comboBoxes(self):
        [self.ind_model_comboBox.addItem(model.__name__) for model in self.app.indicator_models]

    def _update_parameters_fields(self):
        [item.setParent(None) for item in iterate_Qt_items(self.parameters_verticalLayout)]
        self.indicator_class = [ind for ind in self.app.indicator_models
                                if ind.__name__ == get_text_from_widget(self.ind_model_comboBox)][0]
        self.parameters_fields_dict = {}
        _translate = QtCore.QCoreApplication.translate

        for key, value in self.indicator_class.get_parameters_dict(self.indicator_class).items():

            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setObjectName("{}_horizontalLayout".format(key))

            label = QtWidgets.QLabel(self)
            label.setObjectName("{}_label".format(key))
            label.setText(_translate("indicator_add_dialog", "{}:".format(key)))
            h_layout.addWidget(label)

            if type(value) == str:
                input_widget = QtWidgets.QComboBox(self)

                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(input_widget.hasHeightForWidth())
                input_widget.setSizePolicy(sizePolicy)

                input_widget.setObjectName("{}_input_widget".format(key))
            elif type(value) in [int, float]:
                input_widget = QtWidgets.QLineEdit(self)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(input_widget.sizePolicy().hasHeightForWidth())
                input_widget.setSizePolicy(sizePolicy)
                input_widget.setDragEnabled(False)
                input_widget.setReadOnly(False)
                input_widget.setObjectName("{}_input_widget")
            else:
                raise Exception('incorrect something')

            self.parameters_fields_dict.update({key: input_widget})
            h_layout.addWidget(input_widget)

            self.parameters_verticalLayout.addLayout(h_layout)


class MainGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, application):
        super().__init__()
        self.app = application
        self.plot_pixmap = None
        self.setupUi(self)

        self._setup_comboBoxes()
        self._update_indicators_tableWidget()
        self._connect_signals()

    def _update_indicators_tableWidget(self):
        self.indicators_tableWidget.setRowCount(0)
        for indicator in self.app.active_indicators:
            r_pos = self.indicators_tableWidget.rowCount()
            self.indicators_tableWidget.insertRow(r_pos)
            self.indicators_tableWidget.setItem(r_pos, 0, QtWidgets.QTableWidgetItem(indicator.name))


    def _connect_signals(self):
        self.plot_pushButton.clicked.connect(self.plot_pushButton_click)
        self.open_pushButton.clicked.connect(self.open_pushButton_click)
        self.update_pushButton.clicked.connect(self.update_pushButton_click)
        self.exit_pushButton.clicked.connect(self.exit_pushButton_click)
        self.add_ind_pushButton.clicked.connect(self.add_ind_pushButton_click)

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        if self.graph_label.pixmap():
            self._update_graph_label()
            pass

    def _setup_comboBoxes(self):
        [self.pair_comboBox.addItem(pair) for pair in self.app.config_manager['APPLICATION']['pairs'].split(',')]
        [self.resolution_comboBox.addItem(res) for res in self.app.config_manager['APPLICATION']['resolutions']
            .split(',')]

    def _update_graph_label(self):
        pixmap = self.plot_pixmap.scaled(self.graph_label.frameGeometry().width(),
                                         self.graph_label.frameGeometry().height() - 2)
        self.graph_label.setPixmap(pixmap)

    def plot_pushButton_click(self):
        self.app.plot()
        self.plot_pixmap = QtGui.QPixmap(self.app.config_manager['PLOT']['filepath'])

        self.tabWidget.setCurrentIndex(2)
        self._update_graph_label()

    def update_pushButton_click(self):
        self.app.update()

    def open_pushButton_click(self):
        self.app.open()

    def exit_pushButton_click(self):
        self.app.exit()

    def add_ind_pushButton_click(self):
        add_ind_window = IndicatorAddDialogGUI(self.app)
        add_ind_window.exec_()
        if add_ind_window.indicator:
            self.app.active_indicators.append(add_ind_window.indicator)
            self._update_indicators_tableWidget()
