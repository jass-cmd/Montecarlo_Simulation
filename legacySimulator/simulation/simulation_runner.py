from simulation.throughput_function import simulate_project_delivery

def montecarlo_simulation (runs=1000, ticket_goal=150):

    """
    Runs multiple simulations of project delivery to estimate the
    distribution of completion times (in weeks).

    Parameters:
        runs (int): Number of simulations to perform
        ticket_goal (int): Total number of tickets to deliver in each run

    Returns:
        list: A list of weeks required in each simulation
    """

    estimated_weeks = []

    for k in range(runs):
        weeks = simulate_project_delivery ()
        estimated_weeks.append (weeks)

    return  estimated_weeks