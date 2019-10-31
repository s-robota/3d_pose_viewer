import os
import tkinter as tk

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from mpl_toolkits.mplot3d import Axes3D


class Pose3DViewer(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('3D Pose Viewer')

        self.pack()
        self.init_fig()
        self.create_widgets()
        self.ax.mouse_init()  # enable mouse controll

    def init_fig(self):
        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111, projection="3d")

    def load_pose3d(self, filepath):
        assert filepath[-4:] == '.npy'
        if not os.path.exists(filepath):
            raise ValueError('{:s} does not exist.'.format(filepath))
        self.poses3d = np.load(filepath)
        self.fidx_scale.configure(to=(self.poses3d.shape[0] - 1))  # set max frame index
        self.update_fig()

    def update_fig(self, event=None):
        # azim, elev = self.ax.azim, self.ax.elev
        self.ax.cla()  # clear contents in axes
        fidx = self.fidx_scale.get()
        pose3d = self.poses3d[fidx]
        draw_pose3d(self.ax, pose3d)
        self.canvas.draw()

    def create_widgets(self):
        self.canvas_frame = tk.Frame(self.master)
        self.canvas_frame.pack(side=tk.TOP)
        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack(side=tk.BOTTOM)

        self.canvas = FigureCanvasTkAgg(self.fig, self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.canvas_frame)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Scale to control frame index
        self.fidx = tk.IntVar()
        self.fidx_scale = tk.Scale(self.control_frame,
            variable=self.fidx,
            from_=0,
            to=100,  # NOTE just temporal
            resolution=1,
            orient=tk.HORIZONTAL,
            command=self.update_fig)
        self.fidx_scale.pack(anchor=tk.NW)
        self.fidx_scale.pack(fill='x')  # TODO This does not work !


def draw_pose3d(ax, pose3d, azim=None, elev=None, color='red'):
    ax.scatter(pose3d[:,0], pose3d[:,1], pose3d[:,2], c=color)
    ax.set_xlim(0,1)
    ax.set_ylim(0,1)
    ax.set_zlim(0,1)
    ax.grid('True')


if __name__ == '__main__':
    # just for test
    random_dots = np.random.rand(30, 20, 3)
    np.save('test.npy', random_dots)

    root = tk.Tk()
    app = Pose3DViewer(master=root)
    app.load_pose3d('test.npy')
    app.mainloop()