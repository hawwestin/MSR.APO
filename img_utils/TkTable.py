import copy
import tkinter as tk
from pprint import pprint

import numpy as np
from img_utils.tk_scrolled_frame import ScrolledFrame
from img_utils.scrolled_canvas import ScrolledCanvas


class TkTable(tk.Frame):
    """
    Tkinter table sth like Excel matrix.

    raw_kernel = [][] Table with tk.StringVar()
    np_kernel = [][] np.array
    """

    def __init__(self, parent, size):
        super(TkTable, self).__init__(parent)
        self.master = parent
        self.table = ScrolledFrame(parent)
        self.table.pack(fill=tk.BOTH, expand=True)
        self.excel = self.table.interior

        self.raw_kernel = []
        self.size = size

    def draw(self, values=None):
        """
        Searching order is by columns from left to right.
        :param values: Table[][] with valid values
        :return:
        """
        bucket = list(self.excel.children.values())
        try:
            for child in bucket:
                child.destroy()
        except Exception as e:
            pprint(e)

        self.raw_kernel = []
        for x in range(self.size[0]):
            matrix_row = []
            for y in range(self.size[1]):
                value = values[x][y] if values is not None else 0
                buk = Bucket(table=self, x=x, y=y, value=value)
                buk.bucket.grid(column=x, row=y, padx=2, pady=2)
                matrix_row.append(buk.value)
            self.raw_kernel.append(copy.copy(matrix_row))

    def get_values(self):
        """
        Get Values from table
        :return: np.array
        """
        _x, _y = self.size
        np_kernel = np.zeros((_x, _y))
        for x in range(_x):
            for y in range(_y):
                np_kernel[x][y] = self.raw_kernel[x][y].get()
        return np_kernel


class Bucket:
    def __init__(self, table: TkTable, x, y, value):
        self.x = x
        self.y = y
        self.value = tk.StringVar()
        self.value.set(value)
        self.bucket = tk.Entry(table.excel, textvariable=self.value, width=3)
        vcmd = self.bucket.register(self.check_entry)
        self.bucket.configure(validate='key', validatecommand=(vcmd, '%d', '%S'))

    @staticmethod
    def check_entry(why, what):
        if int(why) >= 0:
            if what in '0123456789-.':
                return True
            else:
                return False
        else:
            return True


if __name__ == '__main__':
    pass
