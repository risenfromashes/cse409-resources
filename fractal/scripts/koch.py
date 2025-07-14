import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class Fractal:
    def draw(self, ax):
        raise NotImplementedError

class KochCurve(Fractal):
    def __init__(self, start, end, depth, color, linewidth=2):
        self.start = start
        self.end = end
        self.depth = depth
        self.color = color
        self.linewidth = linewidth
        self.segments = []

    def draw(self, ax):
        self.segments = []
        self._collect_segments(self.start, self.end, self.depth)
        for p1, p2 in self.segments:
            line = Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=self.color, linewidth=self.linewidth)
            ax.add_line(line)

    def _collect_segments(self, p1, p2, depth):
        if depth == 0:
            self.segments.append((p1, p2))
        else:
            dx = (p2[0] - p1[0]) / 3
            dy = (p2[1] - p1[1]) / 3

            pA = (p1[0] + dx, p1[1] + dy)
            pB = (p1[0] + 2*dx, p1[1] + 2*dy)

            angle = -60
            sin60 = 3**0.5 / 2
            cos60 = 0.5
            px = pA[0] + (cos60 * dx - sin60 * dy)
            py = pA[1] + (sin60 * dx + cos60 * dy)
            pPeak = (px, py)

            self._collect_segments(p1, pA, depth - 1)
            self._collect_segments(pA, pPeak, depth - 1)
            self._collect_segments(pPeak, pB, depth - 1)
            self._collect_segments(pB, p2, depth - 1)

    def get_bounds(self):
        xs, ys = [], []
        for p1, p2 in self.segments:
            xs.extend([p1[0], p2[0]])
            ys.extend([p1[1], p2[1]])
        return min(xs), max(xs), min(ys), max(ys)


def draw_koch(size, depth, color, output_path, show=False, linewidth=2):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    start = (0, 0)
    end = (size, 0)
    fractal = KochCurve(start, end, depth, color, linewidth)
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
    for i in range(0, 6):
        draw_koch(1.0, i, curve_color, f'../slide/images/koch/{i}.png', linewidth=3)
