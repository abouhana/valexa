import pytest

from core.models import ModelsManager
from examples.dataset.sample_dataset import dataset
from core.dataobject import DataObject

class TestModelsManager:

    @pytest.fixture()
    def test_modelsmanager_hardcoded( self ):
        return ModelsManager()

    @pytest.fixture()
    def test_data( self ):
        data = dataset("feinberg_nicotinamide")
        return DataObject(data["Validation"], data["Calibration"])

    @pytest.fixture()
    def test_data_no_calib( self ):



    def test_modelsmanager_initialize( self, test_modelsmanager_hardcoded ):
        assert isinstance(test_modelsmanager_hardcoded, ModelsManager)

    def test_initialize_models_single( self , test_modelsmanager_hardcoded):
        test_modelsmanager_hardcoded.initialize_models("Linear")
        assert test_modelsmanager_hardcoded.initialized_models_list == ["Linear"]

    def test_initialize_models_multiple( self, test_modelsmanager_hardcoded ):
        test_modelsmanager_hardcoded.initialize_models(["Linear", "Quadratic"])
        assert test_modelsmanager_hardcoded.initialized_models_list == ["Linear", "Quadratic"]

    def test_initialize_models_all( self , test_modelsmanager_hardcoded):
        test_modelsmanager_hardcoded.initialize_models()
        assert test_modelsmanager_hardcoded.initialized_models_list == list(test_modelsmanager_hardcoded.get_available_models().keys())

    def test_initialize_model_none( self, test_modelsmanager_hardcoded ):
        with pytest.warns(UserWarning):
            test_modelsmanager_hardcoded.initialize_models("")

    def test_modelize( self, test_modelsmanager_hardcoded, test_data ):
        test_modelsmanager_hardcoded.initialize_models("Linear")
        test_modelsmanager_hardcoded.modelize("Linear", test_data)
        assert test_modelsmanager_hardcoded.models["Linear"] is not None

    def test_get_available_models( self, test_modelsmanager_hardcoded ):
        assert type(test_modelsmanager_hardcoded.get_available_models()) == dict

    def test_get_model_weight( self, test_modelsmanager_hardcoded ):
        assert type(test_modelsmanager_hardcoded.get_model_weight("1/X Weighted Linear")) == str
        with pytest.warns(UserWarning):
            test_modelsmanager_hardcoded.get_model_weight("")

    def test_get_model_formula( self, test_modelsmanager_hardcoded ):
        assert type(test_modelsmanager_hardcoded.get_model_formula("Linear")) == str
        with pytest.warns(UserWarning):
            test_modelsmanager_hardcoded.get_model_formula("")

    def test_get_model_info( self, test_modelsmanager_hardcoded ):
        assert type(test_modelsmanager_hardcoded.get_model_info("Linear")) == dict
        with pytest.warns(UserWarning):
            test_modelsmanager_hardcoded.get_model_info("")

    def test_number_of_models( self, test_modelsmanager_hardcoded ):
        assert type(test_modelsmanager_hardcoded.number_of_models) == int

    def test_initialized_models_list( self ):
        assert True
