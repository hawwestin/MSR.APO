from queue import LifoQueue


class Repeater:
    def __init__(self):
        self.__stack = LifoQueue()
        self.__rstack = LifoQueue()
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
        self.__stack.put_nowait(value)
        if not self.__rstack.empty():
            self.__rstack = LifoQueue()

        print("Updated {}".format(self.__stack.qsize()))

    def redo(self):
        """
        Load next image
        :return:
        """
        if not self.__rstack.empty():
            self.item = self.__rstack.get_nowait()
        else:
            pass

    def undo(self):
        """
        Load previous image
        :return:
        """
        if self.__stack.empty():
            pass
        else:
            self.__rstack.put_nowait(self.item)
            self.item = self.__stack.get()

    @property
    def redo_empty(self):
        return self.__rstack.empty()

    @property
    def undo_empty(self):
        return self.__stack.empty()
