import matplotlib.pyplot as plt
import numpy as np

def plot_histogram (results):

    """
    Plot a histogram of simulation results (weeks to delivery). 
    Parameters:
    results (list): List of simulated delivery durations (in weeks)
    """

    bins = range(min(results), max(results) + 1)
    plt.figure(figsize=(10, 5))
    plt.hist(results, bins=bins, edgecolor='black', align='left')
   
   #basic stats 
    mean= np.mean(results)
    p80 = np.percentile(results,80)
    p90 = np.percentile(results,90)

   #vertical lines
    plt.axvline (mean, color='red', linestyle='dashed', linewidth=2,  label= f'mean:{round(mean)}')
    plt.axvline (p80, color='yellow',linestyle='dashed', linewidth=2, label= f'p80:{round(p80)}')
    plt.axvline (p90, color='green', linestyle='dashed', linewidth=2, label= f'p90:{round(p90)}')
    
    #Labels and layout
    plt.title("Monte Carlo Simulation – Delivery Time (Weeks)")
    plt.xlabel("Weeks")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.legend()
    plt.show()
