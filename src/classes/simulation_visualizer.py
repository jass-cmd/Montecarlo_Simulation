import os
os.environ.setdefault("MPLBACKEND", "Agg")  # backend without GUI

import io
import base64
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


class SimulationVisualizer:
    """
    Generates all the visualizations from simulation results
    and returns them as base64-encoded images ready to be sent to the frontend by an API.
    """

    def __init__(self, results: np.ndarray):
        """
        Creates an object that has the array results as the main attribute
        not before validating its structure and data type.
        """
        if not isinstance(results, np.ndarray):
            raise ValueError("Results must be a NumPy array.")
        if results.ndim != 1:
            raise ValueError("Results must be a 1-dimensional array.")
        if results.size < 2:
            raise ValueError("Results array must contain at least two values.")
        if not np.isfinite(results).all():
            raise ValueError("Results contain NaN or infinite values.")

        self.results = results

    # ========= internal helpers =========

    @staticmethod
    def _render_plot_to_base64(fig: Figure) -> str:
        """
        Renders a Matplotlib Figure to PNG (in-memory) and returns a base64 string.
        """
        buf = io.BytesIO()
        FigureCanvas(fig).print_png(buf)  # render with Agg
        img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()
        fig.clf()
        return img_base64

    # ========= public plots =========

    def _plot_histogram(self, bins: int = 30, show: bool = False) -> str:
        """
        Creates a histogram with useful percentiles and returns it as base64.
       
        """
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(1, 1, 1)

        ax.hist(self.results, bins=bins, edgecolor='black', alpha=0.75)
        ax.set_title("Completion Time")
        ax.set_xlabel("Weeks to Completion")
        ax.set_ylabel("Frequency")
        ax.grid(True, alpha=0.25)

        for p, color in zip([50, 85, 95], ['blue', 'green', 'red']):
            val = np.percentile(self.results, p)
            ax.axvline(val, color=color, linestyle='--', label=f'P{p}: {val:.1f} weeks')

        ax.legend()
        return self._render_plot_to_base64(fig)

    def plot_cdf(self) -> str:
        """
        Creates the CDF plot and returns it as base64.
        """
        sorted_vals = np.sort(self.results)
        probs = np.linspace(0, 1, len(sorted_vals), endpoint=True)

        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(1, 1, 1)

        ax.step(sorted_vals, probs, where='post')
        ax.set_title("Cumulative Distribution Function (CDF)")
        ax.set_xlabel("Weeks to Completion")
        ax.set_ylabel("Cumulative Probability")
        ax.set_ylim(0, 1)
        ax.grid(True, alpha=0.25)

        for p, color in zip([50, 85, 95], ['blue', 'green', 'red']):
            val = np.percentile(self.results, p)
            ax.axvline(val, color=color, linestyle='--', label=f'P{p}: {val:.1f} weeks')

        ax.legend()
        return self._render_plot_to_base64(fig)

    def plot_convergence(self, step: int = 200) -> str:
        """
        Convergence of the P85 estimate vs number of simulations. Returns base64.
        """
        if step < 1:
            raise ValueError("Step must be a positive integer.")

        num_points = len(self.results) // step
        if num_points < 2:
            raise ValueError("Not enough data points to analyze convergence.")

        x_vals = []
        y_vals = []
        for i in range(1, num_points + 1):
            current_subset = self.results[:i * step]
            percentile_85 = np.percentile(current_subset, 85)
            x_vals.append(i * step)
            y_vals.append(percentile_85)

        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(1, 1, 1)

        ax.plot(x_vals, y_vals, marker='o')
        ax.set_title("Convergence of P85 Estimate")
        ax.set_xlabel("Number of Simulations")
        ax.set_ylabel("P85 Completion Time (weeks)")
        ax.grid(True, alpha=0.25)

        return self._render_plot_to_base64(fig)
