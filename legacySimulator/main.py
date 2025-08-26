from simulation.throughput_function import simulate_project_delivery
from simulation.simulation_runner import montecarlo_simulation
from sensitivy_analysis.analysis import analyze_results
from plots.results_distribution import plot_histogram
from plots.cumulative_distribution import plot_cumulative_distribution
from plots.convergence_curve import plot_convergence_curve

"""
This file imports the functions I created and uses them to run and visualize the simulation results.
"""

def run_simulation():

    #runs Monte Carlo simulation 1000 times
    simulation = montecarlo_simulation(runs=1000, ticket_goal=150)

    # visualize results
    # plot_histogram(simulation)
    # plot_cumulative_distribution(simulation)

    print(f"Number ofSimulations runned (n={len(simulation)}):")

    #basic statistics
    stats = analyze_results(simulation)
    plot_convergence_curve(simulation)
    return stats

#this ensures the simulation runs only if the file it's executed
if __name__ == "__main__":
    stats = run_simulation()
    print("Basic statistics:")
    print(stats)
    
    
   
