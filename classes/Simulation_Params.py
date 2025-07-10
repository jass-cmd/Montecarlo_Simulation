class SimulationParameters:
    
    """
    Represents the input parameters required to run the simulation.
    it is designed to validate user input and support the integration with a frontend application.
    """

    def __init__(self, backlog: int, th_min: int, th_ex: int, th_max: int, num_sim: int):
        # Apply rounding and type casting
        self.backlog = int(round(backlog))
        self.th_min = int(round(th_min))
        self.th_ex = int(round(th_ex))
        self.th_max = int(round(th_max))
        self.num_sim = int(round(num_sim))

        # Run validations
        self._validate()

    def _validate(self):
        if not (self.th_min < self.th_ex < self.th_max):
            raise ValueError("Throughput values must follow th_min < th_ex < th_max")
        
        for attr in ["backlog", "th_min", "th_ex", "th_max", "num_sim"]:
            value = getattr(self, attr)
            if value <= 0:
                raise ValueError(f"{attr} must be greater than 0")

    def __str__(self):
        return f"SimulationParameters(backlog={self.backlog}, th_min={self.th_min}, th_ex={self.th_ex}, th_max={self.th_max}, num_sim={self.num_sim})"

    def __repr__(self):
        return f"{self.backlog}, {self.th_min}, {self.th_ex}, {self.th_max}, {self.num_sim}"

    def to_dict(self) -> dict:
        return {
            "backlog": self.backlog,
            "th_min": self.th_min,
            "th_ex": self.th_ex,
            "th_max": self.th_max,
            "num_sim": self.num_sim
        }

    @staticmethod
    def from_dict(data: dict) -> "SimulationParameters":
        try:
            return SimulationParameters(
                backlog=data["backlog"],
                th_min=data["th_min"],
                th_ex=data["th_ex"],
                th_max=data["th_max"],
                num_sim=data["num_sim"]
            )
        except KeyError as e:
            raise ValueError(f"Missing required field: {e.args[0]}")
