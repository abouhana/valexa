from PyQt5.QtWidgets import QApplication
import sys

###temp

from valexa.core.profiles import make_profiles, DEFAULT_TOLERANCE, DEFAULT_ACCEPTANCE
from valexa.core.xlsx import XlsxHandler
from valexa.core.html import HtmlWriter
from valexa.gui.profile_plot_canvas import ProfilePlotCanvas

from valexa.gui.app import ValexaApp, AppState

if __name__ == '__main__':
    state = AppState()
    app = QApplication(sys.argv)
    window = ValexaApp(state)
    window.show()
    app.exec_()
