from queue import LifoQueue


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
        self.item = value
        self.stack.put_nowait(value)
        if not self.rstack.empty():
            self.rstack = LifoQueue()

        print("Updated {}".format(self.stack.qsize()))

    def redo(self):
        """
        Load next image
        :return:
        """
        if not self.rstack.empty():
            self.item = self.rstack.get_nowait()
        else:
            pass

    def undo(self):
        """
        Load previous image
        :return:
        """
        if self.stack.empty():
            pass
        else:
            self.rstack.put_nowait(self.item)
            self.item = self.stack.get()

    @property
    def redo_empty(self):
        return self.rstack.empty()

    @property
    def undo_empty(self):
        return self.stack.empty()
