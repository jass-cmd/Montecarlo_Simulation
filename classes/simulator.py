import numpy as np
from simulation_params import SimulationParameters
from risk_class import Risk


class Simulator: 

    def __init__(self, parameters: SimulationParameters, risks: list[Risk]): 
        
        """
        Initialize the constructer with already validated objects from
        SimulationParameters and Risk classes.

        """
        
        