import json
from typing import Dict, List

import mpl_toolkits.axisartist as AA
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from valexa.core.profiles import (DEFAULT_ACCEPTANCE, DEFAULT_TOLERANCE,
    Profile, make_profiles)
from valexa.core.xlsx import XlsxHandler
from valexa.core.encoders import fig_to_dict
from plotly.subplots import make_subplots
import plotly.graph_objects as go




class PloterData:

    handler = XlsxHandler
    calib_data = None
    valid_data = None
    profiles = []
    tolerance_limit = DEFAULT_TOLERANCE
    acceptance_limit = DEFAULT_ACCEPTANCE

    def __init__(self, file: str or File=None, **kwargs):
        if file:
            self.load_data(file)

        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise TypeError("%s() received an invalid keyword %r. Only "
                                "arguments that are already attributes of the "
                                "class are accepted." % (self.__name__, key))
            else:
                setattr(self, key, value)

    def load_data(self, file: str or File) -> None:
        handler = self.handler(file)
        self.calib_data = handler.get_calibration_data()
        self.valid_data = handler.get_validation_data()

        self.profiles = make_profiles(
            self.calib_data, self.valid_data, 
            self.tolerance_limit, self.acceptance_limit
        )

    def reset(self):
        self.__init__()


class ProfilePlotCanvas(FigureCanvas):

    def __init__(self, profile, width=750, height=550):
        
        self.profile = profile
        self.figure = go.Figure({
            "layout": {
                "width": width,
                "height": height
            }
        })
        self._make_plot()

    def _make_plot(self):
        p = self.profile
        fig = self.figure

        levels_x = [l.calculated_concentration for l in p.levels]

        fig.add_trace(go.Scatter(x=levels_x, y=[l.recovery for l in p.levels],
                            name="Recovery",
                            line=dict(color="purple")))
        fig.add_trace(go.Scatter(x=levels_x, y=[l.rel_tolerance[0] for l in p.levels],
                            name="Min tolerance limit", mode="lines", 
                            line=dict(width=1, color="blue")))
        fig.add_trace(go.Scatter(x=levels_x, y=[l.rel_tolerance[1] for l in p.levels],
                            name="Max tolerance limit" ,mode="lines", 
                            line=dict(width=1, color="green")))
        fig.add_trace(go.Scatter(x=levels_x, y=[p.acceptance_interval[0] for _ in p.levels],
                            name="Acceptance limit", mode="lines", 
                            marker=dict(color="black"),
                            line=dict(dash="dash")))
        fig.add_trace(go.Scatter(x=levels_x, y=[p.acceptance_interval[1] for _ in p.levels],
                            name=None, mode="lines", 
                            marker=dict(color="black"),
                            line_dash="dash"))

        results_x = [s.concentration for s in p.series]
        results_y = [(s.result / s.concentration) * 100 for s in p.series]

        fig.add_scatter(x=results_x, y=results_y, 
                            name=None, mode="markers",
                            marker=dict(opacity=0.5, size=2))

        fig.update_layout(
              title_text="Stacked Subplots with Shared X-Axes",
              paper_bgcolor="rgba(0,0,0,0)",
              plot_bgcolor='rgba(0,0,0,0)',
        )
        fig.update_yaxes(
            title_text="Recovery (%)",
            showline=True, linecolor="black", 
            ticks="inside", tickwidth=1, tickcolor="black", ticklen=4,
        )
        fig.update_xaxes(
            title_text="Concentration",
            position=0.465, 
            showline=True, linecolor="black", 
            ticks="inside", tickwidth=1, tickcolor="black", ticklen=4,
        )


class ProfilePloter:

    canva_class = ProfilePlotCanvas

    def __init__(self, data: PloterData, **kwargs):
        self.profiles = data.profiles
        self.figures = []

        for key, value in kwargs.items():
            if not hasattr(self, key):
                raise TypeError("%s() received an invalid keyword %r. Only "
                                "arguments that are already attributes of the "
                                "class are accepted." % (self.__name__, key))
            else:
                setattr(self, key, value)

        for profile in self.profiles:
            self.figures.append(
                    self.canva_class(profile=profile).figure
                )
            # self.figures.append(fig_to_dict(
            #         self.canva_class(profile=profile).figure
            #     ))


