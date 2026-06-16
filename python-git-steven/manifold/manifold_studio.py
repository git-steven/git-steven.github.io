"""
ManifoldStudio
==============
Renders a Calabi-Yau manifold cross-section ("the Manifold") with a luminescent,
glowing dark-teal gradient, and orbits a camera around it.

Why Calabi-Yau: in string theory the *shape* of the compactified manifold
determines the laws of physics. That is "The Shape of Architecture" made literal.

World coordinate convention (as specified)
------------------------------------------
    -x = left,  +x = right
    +y = up,    -y = down
    +z = forward (toward viewer), -z = backward
The camera always points at the manifold's center (0, 0, 0) with +y up.

matplotlib note
---------------
matplotlib's 3D axes are not a real camera. We emulate it faithfully:
  * orbit ANGLE -> view_init(elev, azim, roll), computed so the target stays
    centered and +y stays up;
  * DISTANCE  -> the view-cube size (orthographic). Larger distance => the
    manifold looks smaller => it reads as farther away. "1.0 unit" == the
    manifold's own length along the relevant axis.
For a true cinematic camera, port the geometry to PyVista/Blender; the camera
math here transfers directly.

Conventions: one class, single return point per method, types in TYPES block.
Requires: numpy, matplotlib (Pillow for GIF output).
"""

from __future__ import annotations

import math
import random
from typing import List, Optional, Sequence, Tuple

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import animation

# --- type aliases (his convention: keep them named) ---------------------------
Axis = str                              # one of "x", "y", "z" (world frame)
Vec3 = Tuple[float, float, float]       # an (x, y, z) point in matplotlib frame
CamState = Tuple[float, float, float, float]   # (elev, azim, roll, half_extent)
Patch = Tuple[np.ndarray, np.ndarray, np.ndarray]  # (mx, my, mz) grids


