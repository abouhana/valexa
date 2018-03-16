import os

import pytest

from valexa.core.xlsx import XlsxHandler


class TestXlsxHandler:
    @pytest.fixture(scope="class")
    def filename(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return os.path.join(dir_path, "data/test.xlsx")

    def test_handle_xlsx_on_init(self, filename):
        xs = XlsxHandler(filename)

        assert xs.workbook
