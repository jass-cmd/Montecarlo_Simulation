import numpy as np
import matplotlib.pyplot as plt
import io
import base64


class SimulationVisualizer:
    """
    Generates all the visualizations from simulation results
    and returns them as base64-encoded images ready to be sent to the frontend by an API.
    """

    def __init__(self, results:np.ndarray):

        """
        Creates an object that has the array results as the main attribute
        not before validaing its structure and data type.
        """
        if not isinstance(results, np.ndarray):
            raise ValueError("Results must be a NumPy array.")
        if results.ndim != 1:
            raise ValueError("Results must be a 1-dimensional array.")
        if results.size < 2:
            raise ValueError("Results array must contain at least two values.")
        self.results = results


    def _render_plot_to_base64(self):

         buffer = io.BytesIO() #creates a temporal file in memory
         


    def plot_histogram(self, bins: int = 30) -> str:
        plt.figure(figsize=(10, 6))
        plt.hist(self.results, bins=bins, edgecolor='black', alpha=0.75)
        plt.title("Histogram of Completion Time")
        plt.xlabel("Weeks to Completion")
        plt.ylabel("Frequency")

        for p, color in zip([50, 85, 95], ['blue', 'green', 'red']):
            val = np.percentile(self.results, p)
            plt.axvline(val, color=color, linestyle='--', label=f'P{p}: {val:.1f} weeks')
        plt.legend()

        return self._render_plot_to_base64()

    def plot_cdf(self) -> str:
        sorted_vals = np.sort(self.results)
        probs = np.linspace(0, 1, len(sorted_vals), endpoint=False)

        plt.figure(figsize=(10, 6))
        plt.plot(sorted_vals, probs, drawstyle='steps-post')
        plt.title("Cumulative Distribution Function (CDF)")
        plt.xlabel("Weeks to Completion")
        plt.ylabel("Cumulative Probability")

        for p, color in zip([50, 85, 95], ['blue', 'green', 'red']):
            val = np.percentile(self.results, p)
            plt.axvline(val, color=color, linestyle='--', label=f'P{p}: {val:.1f} weeks')
        plt.legend()

        return self._render_plot_to_base64()

    def plot_boxplot(self) -> str:
        plt.figure(figsize=(8, 6))
        plt.boxplot(self.results, vert=False)
        plt.title("Boxplot of Completion Time")
        plt.xlabel("Weeks to Completion")

        return self._render_plot_to_base64()

    def plot_convergence(self, step: int = 500) -> str:
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

        plt.figure(figsize=(10, 6))
        plt.plot(x_vals, y_vals, marker='o')
        plt.title("Convergence of P85 Estimate")
        plt.xlabel("Number of Simulations")
        plt.ylabel("P85 Completion Time (weeks)")

        return self._render_plot_to_base64()
