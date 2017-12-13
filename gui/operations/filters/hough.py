"""
Detekcja krawędzi (z ograniczeniem do odcinków linii prostych) z wykorzystaniem transformacji Hough'a (HOUGH)

A
    Wizualizacja tablic akumulatorów,
-   zadawanie parametrów z użyciem suwaka przy jednoczesnym  podglądzie tablicy
    akumulatorów oraz konturu wynikowego ,
X   obrazy bmp, (tworzone, przetworzone),
    tablice,
-   działanie na bmp oraz na tablicach,
-   eksport tablicy pikseli do Excela,
    Programy /:P Hough 1, 2,
    - histogram,
-   suwak oraz konkretny poziom szarości,
-   kąt;
    tablica akumulatorów w formie liczbowej
X   - redukcja fragmentów prostych
    (wyznaczonych z wykorzystaniem transformaty Hougha) leżących poza wykrywanym konturem.

B
-   Zadanie  (automatyczne lub manualne) parametrów pozwalających na jak najbardziej efektywną
    realizację transformacji w **danej klasie**.

-   Interaktywne zaznaczanie obszaru w obrazie bmp wizualizującym tablicę akumulatorów w
    celu wyświetlenia żądanej części tej tablicy.

X   Informacja o dopuszczalnym zakresie zmian poziomów szarości.

-   Optymalny zakres parametrów z punktu widzenia dokładności aproksymacji
"""
from gui.operations.matlib_template import MatLibTemplate
import copy
import tkinter as tk


class Hough(MatLibTemplate):
    def __init__(self, tab):
        super(Hough, self).__init__("Hough Transform", tab)

        self.th1 = tk.IntVar()
        self.th2 = tk.IntVar()
        self.th3 = tk.IntVar()
        self.apertureSize = tk.IntVar()
        self.prob = tk.BooleanVar()

        self.operation_options()
        self.controls()
        self.window.mainloop()

    def operation_options(self):
        self.lf_bottom.configure(text='Opcje')

        acc = tk.Button(self.lf_bottom, text="Show probabilistic Hough space\nSlow",
                        command=self.vision_result.hough_accumulator)
        acc.pack(side=tk.TOP, anchor='nw')

        probabilist = tk.Checkbutton(self.lf_bottom, variable=self.prob, text='Probabilistc Hough')
        probabilist.pack(side=tk.TOP, anchor='nw')

    def controls(self):
        # todo validate whole input not last digit.
        def check_entry(why, what):
            if int(why) >= 0:
                if 3 <= int(what) <= 7 and int(what) % 2 == 1:
                    return True
                else:
                    return False
            else:
                return True

        label_1 = tk.Label(self.plugins, text="dolny próg szarości")
        label_1.pack(side=tk.LEFT, padx=2)

        entry_1 = tk.Entry(self.plugins, textvariable=self.th1, width=10)
        entry_1.pack(side=tk.LEFT, padx=2)

        label_2 = tk.Label(self.plugins, text="górny próg szarości")
        label_2.pack(side=tk.LEFT, padx=2)

        entry_2 = tk.Entry(self.plugins, textvariable=self.th2, width=10)
        entry_2.pack(side=tk.LEFT, padx=2)

        label_2 = tk.Label(self.plugins, text="min. wartość akumulatora")
        label_2.pack(side=tk.LEFT, padx=2)

        entry_3 = tk.Entry(self.plugins, textvariable=self.th3, width=10)
        entry_3.pack(side=tk.LEFT, padx=2)

        label_4 = tk.Label(self.plugins, text="apertureSize \nwartości (3, 5, 7) :")
        label_4.pack(side=tk.LEFT, padx=2)

        entry_4 = tk.Entry(self.plugins,
                           textvariable=self.apertureSize,
                           width=10)
        vcmd = entry_4.register(check_entry)
        entry_4.configure(validate='key', validatecommand=(vcmd, '%d', '%S'))
        entry_4.pack(side=tk.LEFT)

        self.th1.set(50)
        self.th2.set(150)
        self.th3.set(200)
        self.apertureSize.set(3)

    def operation_command(self, persist=False):
        try:
            if self.prob.get():
                lines, self.img_result = self.vision_result.houghProbabilistic(self.th1.get(),
                                                                               self.th2.get(),
                                                                               self.th3.get(),
                                                                               self.apertureSize.get())
            else:
                lines, self.img_result = self.vision_result.hough(self.th1.get(),
                                                                  self.th2.get(),
                                                                  self.th3.get(),
                                                                  self.apertureSize.get())
            self.status_message.set("Count of liens found in picture {}".format(lines))
        except TypeError:
            self.status_message.set("Any lines have been found on given image with current threshold")
            self.img_result = self.tab_bg.vision.cvImage.image
        else:
            if persist:
                self.vision_result.cvImage.image = copy.copy(self.vision_result.cvImage_tmp.image)

        self.draw_result()


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    min_val, max_val = 0, 50

    intersection_matrix = np.random.randint(0, 10, size=(max_val, max_val))


    # ax.matshow(intersection_matrix)

    def petla():
        for i in range(max_val):
            for j in range(max_val):
                c = intersection_matrix[j, i]
                ax.text(i + 0.5, j + 0.5, str(c), va='center', ha='center')


    petla()

    ax.set_xlim(min_val, max_val)
    ax.set_ylim(min_val, max_val)
    ax.set_xticks(np.arange(max_val))
    ax.set_yticks(np.arange(max_val))
    ax.grid()

    plt.waitforbuttonpress()
