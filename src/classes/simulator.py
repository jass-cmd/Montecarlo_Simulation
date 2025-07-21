import numpy as np
from simulation_params import SimulationParameters
from risk_class import Risk

class Simulator:
    """
    Monte Carlo simulation of project delivery time based on throughput(obj) and risks(obj).
    """
    def __init__(self, parameters:SimulationParameters, risks: list[Risk]):
        
           self.parameters = parameters
           self.risks = risks
           self.results = None 

    """
    Saves the initial state of the object.
    Creates the atributes of the obj (parameters andn risks)
    Self results will save the results of the simulation. 
    This will later be used for data visualization, convergence and sensibility analysis.

    """
    def run_simulation(self, max_weeks: int = 200):

        """
        Unpack the values that will be used in the simulation
        """
        backlog = self.parameters.backlog
        num_sim = self.parameters.num_sim
        th_min = self.parameters.th_min
        th_ex = self.parameters.th_ex
        th_max = self.parameters.th_max

        
        """
        Run the simulation to get a matrix of throughput values not adjusted by risks.
        It's already and ndarray so vectorizaed operations can be used.
        """
        base_throughput = np.random.triangular(
            
            left=th_min,
            mode=th_ex,
            right=th_max,
            size=(num_sim, max_weeks)
            
            )
        
        #Apply risks to the whole ndarray of throughput values
        adjusted_throughput = self._apply_risks_vectorized(base_throughput)

        #Get the cumulative throughput per row (axis = 1)
        cumulative_throughput = np.cumsum(adjusted_throughput, axis=1)

        #Creates a boolean matrix (mask) to identify the when the simulation hit the target backlog for the first time
        reached = cumulative_throughput >= backlog #it uses broadcasting to apply the operator to the whole matrix
        first_success = np.argmax(reached, axis=1) + 1  # +1 because of 0-based index
        

        self.results = first_success
        return self.results

    def _apply_risks_vectorized(self, throughput: np.ndarray) -> np.ndarray:
        """
        Applies risks across the entire matrix using broadcasting and masks.
        """
        adjusted = throughput.copy()

        for risk in self.risks:
            #createas a boolean matrix (mask) to determine when the risk occurs
            risk_occurs = np.random.rand(*throughput.shape) < risk.probability

            #apply risks to base throughput through the mask for everr risk added by the user (warning: it accumulates risks)
            adjusted = np.where(risk_occurs, adjusted * risk.impact, adjusted)

        return adjusted

    def get_results(self) -> np.ndarray:

        #just for safety, it requires the simulation to run before getting the results.
        if self.results is None:
            raise RuntimeError("Simulation has not been run yet.")
        return self.results
    