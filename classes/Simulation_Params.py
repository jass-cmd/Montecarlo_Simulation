class SimulationParameters: 

    def __init__(self, backlog:int, th_min:int, th_ex:int, th_max:int, num_sim:int):

                SimulationParameters._data_validation (backlog, th_min, th_ex, th_max, num_sim)
                    
                self.backlog = backlog
                self.th_min = th_min
                self.th_ex = th_ex
                self.th_max = th_max
                self.num_sim = num_sim

    @staticmethod
    def _data_validation(backlog:int, th_min:int, th_ex:int, th_max:int, num_sim:int):
                        
                tempdict = { #temporary dict to validate data

                    "backlog":backlog,
                    "th_min":th_min,
                    "th_ex":th_ex,
                    "th_max":th_max,
                    "num_sim":num_sim
                }
            
                for key, value in tempdict.items():
                    if not isinstance(value, int):
                        raise TypeError(f"{key} must be an integer")
                    
                    if value <= 0:
                        raise ValueError(f"{key} must be greater than 0")
                    
                if not (th_min < th_ex < th_max):
                            raise ValueError ("Throughput values must follow th_min < th_ex < th_max")

    def to_dict(self): 
                return {
                    "backlog": self.backlog,
                    "th_min": self.th_min,
                    "th_ex": self.th_ex,
                    "th_max": self.th_max,
                    "num_sim": self.num_sim
                }

    @staticmethod
    def from_dict(data: dict):
                        
                required_fields= ["backlog","th_min","th_ex","th_max","num_sim"]
                for x in required_fields:
                        if x not in data:
                            raise ValueError(f"Missing required field {x}")
                        
                return SimulationParameters(

                        data["backlog"],
                        data["th_min"],
                        data["th_ex"],
                        data["th_max"],
                        data["num_sim"]
                    )
                        
    def __str__(self):
            return f"SimulationParameters(backlog={self.backlog},th_min={self.th_min},th_ex={self.th_ex},th_max={self.th_max},num_sim={self.num_sim})"
    
    def __repr__(self):
            return f"{self.backlog},{self.th_min},{self.th_ex},{self.th_max},{self.num_sim}"
                    






                        
                    

                    