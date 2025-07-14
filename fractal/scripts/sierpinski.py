import os
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

class Fractal:
    def draw(self, ax):
        raise NotImplementedError

class Sierpinski(Fractal):
    def __init__(self, vertices, depth, fill_color, border_color):
        self.vertices = vertices
        self.depth = depth
        self.fill_color = fill_color
        self.border_color = border_color

    def draw(self, ax):
        self._draw_triangle(ax, self.vertices, self.depth)

    def _draw_triangle(self, ax, verts, depth):
        if depth == 0:
            tri = Polygon(verts, closed=True, facecolor=self.fill_color, edgecolor=self.border_color, 
                          linewidth=3)
            ax.add_patch(tri)
        else:
            v0, v1, v2 = verts
            m01 = ((v0[0]+v1[0])/2, (v0[1]+v1[1])/2)
            m12 = ((v1[0]+v2[0])/2, (v1[1]+v2[1])/2)
            m20 = ((v2[0]+v0[0])/2, (v2[1]+v0[1])/2)
            self._draw_triangle(ax, [v0, m01, m20], depth-1)
            self._draw_triangle(ax, [v1, m12, m01], depth-1)
            self._draw_triangle(ax, [v2, m20, m12], depth-1)


def draw_sierpinski(size, depth, fill_color, border_color, output_path,show=False):
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    verts = [(0, 0), (size, 0), (size/2, size * (3**0.5)/2)]
    fractal = Sierpinski(verts, depth, fill_color, border_color)
    fractal.draw(ax)

    plt.tight_layout(pad=0)
    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    plt.savefig(output_path, dpi=300, transparent=True)
    if show:
        plt.show()

if __name__ == '__main__':
    fill = (0.85, 0.82, 0.89)
    border = (0.5, 0.4, 0.63)
    for i in range(0, 7):
        draw_sierpinski(1.0, i, fill, border, f'../slide/images/sierpinski/{i}.png')
