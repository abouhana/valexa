from valexa.core.profiles import DEFAULT_TOLERANCE, DEFAULT_ACCEPTANCE
from valexa.gui.app import AppState


class TestAppState:

    def test_reset_state(self):
        state = AppState()
        state.tolerance_limit = 90
        state.acceptance_limit = 40
        state.valid_data = [2, 3, 4]
        state.calib_data = [2, 3, 4]

        state.reset()

        assert not state.calib_data
        assert not state.valid_data
        assert state.tolerance_limit == DEFAULT_TOLERANCE
        assert state.acceptance_limit == DEFAULT_ACCEPTANCE
