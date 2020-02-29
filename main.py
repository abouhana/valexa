from PyQt5.QtWidgets import QApplication
import sys

from valexa.gui.app import ValexaApp, AppState

if __name__ == '__main__':
    state = AppState()
    app = QApplication(sys.argv)
    window = ValexaApp(state)
    window.show()
    app.exec_()
