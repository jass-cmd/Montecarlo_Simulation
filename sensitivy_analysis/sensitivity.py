import sys # Agrega la carpeta raíz del proyecto al path
import os
import numpy as np 


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

sensitivity_configs = [ #Risks scenarios
    {
        "name": "Base case",
        "ticket_goal": 150,
        "min_val": 3,
        "mode": 5,
        "max_val": 9,
        "risks": [
            {"prob": 0.05, "impact": 0.90},
            {"prob": 0.10, "impact": 0.80},
            {"prob": 0.20, "impact": 1.30}
        ]
    },
    {
        "name": "Lower throughput",
        "ticket_goal": 150,
        "min_val": 2,
        "mode": 4,
        "max_val": 7,
        "risks": [
            {"prob": 0.05, "impact": 0.90},
            {"prob": 0.10, "impact": 0.80},
            {"prob": 0.20, "impact": 1.30}
        ]
    },
    {
        "name": "High risk frequency",
        "ticket_goal": 150,
        "min_val": 3,
        "mode": 5,
        "max_val": 9,
        "risks": [
            {"prob": 0.10, "impact": 0.90},
            {"prob": 0.20, "impact": 0.80},
            {"prob": 0.30, "impact": 1.30}
        ]
    }
]


from simulation.throughput_function import simulate_project_delivery


def run_simulation_with_params (config, runs=1000):
    results = []

    for _ in range (runs):
        result = simulate_project_delivery(
            ticket_goal=config["ticket_goal"],
            min_val=config["min_val"],
            mode=config["mode"],
            max_val=config["max_val"],
            risks=config["risks"]
        )
        results.append(result)

    return results


if __name__ == "__main__":
    data = run_simulation_with_params(sensitivity_configs[0])
    print(f"Primeras 10 simulaciones: {data[:10]}")
    print(f"Promedio: {np.mean(data):.2f} semanas")
