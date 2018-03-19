from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from openpyxl.utils.exceptions import InvalidFileException

from valexa.core.profiles import make_profiles
from valexa.core.xlsx import XlsxHandler
from valexa.gui import main_window
from valexa.gui.plot import ProfilePlotCanvas


class AppState:
    def __init__(self):
        self.calib_data = None
        self.valid_data = None
        self.profiles = []


class ValexaApp(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self, state: AppState):
        super().__init__()
        self.state = state
        self.setupUi(self)

        self.btn_response.clicked.connect(self.open_data_page)
        self.confirm_data_button.clicked.connect(self.open_model_page)
        self.xlsx_choose_button.clicked.connect(self.select_xlsx)

        self.stackedWidget.setCurrentIndex(0)

    def open_data_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def open_model_page(self):
        self.stackedWidget.setCurrentIndex(2)
        try:
            profiles = make_profiles(self.state.calib_data, self.state.valid_data)
            charts_layout = self.plot_layout
            for profile in profiles:
                chart_canva = ProfilePlotCanvas(profile=profile)
                charts_layout.addWidget(chart_canva)
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
