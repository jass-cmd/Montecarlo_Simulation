# test_hist.py
import numpy as np
import matplotlib.pyplot as ptl
from simulation_params import SimulationParameters
from risk_class import Risk
from simulator import Simulator
from simulation_visualizer import SimulationVisualizer

parameters_obj = SimulationParameters(150, 3, 5, 9, 5000)
risk_obj = [Risk("Dependencies", 0.3, 0.7)]
results_distribution = Simulator(parameters_obj, risk_obj)
results_distribution.run_simulation()
viz = SimulationVisualizer(results_distribution.results)
viz.plot_cdf()
#viz._plot_histogram(30)
#viz.plot_convergence(100)
# viz.plot_boxplot()


