from gui.operations.OperationsArithmetic.add_template import AddTemplate
from gui.tabpicture import TabPicture


class LogicOr(AddTemplate):
    def __init__(self, tab: TabPicture):
        super(LogicOr, self).__init__("Logiczny Or", tab)

    def control_plugin(self):
        pass

    def operation_command(self, preview):
        place = self.can.coords('img_f')
        self.vision_result.logic_or(self.tab_bg.vision.cvImage.image,
                                    self.tab_fg.vision.cvImage.image,
                                    place,
                                    preview)
