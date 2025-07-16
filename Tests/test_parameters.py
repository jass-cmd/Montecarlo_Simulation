import pytest
from classes.simulation_params import SimulationParameters

def test_simulation_params_happypath():
    
    params = SimulationParameters(backlog=180, th_min=3, th_ex=5, th_max=9, num_sim=500)

    assert params.backlog == 180
    assert params.th_min == 3
    assert params.th_ex == 5
    assert params.th_max == 9
    assert params.num_sim == 500

@pytest.mark.parametrize ("field, value", [

        ("backlog", "not_an_int"),
        ("th_min", 3.5),
        ("th_ex", None),
        ("th_max","8"),
        ("num_sim", 0),
])

def test_validation_typeError(field, value):

    valid_data = {

        "backlog": 200,
        "th_min": 3,
        "th_ex": 5,
        "th_max": 9,
        "num_sim": 500
    }

    valid_data[field]=value

    with pytest.raises(TypeError) as excinfo:
        SimulationParameters(**valid_data)

    assert field in str(excinfo.value)

@pytest.mark.parametrize("th_min, th_ex, th_max",[
    
    (5, 3, 9),   # th_min > th_ex
    (3, 8, 7),   # th_ex > th_max
    (6, 6, 6),   # todos iguales
    (3, 9, 5),   # ex > max
    (9, 7, 6),   # todo mal

])

def test_th_unqual(th_min, th_ex,th_max): 
    with pytest.arises (ValueError, match="Throughput must follow"):
      
      SimulationParameters(
            backlog=100,
            th_min=th_min,
            th_ex=th_ex,
            th_max=th_max,
            num_sim=1000
        )