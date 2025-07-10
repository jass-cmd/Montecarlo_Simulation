class Risk:
    """
    This class was designed to control and validate the risk input from the user.
    Also, by separating this from the parameters, a user can run simulation without having to add risks.
    
    """
    def __init__(self, name:str, probability, impact):

        #data type validations
        if not isinstance(name, str) or not name.strip():
            raise TypeError("You have to add a name to your risk and it has to be string (eg. client dependencies).")
        
        #Float validation
        try:
            probability = float(probability)
            impact = float(impact)

        except (ValueError,TypeError):
            raise TypeError("Probability and Impact must be numeric values.")

        #data content validations
        if not (0 <= probability <=1) or not (0 <= impact <= 1):
            raise ValueError("This has to be a number between 0 and 1 (eg.0.4 --> 40%))")
        
        self.name=name
        self.probability=probability
        self.impact=impact
    
    @staticmethod
    def list_from_dicts(data_list:list) -> list:

        #this method transforms the dicts to an obj already validated by __init__
        #the users are able to add multiple risks, therefore I need to save them all in a list and create a list of objects.

        risks=[]
        for item in data_list:
            try:
                risk = Risk(
                    name=item["name"],
                    probability=item["probability"],
                    impact=item["impact"]
                )
                risks.append(risk)
            except KeyError as e:
                raise KeyError(f"Missing value 'name', 'probability' or 'impact'] in risk input: {e}")
            except Exception as e:
                raise ValueError(f"Error creating Risk object: {e}")
        return risks

    
    #this converts an OBJ to a dict for serialization and posterior use.
    def to_dict(self)-> dict:
        return {
            "name":self.name,
            "probability":self.probability,
            "impact":self.impact
        }
    
    def __str__(self):
        return f"Risk(name={self.name}, probability={self.probability}, impact={self.impact})"
    
    def __repr__(self):
        return f"Risk(name='{self.name}', probability={self.probability}, impact={self.impact})"

 