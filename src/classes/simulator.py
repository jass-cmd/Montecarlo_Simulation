import numpy as np
from simulation_params import SimulationParameters
from risk_class import Risk

class Simulator:

    """
    This class is the core class of the whole app.
    It's purpose is to take the inputs coming from SimulationParameters and Risk
    and perform the simulation following a triangular distribution probability.
    It is important to note that in this model the risks acumulates.
    """

    def __init__(self, parameters: SimulationParameters, risks: list[Risk]):

        self.parameters = parameters
        self.risks = risks
        self.results = None

    def run_simulation(self, max_weeks: int = 150) -> np.ndarray:

        """
        Takes the user input parameters and run the simulation to get the throughput base.
        No risks applied for now. The output is an ndarray of throughput values.
        """
        backlog = self.parameters.backlog
        th_min = self.parameters.th_min
        th_ex = self.parameters.th_ex
        th_max = self.parameters.th_max
        num_sim = self.parameters.num_sim

        th_base = np.random.triangular(
            left=th_min,
            mode=th_ex,
            right=th_max,
            size=(num_sim, max_weeks)
        )

        th_adjusted = self._apply_risks(th_base) #apply risks
        th_accumulated = np.cumsum(th_adjusted, axis=1) #acumulates the throughput along the rows.
        th_reached = th_accumulated >= backlog #creates a boolean ndarray (mask)
        self.results = np.argmax(th_reached, axis=1) + 1 #finds the week where th_accumulated = backlog

        return self.results

    def _apply_risks(self, th_base_matrix: np.ndarray) -> np.ndarray:

        """
        Apply risks to the throughput base not before creating a copy of it 
        for safely data manipulation
        """
        adjusted = th_base_matrix.copy()
        for risk in self.risks:
            risk_mask = np.random.rand(*th_base_matrix.shape) < risk.probability
            adjusted = np.where(risk_mask, adjusted * risk.impact, adjusted) #apply risks using the mask as filter
        return adjusted

    def get_results(self) -> np.ndarray:
        """
        This is to make sure the simulation is run before trying to pull the results.
        """
        if self.results is None:
            raise RuntimeError("The simulation has not been run yet")
        return self.results
