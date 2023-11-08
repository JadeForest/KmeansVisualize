import time
import threading
from tkinter import *
from tkinter import messagebox

from data import get_sample_data, generate_data, Kmeans

# Window size
WWIDTH = 720
WHEIGHT = 570
# Colors
COLOR_LIST = ['#5CE600', '#1700E6', '#0AFFFF', '#E68A00', '#00CFE6',
              '#61A0FF', '#FFA724', '#F09000', '#D175A3', '#993366',
              '#0066CC', '#E600CF', '#6600CC', '#CC00CC', '#800080']
MAX_K = len(COLOR_LIST)


class App(Tk):
    def __init__(self):
        super().__init__()
        self.data = get_sample_data()
        self.window_init()
        self.widgets_init()

    def to_default(self):
        self.data = get_sample_data()
        self.draw_points()

    def to_random(self):
        self.data = generate_data()
        self.draw_points()

    def window_init(self):
        self.title('Clustering demo (K-means)')
        window_width, window_height = WWIDTH, WHEIGHT
        x = (self.winfo_screenwidth() - window_width)/2
        y = (self.winfo_screenheight() - window_height)/2
        self.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))
        self.resizable(0, 0)


    def widgets_init(self):
        # Menu
        self.menu = Menu(self)
        self.data_select = Menu(self.menu)
        self.menu.add_cascade(label='Options', menu=self.data_select)
        self.data_select.add_command(label='Use default data (from data.txt)', command=self.to_default)
        self.data_select.add_command(label='Use random generated data', command=self.to_random)
        self.data_select.add_separator()
        self.data_select.add_command(label='Exit', command=self.quit)
        self.config(menu=self.menu)

        # Canvas
        self.fm1 = Frame(self)
        self.fig = Canvas(self.fm1, width=500, height=500, background='white')
        self.draw_points()
        self.fig.pack(side=LEFT)

        self.legend = Canvas(self.fm1, width=150,
                             height=80, background='white')
        self.legend.create_rectangle(37-4, 40-4, 37+4, 40+4,
                                     width=0, fill='red')
        self.legend.create_text(75, 40, text='Centroids')
        self.legend.pack(side=RIGHT)
        self.fm1.pack(side=TOP)

        # Tips
        self.tip = Label(self, text=f'K must less than {MAX_K}, better be 2~5.')
        self.tip.pack()

        # Input and Button
        self.fm2 = Frame(self)
        self.tip2 = Label(self.fm2,text='K=')
        self.tip2.pack(side=LEFT)
        self.kstr = StringVar()
        self.ety = Entry(self.fm2, width=10, textvariable=self.kstr)
        self.ety.pack(side=LEFT)
        self.btn = Button(self.fm2, text='Run', width=10,
                          height=1, command=self.run_calc)
        self.btn.pack(side=RIGHT)
        self.fm2.pack(side=BOTTOM)


    def run_calc(self):
        # Handle input
        kget:str = self.kstr.get()

        try:
            K = int(kget) if len(kget)>0 else 1
            if K < 1: raise ValueError
        except ValueError:
            messagebox.showerror(title='Input Error', message='Positive integer expected for K.')
            return
        
        if K > MAX_K:
            self.highlight_tip(True)
            return
        else:
            self.highlight_tip(False)
            
        # Calculate and Draw
        self.disable_btn(True)
        drawing = threading.Thread(target=self.calc_and_draw, args=(K,))
        drawing.start()


    def calc_and_draw(self, K):
        for labels, centers in Kmeans(K, self.data):
            self.draw_points(labels)
            self.draw_centers(centers)
            time.sleep(0.5)
        self.disable_btn(False)

    def draw_points(self, labels=None):
        self.fig.delete(ALL)

        if labels == None:
            labels = [0] * len(self.data)

        for i in range(len(self.data)):
            x, y = self.data[i]
            self.fig.create_oval(x-3, y-3, x+3, y+3, width=0,
                                 fill=COLOR_LIST[labels[i]])

    def draw_centers(self, centers):
        for x, y in centers:
            self.fig.create_rectangle(x-4, y-4, x+4, y+4, width=0, fill='red')

    def highlight_tip(self, highlight:bool):
        fg = 'red' if highlight else 'black'
        self.tip.config(fg=fg)
            
    def disable_btn(self, disabled:bool):
        state = 'disabled' if disabled else 'normal'
        self.btn.config(state=state)
        

if __name__ == '__main__':
    app = App()
    app.mainloop()