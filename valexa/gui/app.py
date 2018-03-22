from PyQt5.QtGui import QIntValidator, QPalette
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, qApp
from openpyxl.utils.exceptions import InvalidFileException

from valexa.core.profiles import make_profiles, DEFAULT_TOLERANCE, DEFAULT_ACCEPTANCE
from valexa.core.xlsx import XlsxHandler
from valexa.gui import Ui_main_window
from valexa.gui.profile_widget import ProfileWidget


class AppState:

    def __init__(self):
        self.calib_data = None
        self.valid_data = None
        self.profiles = []
        self.tolerance_limit = DEFAULT_TOLERANCE
        self.acceptance_limit = DEFAULT_ACCEPTANCE

    def reset(self):
        self.__init__()


class ValexaApp(QMainWindow, Ui_main_window.Ui_MainWindow):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state
        self.setupUi(self)

        # Dynamic widgets
        self.plot_canvas = []

        # Menu actions
        self.actionNew.triggered.connect(self.on_new_action)
        self.actionQuit.triggered.connect(qApp.quit)

        self.btn_response.clicked.connect(self.open_data_page)
        self.confirm_data_button.clicked.connect(self.open_model_page)
        self.xlsx_choose_button.clicked.connect(self.select_xlsx)

        # Input binding
        self.toleranceLimitLineEdit.setValidator(QIntValidator())
        self.acceptanceLimitLineEdit.setValidator(QIntValidator())
        self.toleranceLimitLineEdit.textChanged.connect(self.on_tolerance_changed)
        self.acceptanceLimitLineEdit.textChanged.connect(self.on_acceptance_changed)

        # force page 1
        self.stackedWidget.setCurrentIndex(0)

    def on_new_action(self):
        self.state.reset()
        self.stackedWidget.setCurrentIndex(0)
        self.file_name_input.setText("")
        self.calibration_data_list_widget.clear()
        self.validation_data_list_widget.clear()

    def open_data_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def open_model_page(self):
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.stackedWidget.setCurrentIndex(2)
        try:
            profiles = make_profiles(self.state.calib_data, self.state.valid_data, self.state.tolerance_limit,
                                     self.state.acceptance_limit)
            plot_layout = self.plot_layout
            for profile in profiles:
                profile_widget = ProfileWidget(profile=profile)
                plot_layout.addWidget(profile_widget)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def select_xlsx(self):
        filename, _ = QFileDialog.getOpenFileName()
        try:
            if filename != "":
                xlsx_handler = XlsxHandler(filename)
                self.file_name_input.setText(filename)
                self.confirm_data_button.setEnabled(True)

                self.state.calib_data = xlsx_handler.get_calibration_data()
                self.state.valid_data = xlsx_handler.get_validation_data()

                self.calibration_data_list_widget.addItems([str(r) for r in self.state.calib_data])
                self.validation_data_list_widget.addItems([str(r) for r in self.state.valid_data])

        except InvalidFileException as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_tolerance_changed(self, text):
        if text:
            self.state.tolerance_limit = int(text)

    def on_acceptance_changed(self, text):
        if text:
            self.state.acceptance_limit = int(text)
