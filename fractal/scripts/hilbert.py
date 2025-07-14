import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math

class Fractal:
    def draw(self, ax):
        raise NotImplementedError

class HilbertCurve(Fractal):
    def __init__(self, level, size, color, linewidth=2):
        self.level = level
        self.size = size
        self.color = color
        self.linewidth = linewidth
        self.points = []

    def draw(self, ax):
        self.points = []
        self._hilbert(0, 0, self.size, 0, 0, self.size, self.level)
        for i in range(len(self.points) - 1):
            p1 = self.points[i]
            p2 = self.points[i+1]
            line = Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=self.color, linewidth=self.linewidth)
            ax.add_line(line)

    def _hilbert(self, x0, y0, xi, xj, yi, yj, n):
        if n <= 0:
            x = x0 + (xi + yi) / 2
            y = y0 + (xj + yj) / 2
            self.points.append((x, y))
        else:
            self._hilbert(x0, y0, yi/2, yj/2, xi/2, xj/2, n-1)
            self._hilbert(x0 + xi/2, y0 + xj/2, xi/2, xj/2, yi/2, yj/2, n-1)
            self._hilbert(x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2, n-1)
            self._hilbert(x0 + xi/2 + yi, y0 + xj/2 + yj, -yi/2, -yj/2, -xi/2, -xj/2, n-1)

    def get_bounds(self):
        xs, ys = zip(*self.points)
        return min(xs), max(xs), min(ys), max(ys)


def draw_hilbert(size, depth, color, output_path, show=False, linewidth=2):
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    fractal = HilbertCurve(level=depth, size=size, color=color, linewidth=linewidth)
    fractal.draw(ax)

    xmin, xmax, ymin, ymax = fractal.get_bounds()
    padding = 0.05 * size
    ax.set_xlim(xmin - padding, xmax + padding)
    ax.set_ylim(ymin - padding, ymax + padding)

    plt.tight_layout(pad=0)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    plt.savefig(output_path, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0)
    if show:
        plt.show()

if __name__ == '__main__':
    curve_color = (0.5, 0.4, 0.63)
    for i in range(1, 7):
        draw_hilbert(1.0, i, curve_color, f'../slide/images/hilbert/{i}.png', linewidth=2)
