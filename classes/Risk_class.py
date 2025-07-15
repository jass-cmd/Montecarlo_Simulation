class Risk: 

    def __init__(self, risk_name: str, probability: float, impact: float):

        Risk._data_validation(risk_name, probability, impact)

        self.risk_name = risk_name
        self.probability = probability
        self.impact = impact

    @staticmethod
    def _data_validation(risk_name, probability, impact):

        if risk_name is None or not isinstance(risk_name, str) or not risk_name.strip(): 
                raise TypeError("This field must be a string and must not be empty")
        
        risk_parameters = {"probability":probability, "impact":impact}
    
        for field, value in risk_parameters.items():
            
            if value is None or not (0 < value < 1):
                raise ValueError(f"Field {field} must be values between 0 and 1 (eg. 0.40 ---> 40%)")
            
    @staticmethod
    def from_dict(data: dict):

        dict_keys = ["risk_name","probability","impact"]
        for keys in  dict_keys:
             if keys not in data:
                  raise KeyError(f"The key {keys} is missing")
        
             value = data[keys]
             if value is None:
                  raise ValueError(f"The field {keys} can't be none")
             
             if isinstance (value, str) and not value.strip():
                  raise ValueError(f"the field {keys} cannot be an empty string")
             
        return Risk (
             
            data["risk_name"],
            data["probability"],
            data["impact"]
        )
    
    def to_dict(self):
         
         return {
              "risk_name":self.risk_name,
              "probability":self.probability,
              "impact": self.impact
         }
    
    @staticmethod
    def parse(data):
         
         if isinstance(data, dict):
              return [Risk.from_dict(data)]
        
         elif isinstance(data, list):
            risks = []
            for i, item in enumerate(data):
                 if not isinstance(item, dict):
                      raise TypeError(f"Error at index {i}. This is not a dictionary")
                 
                 try:
                      obj=Risk.from_dict(item)
                      risks.append(obj)
                 except ValueError as e:
                      raise ValueError(f"Error at index {i}. {e}")
            
            return risks
         else:
              raise TypeError("This input must be a dictionary or a list of dictionaries.")
         

    def __str__(self):
         return f"(Risk={self.risk_name}, probability={self.probability}, impact={self.impact})"
    
    def __repr__(self):
         return f"({self.risk_name}, {self.probability}, {self.impact})"