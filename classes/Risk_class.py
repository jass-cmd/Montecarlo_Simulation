class Risk:
    """
    This class's purpose is to model risks that can affect a team's productivity.
    It also includes data validation methods to make sure the object is fully validated 
    and usable by other classes such as the Simulator class.

    """
    def __init__(self, risk_name:str , probability:float, impact:float):

        Risk._data_validation(risk_name, probability, impact)

        self.risk_name = risk_name
        self.probability = probability
        self.impact = impact

    @staticmethod
    def _data_validation(risk_name, probability, impact):
        
        if not isinstance (risk_name, str) or not risk_name.strip():
            raise TypeError ("Risk name must a non empty string")
        
        parameters = {"probability": probability, "impact": impact}
        for key, value in parameters.items():
            if not (0 < value < 1):
                raise ValueError (f"The field {key} has to be a value between 0 and 1 (eg. 0.4 --> 40%)")


    def to_dict(self): 
        return {

        "risk_name": self.risk_name,
        "probability": self.probability,
        "impact": self.impact

        }
    
    @staticmethod
    def from_dict(data:dict):
       try:
            return Risk (
            data["risk_name"],
            data["probability"],
            data["impact"]
        )

       except KeyError as e:
              raise ValueError (f"The field {e.args[0]} is missing the input data")
    
                
    def __str__(self):
        return f"Risk (risk_name={self.risk_name}, probability={self.probability}, impact={self.impact})"
    
    def __repr__(self):
        return f"({self.risk_name},{self.probability},{self.impact})"

    
