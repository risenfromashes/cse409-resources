import os
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import math

class Fractal:
    def draw(self, ax):
        raise NotImplementedError

class FractalTree(Fractal):
    def __init__(self, start_pos, angle, length, depth, angle_change, length_scale, color, linewidth=2):
        self.start_pos = start_pos
        self.angle = angle
        self.length = length
        self.depth = depth
        self.angle_change = angle_change
        self.length_scale = length_scale
        self.color = color
        self.linewidth = linewidth
        self.segments = []

    def draw(self, ax):
        self.segments = []
        self._draw_branch(self.start_pos[0], self.start_pos[1], self.angle, self.length, self.depth)
        for p1, p2 in self.segments:
            line = Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=self.color, linewidth=self.linewidth*(self.depth/10))
            ax.add_line(line)

    def _draw_branch(self, x, y, angle, length, depth):
        if depth == 0 or length < 0.001:
            return
        x2 = x + length * math.cos(math.radians(angle))
        y2 = y + length * math.sin(math.radians(angle))
        self.segments.append(((x, y), (x2, y2)))
        self._draw_branch(x2, y2, angle - self.angle_change, length * self.length_scale, depth - 1)
        self._draw_branch(x2, y2, angle + self.angle_change, length * self.length_scale, depth - 1)

    def get_bounds(self):
        xs, ys = [], []
        for p1, p2 in self.segments:
            xs.extend([p1[0], p2[0]])
            ys.extend([p1[1], p2[1]])
        return min(xs), max(xs), min(ys), max(ys)

def draw_tree(depth, color, output_path, show=False, linewidth=2):
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    fractal = FractalTree(
        start_pos=(0, 0),
        angle=90,
        length=1.0,
        depth=depth,
        angle_change=25,  # adjust for branching angle
        length_scale=0.7,  # adjust for branch length reduction
        color=color,
        linewidth=linewidth
    )
    fractal.draw(ax)

    xmin, xmax, ymin, ymax = fractal.get_bounds()
    padding = 0.05
    ax.set_xlim(xmin - padding, xmax + padding)
    ax.set_ylim(ymin - padding, ymax + padding)

    plt.tight_layout(pad=0)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    plt.savefig(output_path, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0)
    if show:
        plt.show()

if __name__ == '__main__':
    tree_color = (0.4, 0.3, 0.6)
    for i in range(1, 8):
        draw_tree(i, tree_color, f'../slide/images/tree/{i}.png', linewidth=6)
