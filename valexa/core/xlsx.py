import openpyxl


class XlsxHandler:
    def __init__(self, filename: str):
        self.workbook = openpyxl.load_workbook(filename=filename)
