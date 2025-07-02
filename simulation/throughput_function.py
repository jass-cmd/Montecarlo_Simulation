import numpy as np

def triangular_th_generator(min_value=3, mode=5, max_value=9):
    return round(np.random.triangular(min_value, mode, max_value))


def get_capacity_multiplier(risks):
    """
    Returns a risk multiplier based on the defined probability-impact pairs.
    """
    r = np.random.rand()
    cumulative = 0

    for risk in risks:
        cumulative += risk["prob"]
        if r < cumulative:
            return risk["impact"]

    return 1.0


def simulate_project_delivery(
    ticket_goal=150,
    min_val=3,
    mode=5,
    max_val=9,
    risks=None
):
    """
    Simulates the number of weeks required to complete a project
    with throughput driven by a triangular distribution and
    influenced by probabilistic risk factors.

    Parameters:
        ticket_goal (int): Number of tickets to deliver
        min_val (int): Minimum weekly throughput
        mode (int): Most likely weekly throughput
        max_val (int): Maximum weekly throughput
        risks (list): List of risk dicts with 'prob' and 'impact'

    Returns:
        int: Number of weeks to reach the ticket goal
    """

    if risks is None:
        risks = [
            {"prob": 0.05, "impact": 0.90},  # team vacation
            {"prob": 0.10, "impact": 0.80},  # client dependency
            {"prob": 0.20, "impact": 1.30},  # exceptional performance
        ]
    
    delivered = 0
    weeks = 0

    while delivered < ticket_goal:
        base_th = triangular_th_generator(min_val, mode, max_val)
        multiplier = get_capacity_multiplier(risks)
        adjusted_th = max(1, round(base_th * multiplier))  # garantiza mínimo de 1
        delivered += adjusted_th
        weeks += 1

    return weeks
