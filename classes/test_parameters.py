import unittest
from Simulation_Params import SimulationParameters

class TestsParameters(unittest.TestCase):

    def test_happypath(self): 
        parameters = SimulationParameters(150, 3, 5, 9, 1000)
        expected = {"backlog": 150,"th_min": 3,"th_ex": 5,"th_max": 9,"num_sim": 1000}
        self.assertEqual(parameters.to_dict(), expected)

    def test_th_not_ordered(self): 
        with self.assertRaises(ValueError):
            SimulationParameters(150, 5, 1, 9, 1000)
    
    def test_fields_cannot_be_zero(self):

        test_cases = [

            {"backlog": 0, "th_min": 3, "th_ex": 5, "th_max": 9, "num_sim": 1000},
            {"backlog": 150, "th_min": 0, "th_ex": 5, "th_max": 9, "num_sim": 1000},
            {"backlog": 150, "th_min": 3, "th_ex": 0, "th_max": 9, "num_sim": 1000},
            {"backlog": 150, "th_min": 3, "th_ex": 5, "th_max": 0, "num_sim": 1000},
            {"backlog": 150, "th_min": 3, "th_ex": 5, "th_max": 9, "num_sim": 0}, 
        ]
       
        for case in test_cases:

            with self.assertRaises(ValueError):
                SimulationParameters(

                        case["backlog"],
                        case["th_min"],
                        case["th_ex"],
                        case["th_max"],
                        case["num_sim"]
                        
                    )
                






if __name__ == '__main__':
    unittest.main()
