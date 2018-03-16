from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
import sys

from openpyxl.utils.exceptions import InvalidFileException

from valexa.core.xlsx import XlsxHandler
from valexa.gui import main_window


class ValexaApp(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_response.clicked.connect(self.open_data_format)
        self.xlsx_choose_button.clicked.connect(self.select_xlsx)

        self.stackedWidget.setCurrentIndex(0)

    def open_data_format(self):
        self.stackedWidget.setCurrentIndex(1)

    def select_xlsx(self):
        filename, _ = QFileDialog.getOpenFileName()
        try:
            xlsx_handler = XlsxHandler(filename)
            self.file_name_input.setText(filename)
        except InvalidFileException as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ValexaApp()
    window.show()
    app.exec_()
