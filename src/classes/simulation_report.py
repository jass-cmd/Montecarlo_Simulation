import numpy as np
import base64
import io
from fpdf import FPDF
from simulation_analyzer import SimulationAnalyzer
from simulation_visualizer import SimulationVisualizer


class SimulationReport:
    """
    Generates a consolidated PDF report from Monte Carlo simulation results,
    including statistical summaries and graphical visualizations.
    """

    def __init__(self, results: np.ndarray):
        if not isinstance(results, np.ndarray):
            raise ValueError("Results must be a NumPy array.")
        self.results = results
        self.analyzer = SimulationAnalyzer(results)
        self.visualizer = SimulationVisualizer(results)

    def _save_base64_image_to_tempfile(self, img_base64: str, filename: str) -> str:
        """
        Decodes a base64 image string and saves it temporarily to disk
        so it can be inserted into the PDF. Returns the file path.
        """
        img_bytes = base64.b64decode(img_base64)
        path = f"{filename}.png"
        with open(path, "wb") as f:
            f.write(img_bytes)
        return path

    def generate_pdf(self, output_path: str = "simulation_report.pdf") -> None:
        """
        Generates a PDF file with summary statistics and visualizations
        from the simulation results.
        """
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Monte Carlo Simulation Report", ln=True)

        # Statistics
        pdf.set_font("Arial", size=12)
        pdf.ln(5)
        pdf.cell(0, 10, "Summary Statistics:", ln=True)

        stats = self.analyzer.overall_stats().to_dict()
        percentiles = self.analyzer.summary(percentiles=(0.05, 0.95)).to_dict(orient="records")[0]
        stats.update(percentiles)

        for key, val in stats.items():
            pdf.cell(0, 10, f"{key}: {val:.2f}", ln=True)

        # Graphs
        plot_funcs = {
            "Histogram": lambda: self.visualizer._plot_histogram(show=False),
            "CDF": self.visualizer.plot_cdf,
            "Boxplot": self.visualizer.plot_boxplot,
            "Convergence": self.visualizer.plot_convergence
        }

        for title, plot_func in plot_funcs.items():
            image_base64 = plot_func()
            image_path = self._save_base64_image_to_tempfile(image_base64, f"temp_{title}")
            pdf.add_page()
            pdf.set_font("Arial", "B", 14)
            pdf.cell(0, 10, title, ln=True)
            pdf.image(image_path, x=15, w=180)

        # Save PDF
        pdf.output(output_path)
