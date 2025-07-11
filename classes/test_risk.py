import unittest
from Risk_class import Risk 

class TestRisk (unittest.TestCase): #esta clase hereda de unittest.testcase los metodos que empiezan con test_ para testear
    pass

#positive test

    def test_valid_risk_creation(self):
        risk = Risk("Client delay", 0.3, 0.5)
        self.assertEqual(risk.name, "Client delay")
        self.assertEqual(risk.probability, 0.3)
        self.assertEqual(risk.impact, 0.5)
    
    def test_invalid_prob(self):
        with self.assertRaises(ValueError):
            Risk("Bad Risk", 1.5, 0.2)

    def test_invalid_type(self):
        with self.assertRaises(TypeError): 
            Risk("Dependencies", "high", 0.8)

    def test_invalid_name(self):
        with self.assertRaises(TypeError):
            Risk("", 0.9, 0.7)

    def test_integer(self):
        with self.assertRaises(ValueError):
            Risk("test5", 23, 9)


    def test_to_dict(self):
        risk = Risk("Risk Name", 0.8, 0.7)
        expected = {"name":"Risk Name", "probability":0.8, "impact":0.7}
        self.assertEqual (risk.to_dict(), expected)


if __name__ == '__main__':
    unittest.main()