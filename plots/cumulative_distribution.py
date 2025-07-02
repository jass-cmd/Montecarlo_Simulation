import matplotlib.pyplot as plt
import numpy as np

def plot_cumulative_distribution (results):
    """
    Plots the cumulative distribution function (CDF) of the simulation results.
    Parameters:
        results (list): List of simulated delivery durations (in weeks)
    """ 
    sorted_data = np.sort (results) #order data from min to max
    cumulative = np.arange (1, len(sorted_data) + 1)/ len(sorted_data) # % acumulated [this is normalizing the date in terms of 0,1]

    plt.figure(figsize=(10,5))
    plt.plot (sorted_data, cumulative, drawstyle ='steps-post', color='blue', label='CDF') #plt.plot(x, y)


    #reference lines
    plt.axhline(0.8, color ='green', linestyle='dotted', label='80%')
    plt.axhline(0.9, color='orange', linestyle='dotted', label='90%')

    #details of the lines and plot
    plt.title("Cumulative  Distribution - Delivery Time (weeks)")
    plt.xlabel("weeks")
    plt.ylabel("Cumulative Probability")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()  