import tkinter as tk


class ImageData:

    def __init__(self):
        self.frames = {}


    def Open_img(self, path):
        # get last id from dict frames
        last = self.frames.values()

        print(last)

        # self.add_img()

    def add_img(self, container, tkk):
        frame = ImageObject(container, tkk)
        # idki z dlugosci to zly pomysl bo po usunieciu potrzeba przepisac dict

        if self.frames.__len__() is 0:
            item = 0
        else:
            item = sorted(self.frames)[-1]+1
        print("\nitem : %d"% item)
        self.frames[item] = frame

        # frame.grid(row=0, column=0, sticky="nsew")

    def close_img(self, img):
        self.frames.pop(img)
        item = sorted(self.frames)[-1] + 1
        print("\nitem after close : %d"% item)


class ImageObject(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.image = None

    def doddd(self):
        print("donothing")


ooo = tk.Tk()

container = tk.Frame()

a = ImageData()
a.Open_img("bbb.txt")
a.add_img(container, ooo)
a.Open_img("bbb.txt")
a.add_img(container, ooo)
a.Open_img("asd")
a.add_img(container, ooo)
a.Open_img("asd")
a.close_img(1)
a.Open_img("asd")
a.frames[0].doddd()
a.frames[2].doddd()
print(a.frames.keys())
