from OperationsArithmetic.operation_template import OperationTemplate
from tabpicture import TabPicture


class AddImage(OperationTemplate):
    def __init__(self, tab: TabPicture):
        super().__init__("Dodawanie obrazów", tab)
        pass
