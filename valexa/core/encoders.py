import json
import numpy
from matplotlib.figure import Figure
from mpld3.mpld3renderer import MPLD3Renderer
from mpld3.mplexporter import Exporter
from plotly.utils import PlotlyJSONEncoder


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    def default(self, obj):
        if isinstance(obj, (numpy.int_, numpy.intc, numpy.intp, numpy.int8,
            numpy.int16, numpy.int32, numpy.int64, numpy.uint8,
            numpy.uint16,numpy.uint32, numpy.uint64)):
            return int(obj)
        elif isinstance(obj, (numpy.float_, numpy.float16, numpy.float32, 
            numpy.float64)):
            return float(obj)
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


def fig_to_dict(fig: Figure, **kwargs) -> dict:
    """Output json-serializable dictionary representation of the figure

    **kwargs :
        Additional keyword arguments passed to mplexporter.Exporter
    """
    renderer = MPLD3Renderer()
    Exporter(renderer, close_mpl=False, **kwargs).run(fig)
    fig, figure_dict, extra_css, extra_js = renderer.finished_figures[0]
    return figure_dict

    
def fig_to_json(fig: Figure, encoder=NumpyEncoder) -> str:
    """Converts a matplotlib Figure to a Json string"""

    return json.dumps(fig_to_dict(fig), cls=encoder)