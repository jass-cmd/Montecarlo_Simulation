import matplotlib.pyplot as plt
import numpy as np

def plot_convergence_curve(simulation_results):
    """
    Plots how the mean delivery time converges as more simulations are added.
    Parameters:
        simulation_results (list): List of simulated delivery durations
    """

    cumulative_means = [np.mean(simulation_results[:i+1]) for i in range(len(simulation_results))]

    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(simulation_results) + 1), cumulative_means, label='Cumulative Mean')
    plt.xlabel("Number of Simulations")
    plt.ylabel("Mean Delivery Time (Weeks)")
    plt.title("Convergence of Monte Carlo Simulation")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
