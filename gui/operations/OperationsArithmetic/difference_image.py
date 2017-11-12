from gui.operations.OperationsArithmetic.add_template import AddTemplate
from gui.tabpicture import TabPicture


class DifferenceImage(AddTemplate):
    def __init__(self, tab: TabPicture):
        super().__init__("Odejmowanie obrazów", tab)

    def control_plugin(self):
        pass

    def operation_command(self, preview):
        place = self.can.coords('img_f')
        self.vision_result.ar_diff(self.tab_fg.vision.cvImage.image, place, preview)
