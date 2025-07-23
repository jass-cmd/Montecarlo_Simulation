import numpy as np
import pandas as pd

class SimulationAnalyzer:
    """
    Analiza un único resultado de simulación Monte Carlo,
    donde cada valor es la semana de finalización ('completion_week').
    """

    def __init__(self, completion_weeks: np.ndarray):
        """
        :param completion_weeks: 1D array con la semana de entrega
                                 de cada réplica de la simulación.
        """
        self.df = pd.DataFrame({
            'sim_run': np.arange(len(completion_weeks)),  # réplica 0,1,2…
            'completion_week': completion_weeks           # resultado por réplica
        })

    def summary(self, percentiles=(0.5, 0.9)) -> pd.DataFrame:
        """
        Calcula los percentiles deseados de 'completion_week'.
        Devuelve un DataFrame con columnas ['pXX', ...].
        """
        agg_kwargs = {
            f"p{int(p*100)}": (lambda x, q=p: x.quantile(q))
            for p in percentiles
        }
        return self.df['completion_week'].agg(**agg_kwargs).to_frame().T

    def overall_stats(self) -> pd.Series:
        """Estadísticas descriptivas (count, mean, std, min, 25%, 50%, 75%, max)."""
        return self.df['completion_week'].describe()

    def filter_outliers(self, z_thresh=3.0) -> pd.DataFrame:
        """Elimina las réplicas cuya completion_week esté fuera de z_thresh z-scores."""
        arr = self.df['completion_week'].to_numpy()
        mean, std = arr.mean(), arr.std(ddof=0)
        mask = np.abs((arr - mean) / std) <= z_thresh
        return self.df.loc[mask].reset_index(drop=True)
