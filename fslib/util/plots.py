__author__ = 'griver'
from matplotlib import pyplot as plt
import matplotlib.colors as cls

colors = list(cls.cnames)

class PlotBuilder(object):
    figure = None
    sp = []

    def create_figure(self, gridx = 1, gridy = 1):
        self.figure = plt.figure()
        self.sp = []
        id = 1
        for i in range(0, gridx * gridy):
            ax = self.figure.add_subplot(gridx, gridy, i + 1)
            self.sp.append(ax)

    def plot_funcs(self, plt_id, x_axis, func, *funcs):
        cid = 0
        lines = []
        tmp = self.sp[plt_id].plot(x_axis, func[0], func[1], color=colors[cid], label=func[2])    # func[1], label=func[2])
        lines.append(tmp[0])
        for f in funcs:
            cid += 1
            tmp = self.sp[plt_id].plot(x_axis, f[0], f[1], color=colors[cid], label=f[2])  # f[1], label=f[2])
            lines.append(tmp[0])

        # Now add the legend with some customizations.

        legend = self.sp[plt_id].legend(loc='lower left', shadow=True)

        # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
        frame = legend.get_frame()
        frame.set_facecolor('0.90')

        # Set the fontsize
        for label in legend.get_texts():
            label.set_fontsize('large')

        for label in legend.get_lines():
            label.set_linewidth(1)  # the legend line width

    def show(self):
        plt.show()