import mpl_toolkits.axisartist as AA
from matplotlib.backends.backend_qt5agg import \
    FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtWidgets



class ProfilePlotCanvas(FigureCanvas):

    def __init__(self, profile, parent=None, width=5, height=5, dpi=100):
        
        self.profile = profile
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = AA.Subplot(fig, 111)
        fig.add_subplot(self.axes)

        super().__init__(fig)

        self.setParent(parent)

        super().setSizePolicy(
            QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Expanding
        )

        super().updateGeometry()

        self._make_plot()

    def _make_plot(self):
        p = self.profile
        ax = self.axes
        levels_x = [l.calculated_concentration for l in p.levels]
        ax.axis["bottom", "top", "right"].set_visible(False)
        ax.axis["y=100"] = ax.new_floating_axis(nth_coord=0, value=100)
        ax.plot(levels_x, [l.recovery for l in p.levels], color="m", linewidth=2.0, marker=".", label="Recovery")
        ax.plot(levels_x, [l.rel_tolerance[0] for l in p.levels], linewidth=1.0, color="b",
                label="Min tolerance limit")
        ax.plot(levels_x, [l.rel_tolerance[1] for l in p.levels], linewidth=1.0, color="g",
                label="Max tolerance limit")
        ax.plot(levels_x, [p.acceptance_interval[0] for _ in p.levels], "k--", label="Acceptance limit")
        ax.plot(levels_x, [p.acceptance_interval[1] for _ in p.levels], "k--")
        results_x = [s.concentration for s in p.series]
        results_y = [(s.result / s.concentration) * 100 for s in p.series]
        ax.scatter(results_x, results_y, alpha=0.5, s=2)
        ax.set_xlabel("Concentration")
        ax.set_ylabel("Recovery (%)")
        ax.legend(loc=1)
        
