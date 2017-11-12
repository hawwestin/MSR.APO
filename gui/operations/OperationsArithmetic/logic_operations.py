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


class LogicAnd(AddTemplate):
    def __init__(self, tab: TabPicture):
        super(LogicAnd, self).__init__("Logiczny And", tab)

    def control_plugin(self):
        pass

    def operation_command(self, preview):
        place = self.can.coords('img_f')
        self.vision_result.logic_and(self.tab_bg.vision.cvImage.image,
                                     self.tab_fg.vision.cvImage.image,
                                     place,
                                     preview)


class LogicXor(AddTemplate):
    def __init__(self, tab: TabPicture):
        super(LogicXor, self).__init__("Logiczny Xor", tab)

    def control_plugin(self):
        pass

    def operation_command(self, preview):
        place = self.can.coords('img_f')
        self.vision_result.logic_xor(self.tab_bg.vision.cvImage.image,
                                     self.tab_fg.vision.cvImage.image,
                                     place,
                                     preview)
