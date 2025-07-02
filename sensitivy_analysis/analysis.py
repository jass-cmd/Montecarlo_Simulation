import numpy as np

def analyze_results (results):

    """
    Analyze a list of simulation results and return useful statistics.
    Parameters:
        simulation_results (list): List of weeks required in each simulation
    Returns:
        dict: Dictionary with summary statistics
    """
    stats = {

        "mean": round (np.mean(results)),
        "mediam": round (np.median(results)),
        "pencentile_50":int (np.percentile(results,50)),
        "percentile_80":int (np.percentile(results,80)),
        "percentile_90":int (np.percentile(results,90)),
        "min":min(results),
        "max":max (results)
    }

    return stats     