class ManifoldStudio:
    """Generates the Manifold and produces stills + camera animations of it."""

    # world-axis -> the matplotlib axis that carries it.
    #   world x (right)        -> mpl x
    #   world y (up)           -> mpl z   (matplotlib is z-up)
    #   world z (forward/back) -> mpl y
    _WORLD_TO_MPL = {"x": "x", "y": "z", "z": "y"}

    def __init__(
        self,
        degree: int = 5,
        resolution: int = 40,
        proj_angle: float = 0.4 * math.pi,
        bg: str = "#0b0a24",
    ) -> None:
        self.degree = degree
        self.resolution = resolution
        self.proj_angle = proj_angle
        self.bg = bg
        # luminescent dark-teal -> bright turquoise; reads as self-lit on dark bg
        self.cmap = LinearSegmentedColormap.from_list(
            "manifold_glow",
            ["#03201f", "#063f3b", "#0a6f66", "#10a99c", "#26e6d2", "#8ffbee"],
        )
        self._patches: List[Patch] = []
        self._cmin = 0.0
        self._cmax = 1.0
        self._ext_mpl = {"x": 1.0, "y": 1.0, "z": 1.0}  # extents in mpl frame
        self._gext = 1.0
        self._build_patches()

    # ------------------------------------------------------------------ geometry
    def _build_patches(self) -> None:
        """Build the n^2 Calabi-Yau patches in matplotlib coordinates."""
        n = self.degree
        res = self.resolution
        a = np.linspace(0.0, math.pi / 2.0, res)
        b = np.linspace(-math.pi / 2.0, math.pi / 2.0, res)
        grid_a, grid_b = np.meshgrid(a, b)
        zexp = 2.0 / n
        patches: List[Patch] = []
        all_mx, all_my, all_mz = [], [], []
        for k1 in range(n):
            for k2 in range(n):
                z1 = np.exp(2j * math.pi * k1 / n) * (np.cos(grid_a + 1j * grid_b)) ** zexp
                z2 = np.exp(2j * math.pi * k2 / n) * (np.sin(grid_a + 1j * grid_b)) ** zexp
                world_x = z1.real
                world_z = z2.real
                world_y = math.cos(self.proj_angle) * z1.imag + math.sin(self.proj_angle) * z2.imag
                # permute world -> mpl (mpl is z-up, so world-up y maps to mpl z)
                mx, my, mz = world_x, world_z, world_y
                patches.append((mx, my, mz))
                all_mx.append(mx); all_my.append(my); all_mz.append(mz)
        cat_x = np.concatenate([p.ravel() for p in all_mx])
        cat_y = np.concatenate([p.ravel() for p in all_my])
        cat_z = np.concatenate([p.ravel() for p in all_mz])
        self._patches = patches
        self._cmin, self._cmax = float(cat_z.min()), float(cat_z.max())
        self._ext_mpl = {
            "x": float(cat_x.max() - cat_x.min()),
            "y": float(cat_y.max() - cat_y.min()),
            "z": float(cat_z.max() - cat_z.min()),
        }
        self._gext = max(self._ext_mpl.values())

    def _extent(self, world_axis: Axis) -> float:
        """Length of the manifold along a WORLD axis (the distance unit)."""
        result = self._ext_mpl[self._WORLD_TO_MPL[world_axis]]
        return result

    # -------------------------------------------------------------------- camera
    def _orbit_unit(self, rev_axis: Axis, angle_deg: float) -> Vec3:
        """Unit camera direction (mpl frame) orbiting one WORLD axis, eye->origin."""
        a = math.radians(angle_deg)
        if rev_axis == "y":          # orbit world-up: turntable in mpl x-y plane
            vec = (math.cos(a), math.sin(a), 0.0)
        elif rev_axis == "x":        # orbit world-x: in mpl y-z plane
            vec = (0.0, math.sin(a), math.cos(a))
        else:                        # rev_axis == "z": orbit world-z: in mpl x-z plane
            vec = (math.sin(a), 0.0, math.cos(a))
        return vec

    def _rotate_about(self, vec: Vec3, world_axis: Axis, angle_deg: float) -> Vec3:
        """Rotate a vector about a WORLD axis (mapped into the mpl frame)."""
        a = math.radians(angle_deg)
        c, s = math.cos(a), math.sin(a)
        x, y, z = vec
        mpl_axis = self._WORLD_TO_MPL[world_axis]
        if mpl_axis == "x":
            out = (x, c * y - s * z, s * y + c * z)
        elif mpl_axis == "y":
            out = (c * x + s * z, y, -s * x + c * z)
        else:                         # mpl z
            out = (c * x - s * y, s * x + c * y, z)
        return out

    def _cam_to_view(self, cam: Vec3) -> Tuple[float, float, float]:
        """Convert an mpl-frame camera position to (elev, azim, roll) degrees."""
        x, y, z = cam
        r = math.sqrt(x * x + y * y + z * z) or 1.0
        elev = math.degrees(math.asin(max(-1.0, min(1.0, z / r))))
        azim = math.degrees(math.atan2(y, x))
        return elev, azim, 0.0

    def _half_for(self, distance: float) -> float:
        """View-cube half-size for a given distance (units of manifold length)."""
        # at distance 2.0 the manifold fills ~60% of frame; larger => farther/smaller
        result = self._gext * 0.5 * (distance / 2.0) / 0.6
        return result

    def _state(self, rev_axis: Axis, angle_deg: float, distance: float) -> CamState:
        """One camera state (elev, azim, roll, half) for a single-axis orbit."""
        unit = self._orbit_unit(rev_axis, angle_deg)
        elev, azim, roll = self._cam_to_view(unit)
        half = self._half_for(distance)
        return elev, azim, roll, half

    # -------------------------------------------------------------------- drawing
    def _new_fig(self, transparent: bool = False):
        face = "none" if transparent else self.bg
        fig = plt.figure(figsize=(7, 7), facecolor=face)
        ax = fig.add_subplot(111, projection="3d")
        ax.set_facecolor(face)
        ax.set_proj_type("ortho")
        ax.set_axis_off()
        ax.set_box_aspect((1, 1, 1))
        return fig, ax

    def _draw_surface(self, ax) -> None:
        """Draw all patches once, self-lit (shade=False) so the gradient glows."""
        span = (self._cmax - self._cmin) or 1.0
        for mx, my, mz in self._patches:
            norm = (mz - self._cmin) / span
            ax.plot_surface(
                mx, my, mz,
                facecolors=self.cmap(norm),
                rstride=1, cstride=1, linewidth=0,
                antialiased=False, shade=False,
            )

    def _apply_state(self, ax, state: CamState) -> None:
        elev, azim, roll, half = state
        ax.view_init(elev=elev, azim=azim, roll=roll)
        ax.set_xlim(-half, half)
        ax.set_ylim(-half, half)
        ax.set_zlim(-half, half)

    # --------------------------------------------------------------- public: still
    def render_image(self, axis: Axis, angle: float, distance: float, out_path: str,
                     transparent: bool = False) -> str:
        """Single still: view the manifold from `axis` at `angle`, at `distance`
        (distance unit == manifold length along `axis`). Set transparent=True to
        export a cut-out PNG that drops cleanly into a Gemini/Photoshop scene."""
        fig, ax = self._new_fig(transparent=transparent)
        self._draw_surface(ax)
        self._apply_state(ax, self._state(axis, angle, distance))
        save_face = "none" if transparent else self.bg
        fig.savefig(out_path, dpi=130, facecolor=save_face, transparent=transparent,
                    bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        return out_path

    def set_gradient(self, stops: Sequence[str]) -> None:
        """Set the manifold colormap from hex stops, e.g.
        ["#365558", "#FFFFFF", "#515931"] (dark turquoise -> white -> dark green).
        Coloring is by height, so a 3-stop divergent map reveals the form."""
        self.cmap = LinearSegmentedColormap.from_list("manifold_custom", list(stops))
        return None

    def render_six_views(self, out_path: str, distance: float = 2.0,
                         frame_color: str = "#365558", label_color: str = "#E8F6F4",
                         dpi: int = 130) -> str:
        """Orthographic contact sheet: N, E, S, W around the equator plus TOP and
        BOTTOM, each framed and labeled. Camera looks at (0,0,0); +y is up."""
        import matplotlib.patches as mpatches
        views = [("N", 0.0, 90.0), ("E", 0.0, 0.0), ("S", 0.0, 270.0),
                 ("W", 0.0, 180.0), ("TOP", 90.0, 0.0), ("BOTTOM", -90.0, 0.0)]
        half = self._half_for(distance)
        fig = plt.figure(figsize=(12, 8), facecolor=self.bg)
        for i, (name, elev, azim) in enumerate(views):
            ax = fig.add_subplot(2, 3, i + 1, projection="3d")
            ax.set_facecolor(self.bg)
            ax.set_proj_type("ortho")
            ax.set_axis_off()
            ax.set_box_aspect((1, 1, 1))
            self._draw_surface(ax)
            ax.view_init(elev=elev, azim=azim, roll=0)
            ax.set_xlim(-half, half)
            ax.set_ylim(-half, half)
            ax.set_zlim(-half, half)
            ax.text2D(0.05, 0.90, name, transform=ax.transAxes,
                      color=label_color, fontsize=14, fontweight="bold")
        fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01,
                            wspace=0.03, hspace=0.03)
        for ax in fig.axes:
            p = ax.get_position()
            fig.add_artist(mpatches.Rectangle(
                (p.x0, p.y0), p.width, p.height, transform=fig.transFigure,
                fill=False, edgecolor=frame_color, linewidth=1.6))
        fig.savefig(out_path, dpi=dpi, facecolor=self.bg)
        plt.close(fig)
        return out_path

    # ----------------------------------------------------------- state generators
    def _revolve_states(
        self, rev_axis: Axis, d: float, rps: float, fps: int,
        detente_pause: float, detente_every: float,
        rev_axis2: Optional[Axis], rps2: float, d2: float,
    ) -> List[CamState]:
        """Build camera states for a symmetric revolve around one or two axes."""
        dt = 1.0 / fps
        states: List[CamState] = []
        t = 0.0
        last_bucket = -1
        two = rev_axis2 is not None
        while True:
            ang1 = 360.0 * rps * t
            ang2 = 360.0 * rps2 * t if two else 0.0
            if ang1 >= 360.0 and (not two or ang2 >= 360.0):
                break
            # base orbit on axis 1
            r1 = d * self._extent(rev_axis)
            ux, uy, uz = self._orbit_unit(rev_axis, ang1)
            cam = (ux * r1, uy * r1, uz * r1)
            dist_eff = d
            if two:
                cam = self._rotate_about(cam, rev_axis2, ang2)
                phase = (1.0 - math.cos(math.radians(ang2))) / 2.0
                dist_eff = d + (d2 - d) * phase
            elev, azim, roll = self._cam_to_view(cam)
            states.append((elev, azim, roll, self._half_for(dist_eff)))
            # detente: hold briefly each `detente_every` degrees on axis 1
            if detente_pause > 0.0 and detente_every > 0.0:
                bucket = int(ang1 // detente_every)
                if bucket != last_bucket:
                    last_bucket = bucket
                    hold = states[-1]
                    states.extend([hold] * max(1, round(detente_pause * fps)))
            t += dt
        return states

    def gen_revolve_sym(
        self, rev_axis: Axis, out_path: str, d: float = 2.0, rps: float = 0.5,
        detente_pause: float = 0.5, detente_every: float = 15.0,
        rev_axis2: Optional[Axis] = None, rps2: float = 0.5, d2: float = 2.0,
        fps: int = 15,
    ) -> str:
        """Symmetric camera revolve. Orbits `rev_axis` at `rps` rotations/sec and
        distance `d`; optionally also orbits `rev_axis2` at `rps2`/`d2`. Adds a
        `detente_pause`-second hold every `detente_every` degrees. Stops once BOTH
        axes have completed at least one full revolution."""
        states = self._revolve_states(
            rev_axis, d, rps, fps, detente_pause, detente_every, rev_axis2, rps2, d2
        )
        result = self._animate(states, out_path, fps)
        return result

    def _rand_states(
        self, d1: float, d2: float, max_duration: float, fps: int, seed: Optional[int],
    ) -> List[CamState]:
        """Random-walk camera: 1-2 random axes, distance oscillating between
        d1 and d2; re-roll parameters per segment until max_duration is hit."""
        rng = random.Random(seed)
        dt = 1.0 / fps
        n_frames = int(round(max_duration * fps))
        states: List[CamState] = []
        t = 0.0
        seg_end = 0.0
        ax1 = ax2 = "y"
        rps1 = rps2 = 0.2
        osc_period = 4.0
        phase0 = 0.0
        use_two = False
        for i in range(n_frames):
            if t >= seg_end:                         # re-roll a new segment
                axes = ["x", "y", "z"]
                use_two = rng.random() < 0.5
                ax1 = rng.choice(axes)
                ax2 = rng.choice([a for a in axes if a != ax1])
                rps1 = rng.uniform(0.08, 0.35) * rng.choice([-1.0, 1.0])
                rps2 = rng.uniform(0.08, 0.35) * rng.choice([-1.0, 1.0])
                osc_period = rng.uniform(2.5, 6.0)
                phase0 = rng.uniform(0.0, 2.0 * math.pi)
                seg_end = t + rng.uniform(2.0, 4.0)
            ang1 = 360.0 * rps1 * t
            r1 = d1 * self._extent(ax1)
            ux, uy, uz = self._orbit_unit(ax1, ang1)
            cam = (ux * r1, uy * r1, uz * r1)
            if use_two:
                cam = self._rotate_about(cam, ax2, 360.0 * rps2 * t)
            # smooth distance oscillation between d1 and d2
            osc = (1.0 - math.cos(2.0 * math.pi * t / osc_period + phase0)) / 2.0
            dist_eff = d1 + (d2 - d1) * osc
            elev, azim, roll = self._cam_to_view(cam)
            states.append((elev, azim, roll, self._half_for(dist_eff)))
            t += dt
        return states

    def gen_rand_sim(
        self, out_path: str, d1: float = 1.5, d2: float = 3.0,
        max_duration: float = 6.0, fps: int = 15, seed: Optional[int] = None,
    ) -> str:
        """Random camera 'sim': drifts around 1-2 random axes while the distance
        oscillates between d1 and d2, re-rolling until `max_duration` seconds."""
        states = self._rand_states(d1, d2, max_duration, fps, seed)
        result = self._animate(states, out_path, fps)
        return result

    # ----------------------------------------------------------------- animation
    def _animate(self, states: Sequence[CamState], out_path: str, fps: int) -> str:
        """Draw the surface once, then sweep the camera through `states`."""
        fig, ax = self._new_fig()
        self._draw_surface(ax)
        self._apply_state(ax, states[0])

        def update(frame: int):
            self._apply_state(ax, states[frame])
            return ()

        anim = animation.FuncAnimation(
            fig, update, frames=len(states), interval=1000.0 / fps, blit=False
        )
        anim.save(out_path, writer=animation.PillowWriter(fps=fps))
        plt.close(fig)
        return out_path


if __name__ == "__main__":
    # Preview settings kept light so it renders quickly; raise `resolution`
    # and `fps` for final art.
    studio = ManifoldStudio(degree=5, resolution=18)

    studio.render_image(axis="y", angle=35.0, distance=2.0, out_path="cy_still.png")

    # 1) revolve around the up-axis (turntable), with detentes
    studio.gen_revolve_sym("y", "cy_revolve_y.gif", rps=0.6, fps=12)
    # 2) revolve around x (tumble over the top)
    studio.gen_revolve_sym("x", "cy_revolve_x.gif", rps=0.6, detente_pause=0.0, fps=12)
    # 3) dual-axis revolve (y then layered with z), stops when both finish a rev
    studio.gen_revolve_sym(
        "y", "cy_revolve_yz.gif", rps=0.6, rev_axis2="z", rps2=0.3,
        d=2.0, d2=3.0, detente_pause=0.0, fps=12,
    )
    # 4) random sim
    studio.gen_rand_sim("cy_rand_sim.gif", d1=1.6, d2=3.2, max_duration=5.0, fps=12, seed=7)

    print("ok: cy_still.png + 4 animations written")
