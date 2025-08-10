import numpy as np
import matplotlib.pyplot as plt
import io
import base64


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
       
        self.results = results

    def _render_plot_to_base64(self) -> str:
        """
        This method converts the plots into base 64 strings that can be sent to the frontend
        by fast API. This is to not depend on the file management system.
        """
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", bbox_inches="tight")
        plt.close()
        buffer.seek(0)
        img_bytes = buffer.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")
        return img_base64

    def _plot_histogram(self, bins: int = 30, show: bool = True) -> str:
        """
        This method creates a histogram with percentiles that
        will be converted into base64 string
        """
        plt.figure(figsize=(10, 6))
        plt.hist(self.results, bins=bins, edgecolor='black', alpha=0.75)
        plt.title("Completion Time")
        plt.xlabel("Weeks to Completion")
        plt.ylabel("Frequency")

        for p, color in zip([50, 85, 95], ['blue', 'green', 'red']):
            val = np.percentile(self.results, p)
            plt.axvline(val, color=color, linestyle='--', label=f'P{p}: {val:.1f} weeks')

        plt.legend()

        if show:
            plt.show()
            return ""
        else:
            return self._render_plot_to_base64()

    def plot_cdf(self) -> str:
        """
        This creates the CDF plot.
        """
        sorted_vals = np.sort(self.results)
        probs = np.linspace(0, 1, len(sorted_vals), endpoint=True)

        plt.figure(figsize=(10, 6))
        plt.plot(sorted_vals, probs, drawstyle='steps-post')
        plt.title("Cumulative Distribution Function (CDF)")
        plt.xlabel("Weeks to Completion")
        plt.ylabel("Cumulative Probability")

        for p, color in zip([50, 85, 95], ['blue', 'green', 'red']):
            val = np.percentile(self.results, p)
            plt.axvline(val, color=color, linestyle='--', label=f'P{p}: {val:.1f} weeks')

        plt.legend()
        plt.show()#for local use only
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
        plt.show() #for local use only
        return self._render_plot_to_base64()