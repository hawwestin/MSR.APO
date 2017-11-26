from gui.operations.add_template import AddTemplate
from gui.tabpicture import TabPicture
from img_utils.rect_tracker import RectTracker


class Substraction(AddTemplate):
    def __init__(self, tab: TabPicture):
        self.rect = None
        super(Substraction, self).__init__("Wycinanie fragmentów", tab)

    def control_plugin(self):
        """
        Mock method to be filled by concrete operation.
        :return:
        """
        self.rect = RectTracker(self.can)

    def operation_command(self, preview):
        place = self.can.coords('img_f')
        self.vision_result.image_cut(place=place)
        if preview:
            self.vision_result.preview()
