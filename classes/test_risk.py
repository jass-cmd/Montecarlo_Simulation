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

if __name__ == '__main__':
    unittest.main()