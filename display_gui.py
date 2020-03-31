import tkinter as tk
from tkinter import ttk
# https://pythonprogramming.net/change-show-new-frame-tkinter/
# https://www.tutorialspoint.com/python/python_gui_programming.htm
# https://pythonprogramming.net/styling-gui-bit-using-ttk/?completed=/change-show-new-frame-tkinter/
from analysis import Analysis
LARGE_FONT = ("Verdana", 12)


class MainClass(tk.Tk):
    """ This class should be left alone !!!"""
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Reddit Analysis")
        tk.Tk.geometry(self, "600x400")
        container = tk.Frame(self, height=100, width=100)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    """ Main page, use it only for presentation and page buttons """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Reddit Analysis", font=LARGE_FONT)
        label.pack(pady=5, padx=10)
        text1 = tk.Label(self, text="Hello, use the bottom buttons to navegate pages.\n :)")
        text1.pack(padx=100)

        button1 = ttk.Button(self, text="Analysis from the daily data",
                           command=lambda: controller.show_frame(PageOne))
        button1.pack()

        button2 = ttk.Button(self, text="Analysis from profiles",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        useless_button = tk.Button(self, text="I Am Useless", command=lambda: print("<3"))
        useless_button.place(x=300, y=150)


class PageOne(tk.Frame):  # Daily data analysis (liams part)
    """ Page 1, daily data analysis """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Page settings
        label = tk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.place(x=0)

        button2 = ttk.Button(self, text="Page Two", command=lambda: controller.show_frame(PageTwo))
        button2.place(x=0, y=25)

        # Buttons that call other analysis functions
        an = Analysis(r'C:\Users\laptop\Desktop\RedditAnalysis\RedditAnalysis')

        scatter_button = ttk.Button(self, text="Scatter plots")
        scatter_button.place(x=100, y=100)





class PageTwo(tk.Frame):  # Profile data analysis (Burek this is urs)
    """ Page 2, user profiles analysis """
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button1.place(x=0)

        button2 = ttk.Button(self, text="Page One", command=lambda: controller.show_frame(PageOne))
        button2.place(x=0, y=25)


app = MainClass()
app.mainloop()


