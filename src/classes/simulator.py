import numpy as np
from simulation_params import SimulationParameters
from risk_class import Risk

class Simulator:
    """
    Vectorized Monte Carlo simulation of project delivery time based on throughput(obj) and risks(obj).
    """
    def __init__(self, parameters:SimulationParameters, risks: list[Risk]):
        
            self.parameters = parameters
            self.risks = risks
            self.results = None # this will be np.ndarray with simulation durations

    """
    Metodo constructor de la clase, guarda el estado inicial del objeto.
    Crea los atributos que va a guardar los riesgos y parametros
    ingresados por el usuario. Es importante saber que estos atributos 
    quedan disponible para usar desde cualquier parte del codigo del objeto.
    El atributo self.results va a guardar los resultados luego de ejecutar la simulacion.
    Se deja como none para que si el usuario intenta obtener los resultados sin haber hecho
    la simulacion le dara error. Ademas, esto es extensible. Si el dia de manana quiero

    """
    def run_simulation(self, max_weeks: int = 200):

        backlog = self.parameters.backlog
        num_sim = self.parameters.num_sim
        th_min = self.parameters.th_min
        th_ex = self.parameters.th_ex
        th_max = self.parameters.th_max

        """
        Primero defino todas los parametros que voy a usar en la simulacion.
        
        """
        base_throughput = np.random.triangular(
       
            left=th_min,
            mode=th_ex,
            right=th_max,
            size=(num_sim, max_weeks)
        )

        """
        Genero la matriz del throughput base siguiendo una distribucion triangular
        Esto genera una matriz como la que cree en google sheets. Ya es un ndarray
        """
        # 2. Aplicar riesgos de forma vectorizada
        adjusted_throughput = self._apply_risks_vectorized(base_throughput)

        # 3. Acumulamos throughput por simulación a lo largo de las semanas
        cumulative_throughput = np.cumsum(adjusted_throughput, axis=1)

        # 4. Detectamos en qué semana se alcanza el backlog por simulación
        reached = cumulative_throughput >= backlog
        first_success = np.argmax(reached, axis=1) + 1  # +1 porque argmax da el índice 0-based
        """
        reached = cumulative_throughput >= backlog 
         
        Aplica broadcasting siguiendo ese operador >= y devuelve un ndarray de booleanos
        donde se puede ver que celdas superaron el backlog (true) o lo igualaron (true) y cuales no(false).

        first_success = np.argmax(reached, axis=1) 

        Una vez que tengo ese ndarray de booleanos, busco la primera ocurrencia de true con np argmx.
        np.argmax busca la primera ocurrencia del mayor valor y lo hace a lo largo de las filas porque 
        lo indico con axis= 1. En este caso la mayor ocurrencia es true ya que true = 1 y false = 0.
        Devuelve un array de tamaño num_sim con el indice de columna.

        """

        self.results = first_success

    def _apply_risks_vectorized(self, throughput: np.ndarray) -> np.ndarray:
        """
        Applies risks across the entire matrix using broadcasting and masks.
        """
        adjusted = throughput.copy()

        for risk in self.risks:
            # Matriz booleana: True donde el riesgo ocurre
            risk_occurs = np.random.rand(*throughput.shape) < risk.probability

            # Aplicar impacto del riesgo
            adjusted = np.where(risk_occurs, adjusted * risk.impact, adjusted)

        return adjusted

    def get_results(self) -> np.ndarray:
        if self.results is None:
            raise RuntimeError("Simulation has not been run yet.")
        return self.results