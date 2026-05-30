"""Figure-8 immersion of the Klein bottle — 'the Manifold'."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import animation

# --- palette (matches the article image set) ---
BG = "#161038"          # deep indigo twilight
TEAL_CMAP = LinearSegmentedColormap.from_list(
    "manifold_teal",
    ["#0b3b3b", "#0f5c5c", "#13a7a7", "#2fe0d0", "#7af7e6"],  # dark teal -> bright turquoise
)

# --- figure-8 Klein bottle immersion ---
R = 3.0
u = np.linspace(0, 2 * np.pi, 220)
v = np.linspace(0, 2 * np.pi, 110)
u, v = np.meshgrid(u, v)
t = R + np.cos(u / 2) * np.sin(v) - np.sin(u / 2) * np.sin(2 * v)
x = t * np.cos(u)
y = t * np.sin(u)
z = np.sin(u / 2) * np.sin(v) + np.cos(u / 2) * np.sin(2 * v)

# color by height for the glow gradient
norm = (z - z.min()) / (z.max() - z.min())

def make_axes():
    fig = plt.figure(figsize=(7, 7), facecolor=BG)
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor(BG)
    ax.set_box_aspect((1, 1, 0.7))
    ax.set_axis_off()
    ax.plot_surface(
        x, y, z, facecolors=TEAL_CMAP(norm),
        rstride=1, cstride=1, linewidth=0, antialiased=True, shade=True,
    )
    return fig, ax

# --- three still angles ---
for i, (elev, azim) in enumerate([(22, 35), (8, 120), (55, 210)]):
    fig, ax = make_axes()
    ax.view_init(elev=elev, azim=azim)
    fig.savefig(f"manifold_angle_{i}.png", dpi=130, facecolor=BG, bbox_inches="tight")
    plt.close(fig)

# --- rotating animation (gif) ---
fig, ax = make_axes()
def spin(frame):
    ax.view_init(elev=18, azim=frame * 4)
    return ()
anim = animation.FuncAnimation(fig, spin, frames=90, interval=60, blit=False)
anim.save("manifold_spin.gif", writer=animation.PillowWriter(fps=18))
plt.close(fig)
print("ok: wrote 3 stills + manifold_spin.gif")
