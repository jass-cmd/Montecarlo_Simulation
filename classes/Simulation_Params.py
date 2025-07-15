class SimulationParameters: 
    """
    This class captures the simulation parameters.
    Validates them and make sure the object is create after
    bien fully validated
    """
    def __init__(self, backlog:int, th_min:int, th_ex:int, th_max:int, num_sim:int):
        
        SimulationParameters._data_validation(backlog, th_min, th_ex, th_max, num_sim)

        self.backlog = backlog
        self.th_min = th_min
        self.th_ex = th_ex
        self.th_max = th_max
        self.num_sim = num_sim
    
    @staticmethod
    def _data_validation(backlog, th_min, th_ex, th_max, num_sim):
        """
        This method is in charge of validating the inputs user.
        More specifcally it's content.

        """
        tempdict = {
             
             "backlog":backlog,
             "th_min":th_min,
             "th_ex":th_ex,
             "th_max":th_max,
             "num_sim":num_sim
        }
         
        for key, value in tempdict.items():
             if value is None or not isinstance(value, int):
                 raise TypeError(f"The field {key} must be an Integer")
             
             if (value <= 0): 
                 raise ValueError(f"{key} cannot be less or equal zero")
                 
        if not (th_min < th_ex < th_max):
            raise ValueError("Throughput must follow th_min < th_ex < th_max")
         
    @staticmethod
    def from_dict(data:dict): 
        """
        This method takes a dict (user's input) and
        converts them into a obj after calling the constructor
        and validating the data.
        """
        keys = ["backlog", "th_min", "th_ex", "th_max", "num_sim"]

        for x in keys:
            if x not in data:
                raise ValueError(f"Field {x} is missing")
        
        return SimulationParameters (

            data["backlog"],
            data["th_min"],
            data["th_ex"],
            data["th_max"],
            data["num_sim"]
        )

    def to_dict(self): 
        """
        Converts an obj into a dict for future serialization 
        and data analysis.
        
        """
        return {
            "backlog":self.backlog,
            "th_min":self.th_min,
            "th_ex":self.th_ex,
            "th_max":self.th_max,
            "num_sim":self.num_sim
        }
    
    def __str__(self):
        return (f"SimulationParameters(backlog={self.backlog}, th_min={self.th_min}, th_ex={self.th_ex}, th_max={self.th_max}, num_sim={self.num_sim})")
    
    def __repr__(self):
        return (f"{self.backlog}, {self.th_min}, {self.th_ex}, {self.th_max}, {self.num_sim}")