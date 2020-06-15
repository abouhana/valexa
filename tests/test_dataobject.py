import pandas as pd
import numpy as np
import pytest

from valexa.dataobject import DataObject


class TestDataObject:
    @pytest.fixture()
    def calibration_data( self ):
        return pd.DataFrame(
            [
                [1, 1, 0.1, 0.0131990354713203],
                [1, 1, 0.1, 0.0121580077483161],
                [1, 1, 0.1, 0.0128884326181805],
                [1, 2, 5, 0.681151835343229],
                [1, 2, 5, 0.679801900354773],
                [1, 2, 5, 0.679848238946098],
                [1, 3, 10, 1.3497717630804],
                [1, 3, 10, 1.38031766847637],
                [1, 3, 10, 1.36539234682978],
                [1, 4, 20, 2.75173441077979],
                [1, 4, 20, 2.75358268984679],
                [1, 4, 20, 2.7885735990718],
                [2, 1, 0.1, 0.0136248048536127],
                [2, 1, 0.1, 0.0140230069712878],
                [2, 1, 0.1, 0.0131695546390164],
                [2, 2, 5, 0.705403525496292],
                [2, 2, 5, 0.687118070660444],
                [2, 2, 5, 0.692335066650226],
                [2, 3, 10, 1.42351812984358],
                [2, 3, 10, 1.3482444417842],
                [2, 3, 10, 1.41418540356946],
                [2, 4, 20, 2.7798133637339],
                [2, 4, 20, 2.75673474145702],
                [2, 4, 20, 2.74364377966984],
                [3, 1, 0.1, 0.0131589924950808],
                [3, 1, 0.1, 0.0140116689218943],
                [3, 1, 0.1, 0.0147452233128681],
                [3, 2, 5, 0.725752822269548],
                [3, 2, 5, 0.731510840529777],
                [3, 2, 5, 0.742348790890809],
                [3, 3, 10, 1.461947767082],
                [3, 3, 10, 1.4735790753879],
                [3, 3, 10, 1.45388648982298],
                [3, 4, 20, 2.95467913585596],
                [3, 4, 20, 2.96259166421757],
                [3, 4, 20, 2.94563585509296],
                [4, 1, 0.1, 0.0137769810364108],
                [4, 1, 0.1, 0.0125886619171235],
                [4, 1, 0.1, 0.0138757512257883],
                [4, 2, 5, 0.660585701171955],
                [4, 2, 5, 0.667743153026165],
                [4, 2, 5, 0.634041243357693],
                [4, 3, 10, 1.34709970412085],
                [4, 3, 10, 1.29979477004593],
                [4, 3, 10, 1.27408689795716],
                [4, 4, 20, 2.57202007153029],
                [4, 4, 20, 2.62481794644455],
                [4, 4, 20, 2.58657308272152],
            ],
            columns=["Serie", "Level", "x", "y"],
        )

    @pytest.fixture()
    def validation_data( self ):
        return pd.DataFrame(
            [
                [1, 1, 0.1, 0.0123186375477679],
                [1, 1, 0.1, 0.0142510326427342],
                [1, 1, 0.1, 0.0139493420576473],
                [1, 2, 0.245, 0.0334809219214063],
                [1, 2, 0.245, 0.0341209753943783],
                [1, 2, 0.245, 0.0315852729728695],
                [1, 3, 1.8, 0.24435215303244],
                [1, 3, 1.8, 0.238261503179844],
                [1, 3, 1.8, 0.252821709989549],
                [1, 4, 4.245, 0.577594160575005],
                [1, 4, 4.245, 0.577077547450487],
                [1, 4, 4.245, 0.597583139368881],
                [1, 5, 12.245, 1.66365492538354],
                [1, 5, 12.245, 1.65004400859936],
                [1, 5, 12.245, 1.66123151365644],
                [2, 1, 0.1, 0.0161160291949673],
                [2, 1, 0.1, 0.0138983422744785],
                [2, 1, 0.1, 0.014359900049695],
                [2, 2, 0.245, 0.0323059976116102],
                [2, 2, 0.245, 0.0383719799832885],
                [2, 2, 0.245, 0.0349483504776391],
                [2, 3, 1.8, 0.254558096171836],
                [2, 3, 1.8, 0.248860106480675],
                [2, 3, 1.8, 0.250949836445599],
                [2, 4, 4.245, 0.619438937585894],
                [2, 4, 4.245, 0.59411022173183],
                [2, 4, 4.245, 0.587929068257607],
                [2, 5, 12.245, 1.73134277663237],
                [2, 5, 12.245, 1.70596032435095],
                [2, 5, 12.245, 1.7543641996754],
                [3, 1, 0.1, 0.0149763345245691],
                [3, 1, 0.1, 0.0146382428938148],
                [3, 1, 0.1, 0.0145425976006955],
                [3, 2, 0.245, 0.0356861577325312],
                [3, 2, 0.245, 0.0360105565089741],
                [3, 2, 0.245, 0.0348923562819505],
                [3, 3, 1.8, 0.27611438709365],
                [3, 3, 1.8, 0.272995299537074],
                [3, 3, 1.8, 0.268190623410634],
                [3, 4, 4.245, 0.623973771750776],
                [3, 4, 4.245, 0.641163860549282],
                [3, 4, 4.245, 0.622347571756852],
                [3, 5, 12.245, 1.79715293360601],
                [3, 5, 12.245, 1.79499566505565],
                [3, 5, 12.245, 1.77783171736778],
                [4, 1, 0.1, 0.0117623771526985],
                [4, 1, 0.1, 0.0122839860778568],
                [4, 1, 0.1, 0.0131846082990898],
                [4, 2, 0.245, 0.0339512808197785],
                [4, 2, 0.245, 0.0325440114979611],
                [4, 2, 0.245, 0.031246583442835],
                [4, 3, 1.8, 0.2458351458209],
                [4, 3, 1.8, 0.23963020441768],
                [4, 3, 1.8, 0.239249337450777],
                [4, 4, 4.245, 0.575062360858099],
                [4, 4, 4.245, 0.559726296625267],
                [4, 4, 4.245, 0.567000741826223],
                [4, 5, 12.245, 1.60927504165907],
                [4, 5, 12.245, 1.63993745480924],
                [4, 5, 12.245, 1.60365500992791],
            ],
            columns=["Serie", "Level", "x", "y"],
        )

    @pytest.fixture()
    def calculated_data( self ):
        return pd.DataFrame(
            [
                0.0971882842930686,
                0.111145506906756,
                0.108966468744488,
                0.250038348333509,
                0.254661299835613,
                0.236346534252087,
                1.77311027244765,
                1.72911898097928,
                1.83428383483021,
                4.18003673154468,
                4.17630535983771,
                4.32441229302957,
                12.024391080151,
                11.9260827186632,
                12.0068873631069,
                0.124615926139905,
                0.108598109639877,
                0.111931829868497,
                0.241552154082253,
                0.285365278299325,
                0.260637230043763,
                1.84682533245284,
                1.80567013040478,
                1.8207637447484,
                4.48227143990347,
                4.29932824851632,
                4.25468327126822,
                12.5132840661573,
                12.3299527495462,
                12.6795622393593,
                0.116384187057242,
                0.113942232942085,
                0.11325141011217,
                0.265966233480662,
                0.268309287419381,
                0.260232797504923,
                2.00252121053952,
                1.97999279515898,
                1.94528978103,
                4.51502545077851,
                4.63918530645957,
                4.50327980135687,
                12.9886149203473,
                12.9730334911286,
                12.84906244637,
                0.0931705499356458,
                0.0969380051029068,
                0.103442981681106,
                0.253435636947007,
                0.243271270843418,
                0.233900261654971,
                1.78382157084462,
                1.73900477913612,
                1.73625386910891,
                4.16175015425302,
                4.05098146979867,
                4.10352302888526,
                11.6316183263669,
                11.8530855239004,
                11.5910261958175,
            ],
            columns=["x_calc"],
        )

    @pytest.fixture()
    def test_object_with_calib( self, validation_data, calibration_data ):
        return DataObject(validation_data, calibration_data)

    @pytest.fixture()
    def test_object_without_calib( self, validation_data ):
        return DataObject(validation_data)

    def test_create_dataobject_with_calibration( self, test_object_with_calib ):
        assert isinstance(test_object_with_calib, DataObject)
        assert test_object_with_calib.calibration_data is not None

    def test_create_dataobject_without_calibration( self, test_object_without_calib ):
        assert isinstance(test_object_without_calib, DataObject)
        assert test_object_without_calib.calibration_data is None

    def test_add_calculated_value( self, calculated_data, test_object_with_calib ):
        test_object_with_calib.add_calculated_value(calculated_data)
        assert test_object_with_calib.validation_data["x_calc"] is not None

    def test_get_level( self, test_object_with_calib ):
        assert isinstance(test_object_with_calib.get_level(1), pd.DataFrame)
        assert isinstance(test_object_with_calib.get_level(1, "calibration"), pd.DataFrame)
        assert test_object_with_calib.get_level(1, "") is None

    def test_get_serie( self, test_object_with_calib ):
        assert isinstance(test_object_with_calib.get_serie(1), pd.DataFrame)
        assert isinstance(test_object_with_calib.get_serie(1, "calibration"), pd.DataFrame)
        assert test_object_with_calib.get_serie(1, "") is None

    def test_data_x( self, test_object_with_calib, validation_data, calibration_data ):
        assert test_object_with_calib.data_x().equals(validation_data["x"])
        assert test_object_with_calib.data_x("calibration").equals(calibration_data["x"])
        assert test_object_with_calib.data_x("") is None

    def test_data_x_calc(
            self, test_object_with_calib, test_object_without_calib, calculated_data
    ):
        test_object_with_calib.add_calculated_value(calculated_data)
        assert test_object_without_calib.data_x_calc is None
        assert test_object_with_calib.data_x_calc.equals(calculated_data["x_calc"])

    def test_data_y( self, test_object_with_calib, validation_data, calibration_data ):
        assert test_object_with_calib.data_y().equals(validation_data["y"])
        assert test_object_with_calib.data_y("calibration").equals(calibration_data["y"])
        assert test_object_with_calib.data_y("") is None

    def test_list_of_series( self, test_object_with_calib ):
        assert isinstance(test_object_with_calib.list_of_series(), np.ndarray)
        assert isinstance(test_object_with_calib.list_of_series("calibration"), np.ndarray)
        assert test_object_with_calib.list_of_series("") is None

    def test_list_of_levels( self, test_object_with_calib ):
        assert isinstance(test_object_with_calib.list_of_levels(), np.ndarray)
        assert isinstance(test_object_with_calib.list_of_levels("calibration"), np.ndarray)
        assert test_object_with_calib.list_of_levels("") is None

    def test_add_corrected_value(self, test_object_with_calib, calculated_data):
        test_object_with_calib.add_calculated_value(calculated_data)
        test_object_with_calib.add_corrected_value(calculated_data+1)
        assert test_object_with_calib.data_x_calc.equals(calculated_data["x_calc"]+1)