# TEST_DATA = json.loads('{"width": 500.0, "height": 500.0, "axes": [{"bbox": [0.125, 0.10999999999999999, 0.775, 0.77], "xlim": [-0.5349384116779601, 12.895910836872632], "ylim": [10.4877921745567, 203.63074195898025], "xdomain": [-0.5349384116779601, 12.895910836872632], "ydomain": [10.4877921745567, 203.63074195898025], "xscale": "linear", "yscale": "linear", "axes": [{"position": "bottom", "nticks": 9, "tickvalues": null, "tickformat": null, "scale": "linear", "fontsize": 10.0, "grid": {"gridOn": false}, "visible": false}, {"position": "left", "nticks": 10, "tickvalues": null, "tickformat": null, "scale": "linear", "fontsize": 10.0, "grid": {"gridOn": false}, "visible": false}], "axesbg": "#FFFFFF", "axesbgalpha": null, "zoomable": true, "id": "el8952275645584", "lines": [{"data": "data01", "xindex": 0, "yindex": 1, "coordinates": "data", "id": "el8952275625840", "color": "#BF00BF", "linewidth": 2.0, "dasharray": "none", "alpha": 1, "zorder": 2, "drawstyle": "default"}, {"data": "data01", "xindex": 0, "yindex": 2, "coordinates": "data", "id": "el8952275627152", "color": "#0000FF", "linewidth": 1.0, "dasharray": "none", "alpha": 1, "zorder": 2, "drawstyle": "default"}, {"data": "data01", "xindex": 0, "yindex": 3, "coordinates": "data", "id": "el8952275626704", "color": "#007F00", "linewidth": 1.0, "dasharray": "none", "alpha": 1, "zorder": 2, "drawstyle": "default"}, {"data": "data01", "xindex": 0, "yindex": 4, "coordinates": "data", "id": "el8952275626128", "color": "#000000", "linewidth": 1.5, "dasharray": "5.550000000000001,2.4000000000000004", "alpha": 1, "zorder": 2, "drawstyle": "default"}, {"data": "data01", "xindex": 0, "yindex": 5, "coordinates": "data", "id": "el8952275624656", "color": "#000000", "linewidth": 1.5, "dasharray": "5.550000000000001,2.4000000000000004", "alpha": 1, "zorder": 2, "drawstyle": "default"}, {"data": "data03", "xindex": 0, "yindex": 1, "coordinates": "axes", "id": "el8952276660944", "color": "#BF00BF", "linewidth": 2.0, "dasharray": "none", "alpha": 1, "zorder": 1000002.0, "drawstyle": "default"}, {"data": "data03", "xindex": 0, "yindex": 2, "coordinates": "axes", "id": "el8952276660912", "color": "#0000FF", "linewidth": 1.0, "dasharray": "none", "alpha": 1, "zorder": 1000002.0, "drawstyle": "default"}, {"data": "data03", "xindex": 0, "yindex": 3, "coordinates": "axes", "id": "el8952276661808", "color": "#007F00", "linewidth": 1.0, "dasharray": "none", "alpha": 1, "zorder": 1000002.0, "drawstyle": "default"}, {"data": "data03", "xindex": 0, "yindex": 4, "coordinates": "axes", "id": "el8952276662672", "color": "#000000", "linewidth": 1.5, "dasharray": "5.550000000000001,2.4000000000000004", "alpha": 1, "zorder": 1000002.0, "drawstyle": "default"}], "paths": [{"data": "data05", "xindex": 0, "yindex": 1, "coordinates": "axes", "pathcodes": ["M", "L", "S", "L", "S", "L", "S", "L", "S", "Z"], "id": "el8952275626960", "dasharray": "none", "alpha": 0.8, "facecolor": "#FFFFFF", "edgecolor": "#CCCCCC", "edgewidth": 1.0, "zorder": 1000000.0}], "markers": [{"data": "data01", "xindex": 0, "yindex": 1, "coordinates": "data", "id": "el8952275625840pts", "facecolor": "#BF00BF", "edgecolor": "#BF00BF", "edgewidth": 1.0, "alpha": 1, "zorder": 2, "markerpath": [[[0.0, 1.5], [0.39780465000000004, 1.5], [0.7793698061772802, 1.3419505373823626], [1.0606601717798214, 1.0606601717798214], [1.3419505373823626, 0.7793698061772802], [1.5, 0.39780465000000004], [1.5, 0.0], [1.5, -0.39780465000000004], [1.3419505373823626, -0.7793698061772802], [1.0606601717798214, -1.0606601717798214], [0.7793698061772802, -1.3419505373823626], [0.39780465000000004, -1.5], [0.0, -1.5], [-0.39780465000000004, -1.5], [-0.7793698061772802, -1.3419505373823626], [-1.0606601717798214, -1.0606601717798214], [-1.3419505373823626, -0.7793698061772802], [-1.5, -0.39780465000000004], [-1.5, 0.0], [-1.5, 0.39780465000000004], [-1.3419505373823626, 0.7793698061772802], [-1.0606601717798214, 1.0606601717798214], [-0.7793698061772802, 1.3419505373823626], [-0.39780465000000004, 1.5], [0.0, 1.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]}, {"data": "data04", "xindex": 0, "yindex": 1, "coordinates": "axes", "id": "el8952276660976pts", "facecolor": "#BF00BF", "edgecolor": "#BF00BF", "edgewidth": 1.0, "alpha": 1, "zorder": 1000002.0, "markerpath": [[[0.0, 1.5], [0.39780465000000004, 1.5], [0.7793698061772802, 1.3419505373823626], [1.0606601717798214, 1.0606601717798214], [1.3419505373823626, 0.7793698061772802], [1.5, 0.39780465000000004], [1.5, 0.0], [1.5, -0.39780465000000004], [1.3419505373823626, -0.7793698061772802], [1.0606601717798214, -1.0606601717798214], [0.7793698061772802, -1.3419505373823626], [0.39780465000000004, -1.5], [0.0, -1.5], [-0.39780465000000004, -1.5], [-0.7793698061772802, -1.3419505373823626], [-1.0606601717798214, -1.0606601717798214], [-1.3419505373823626, -0.7793698061772802], [-1.5, -0.39780465000000004], [-1.5, 0.0], [-1.5, 0.39780465000000004], [-1.3419505373823626, 0.7793698061772802], [-1.0606601717798214, 1.0606601717798214], [-0.7793698061772802, 1.3419505373823626], [-0.39780465000000004, 1.5], [0.0, 1.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]}], "texts": [{"text": "Concentration", "position": [0.5, -0.14285714285714285], "coordinates": "axes", "h_anchor": "middle", "v_baseline": "hanging", "rotation": -0.0, "fontsize": 10.0, "color": "#000000", "alpha": 1, "zorder": 3, "id": "el8952275702224"}, {"text": "Recovery (%)", "position": [-0.16129032258064516, 0.5], "coordinates": "axes", "h_anchor": "middle", "v_baseline": "auto", "rotation": -90.0, "fontsize": 10.0, "color": "#000000", "alpha": 1, "zorder": 3, "id": "el8952275702672"}, {"text": "Recovery", "position": [0.6222580645161291, 0.938961038961039], "coordinates": "axes", "h_anchor": "start", "v_baseline": "auto", "rotation": -0.0, "fontsize": 10.0, "color": "#000000", "alpha": 1, "zorder": 1000003.0, "id": "el8952276660656"}, {"text": "Min tolerance limit", "position": [0.6222580645161291, 0.8845598845598845], "coordinates": "axes", "h_anchor": "start", "v_baseline": "auto", "rotation": -0.0, "fontsize": 10.0, "color": "#000000", "alpha": 1, "zorder": 1000003.0, "id": "el8952276661520"}, {"text": "Max tolerance limit", "position": [0.6222580645161291, 0.8301587301587301], "coordinates": "axes", "h_anchor": "start", "v_baseline": "auto", "rotation": -0.0, "fontsize": 10.0, "color": "#000000", "alpha": 1, "zorder": 1000003.0, "id": "el8952276662384"}, {"text": "Acceptance limit", "position": [0.6222580645161291, 0.7757575757575759], "coordinates": "axes", "h_anchor": "start", "v_baseline": "auto", "rotation": -0.0, "fontsize": 10.0, "color": "#000000", "alpha": 1, "zorder": 1000003.0, "id": "el8952276663248"}], "collections": [{"offsets": "data02", "xindex": 0, "yindex": 1, "paths": [[[[0.0, -0.5], [0.13260155, -0.5], [0.25978993539242673, -0.44731684579412084], [0.3535533905932738, -0.3535533905932738], [0.44731684579412084, -0.25978993539242673], [0.5, -0.13260155], [0.5, 0.0], [0.5, 0.13260155], [0.44731684579412084, 0.25978993539242673], [0.3535533905932738, 0.3535533905932738], [0.25978993539242673, 0.44731684579412084], [0.13260155, 0.5], [0.0, 0.5], [-0.13260155, 0.5], [-0.25978993539242673, 0.44731684579412084], [-0.3535533905932738, 0.3535533905932738], [-0.44731684579412084, 0.25978993539242673], [-0.5, 0.13260155], [-0.5, 0.0], [-0.5, -0.13260155], [-0.44731684579412084, -0.25978993539242673], [-0.3535533905932738, -0.3535533905932738], [-0.25978993539242673, -0.44731684579412084], [-0.13260155, -0.5], [0.0, -0.5]], ["M", "C", "C", "C", "C", "C", "C", "C", "C", "Z"]]], "pathtransforms": [[1.9641855032959654, 0.0, 0.0, 1.9641855032959654, 0.0, 0.0]], "alphas": [0.5], "edgecolors": ["#1F77B4"], "facecolors": ["#1F77B4"], "edgewidths": [1.0], "offsetcoordinates": "data", "pathcoordinates": "display", "zorder": 1, "id": "el8952275627856"}], "images": [], "sharex": [], "sharey": []}], "data": {"data01": [[0.10705926706676851, 107.0592670667685, 19.26701716475777, 194.85151696877918, 80.0, 120.0], [0.2534768755600624, 103.4599492081887, 72.23471277171892, 134.6851856446585, 80.0, 120.0], [1.8321502312465716, 101.78612395814287, 97.68902505596898, 105.88322286031675, 80.0, 120.0], [4.308305281739574, 101.49129050034334, 98.58012488340793, 104.40245611727875, 80.0, 120.0], [12.285417689211242, 100.33007504459977, 97.01994120218511, 103.64020888701444, 80.0, 120.0]], "data02": [[0.1, 150.23870130475865], [0.1, 164.2044156691515], [0.1, 162.02405175251482], [0.245, 123.7476576558001], [0.245, 125.63572466161577], [0.245, 118.15576200101607], [1.8, 101.51001897701843], [1.8, 99.06457140333525], [1.8, 104.91061792987166], [4.245, 99.77788469194076], [4.245, 99.6899308186617], [4.245, 103.18102724557794], [12.245, 98.69087920085299], [12.245, 97.88754581140527], [12.245, 98.5478463994901], [0.1, 81.01813361609008], [0.1, 64.94926399464977], [0.1, 68.29360969295118], [0.245, 80.94982408253605], [0.245, 98.88972959913248], [0.245, 88.76447929475535], [1.8, 100.48426044227597], [1.8, 98.19057295180336], [1.8, 99.03177971748904], [4.245, 104.8895801239783], [4.245, 100.56622839467731], [4.245, 99.51116896269393], [12.245, 102.15738926793969], [12.245, 100.65542403157323], [12.245, 103.51964444797319], [0.1, 138.25438340783091], [0.1, 135.96629184598788], [0.1, 135.31899635503467], [0.245, 113.6373754528812], [0.245, 114.53346642594768], [0.245, 111.44464734807089], [1.8, 105.86387533583486], [1.8, 104.69115612310931], [1.8, 102.88468679443632], [4.245, 100.3473786415646], [4.245, 103.08793921047688], [4.245, 100.0881188068568], [12.245, 99.62786513161129], [12.245, 99.50863544512012], [12.245, 98.56000431552151], [0.1, 56.48404363721161], [0.1, 60.506780654437506], [0.1, 67.45253287060346], [0.245, 92.90149148628556], [0.245, 88.47165430677825], [0.245, 84.38757818344527], [1.8, 103.42739824366218], [1.8, 100.76886676234476], [1.8, 100.60568281653346], [4.245, 103.66901335375125], [4.245, 100.88280973316517], [4.245, 102.20440602077514], [12.245, 101.07614738859479], [12.245, 103.0073336786498], [12.245, 100.72218541646507]], "data03": [[0.5218996415770609, 0.9515873015873016, 0.8971861471861472, 0.8427849927849927, 0.7883838383838385], [0.593584229390681, 0.9515873015873016, 0.8971861471861472, 0.8427849927849927, 0.7883838383838385]], "data04": [[0.557741935483871, 0.9515873015873016]], "data05": [[0.514731182795699, 0.7535353535353535], [0.974910394265233, 0.7535353535353535], [0.982078853046595, 0.7535353535353535], [0.982078853046595, 0.7607503607503607], [0.982078853046595, 0.9747474747474747], [0.982078853046595, 0.9819624819624819], [0.974910394265233, 0.9819624819624819], [0.514731182795699, 0.9819624819624819], [0.5075627240143369, 0.9819624819624819], [0.5075627240143369, 0.9747474747474747], [0.5075627240143369, 0.7607503607503607], [0.5075627240143369, 0.7535353535353535], [0.514731182795699, 0.7535353535353535]]}, "id": "el8952275644528", "plugins": [{"type": "reset"}, {"type": "zoom", "button": true, "enabled": false}, {"type": "boxzoom", "button": true, "enabled": false}]}')