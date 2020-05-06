from valexa.core.profiles import ProfileManager
from valexa.core.optimizer import Optimizer

import collections
import pandas as pd
import time

def test_data():
    calib = pd.DataFrame([
        [1, 1, 0.98, 5],
        [1, 2, 3.9, 13],
        [1, 3, 15.635, 58],
        [1, 4, 62.5, 230],
        [1, 5, 250, 890],
        [1, 6, 500, 1616],
        [1, 7, 1000, 3310],
        [1, 1, 0.98, 5],
        [1, 2, 3.9, 19],
        [1, 3, 15.635, 57],
        [1, 4, 62.5, 219],
        [1, 5, 250, 898],
        [1, 6, 500, 1623],
        [1, 7, 1000, 3294],
        [1, 1, 0.98, 6],
        [1, 2, 3.9, 16],
        [1, 3, 15.635, 63],
        [1, 4, 62.5, 230],
        [1, 5, 250, 887],
        [1, 6, 500, 1660],
        [1, 7, 1000, 3298]
    ], columns=["Serie", "Level", "x", "y"])

    valid = pd.DataFrame([
        [1, 1, 0.7765, 6],
        [1, 2, 1.563, 8],
        [1, 3, 6.25, 25],
        [1, 4, 25, 93],
        [1, 5, 100, 348],
        [1, 1, 0.7765, 7],
        [1, 2, 1.563, 12],
        [1, 3, 6.25, 25],
        [1, 4, 25, 96],
        [1, 5, 100, 350],
        [1, 1, 0.7765, 9],
        [1, 2, 1.563, 13],
        [1, 3, 6.25, 27],
        [1, 4, 25, 89],
        [1, 5, 100, 349],
        [2, 1, 0.7765, 5],
        [2, 2, 1.563, 11],
        [2, 3, 6.25, 28],
        [2, 4, 25, 91],
        [2, 5, 100, 332],
        [2, 1, 0.7765, 5],
        [2, 2, 1.563, 11],
        [2, 3, 6.25, 31],
        [2, 4, 25, 92],
        [2, 5, 100, 329],
        [2, 1, 0.7765, 6],
        [2, 2, 1.563, 13],
        [2, 3, 6.25, 26],
        [2, 4, 25, 90],
        [2, 5, 100, 333],
        [2, 1, 0.7765, 3],
        [2, 2, 1.563, 8],
        [2, 3, 6.25, 25],
        [2, 4, 25, 94],
        [2, 5, 100, 333],
        [2, 1, 0.7765, 4],
        [2, 2, 1.563, 12],
        [2, 3, 6.25, 32],
        [2, 4, 25, 98],
        [2, 5, 100, 351],
        [2, 1, 0.7765, 9],
        [2, 2, 1.563, 10],
        [2, 3, 6.25, 34],
        [2, 4, 25, 97],
        [2, 5, 100, 345],
        [3, 1, 0.7765, 7],
        [3, 2, 1.563, 6],
        [3, 3, 6.25, 24],
        [3, 4, 25, 98],
        [3, 5, 100, 370],
        [3, 1, 0.7765, 6],
        [3, 2, 1.563, 9],
        [3, 3, 6.25, 27],
        [3, 4, 25, 95],
        [3, 5, 100, 361],
        [3, 1, 0.7765, 6],
        [3, 2, 1.563, 12],
        [3, 3, 6.25, 21],
        [3, 4, 25, 101],
        [3, 5, 100, 364]
    ], columns=["Serie", "Level", "x", "y"])

    return {"Calibration": calib, "Validation": valid}


if __name__ == '__main__':
    start_time = time.time()
    profiles: ProfileManager = ProfileManager("Test", test_data(), rolling_data=False, acceptance_limit=25, generate_figure=True)
    print("--- %s seconds ---" % (time.time() - start_time))
    profiles.make_profiles("Linear")
    print("--- %s seconds ---" % (time.time() - start_time))
    optimizer_parameter = collections.OrderedDict({
        "has_limits": True,
        "min_loq": "min",
        "model.fit.rsquared": "max",
        "model.data.calibration_levels": "max",
        "max_loq": "max"
    })
    aa = Optimizer(profiles, optimizer_parameter)

    exit()
    # app = QApplication(sys.argv)
    # window = ValexaApp(state)
    # window.show()
    # app.exec_()
