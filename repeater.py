from queue import LifoQueue
import utils


class Repeater:
    def __init__(self):
        self.stack = LifoQueue()
        self.rstack = LifoQueue()
        self.item = None

    def current(self):
        """
        Current version of image
        :return:
        """
        return self.item

    def update(self, value):
        """
        Set new version of image
        :param value:
        :return:
        """
        if self.item is not None:
            self.stack.put_nowait(self.item)

        if not self.rstack.empty():
            self.rstack = LifoQueue()

        self.item = value

    def redo(self):
        """
        Load next image
        :return:
        """
        if self.rstack.empty():
            utils.status_message.set("Nothing to Redo")
            return
        elif self.item is not None:
            self.stack.put_nowait(self.item)
            self.item = self.rstack.get_nowait()

    def undo(self):
        """
        Load previous image
        :return:
        """
        if self.stack.empty():
            utils.status_message.set("Nothing to Undo")
            return
        else:
            self.rstack.put_nowait(self.item)
            self.item = self.stack.get()

    @property
    def redo_empty(self):
        return self.rstack.empty()

    @property
    def undo_empty(self):
        return self.stack.empty()
