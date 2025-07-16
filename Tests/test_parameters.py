import pytest
from classes.simulation_params import SimulationParameters

def test_parameters_happypath():

    paramns = SimulationParameters(backlog=100, th_min=3, th_ex=5, th_max=9, num_sim=1000)

    assert paramns.backlog == 100
    assert paramns.th_min == 3
    assert paramns.th_ex == 5
    assert paramns.th_max == 9
    assert paramns.num_sim == 1000

@pytest.mark.parametrize("field, value",[

        ("backlog", None), #should fail, It's trying to break the no none values validation
        ("th_min", -3), #should fail, it's trying to break the <= 0 validation
        ("th_ex", 3.5), #should fail, it's trying to break the no float validation
        ("th_max", 0), #should fail, it's trying to break the no 0 values validation
        ("num_sim", "1000"), #should fail, it's trying to break the only integers validation

])

def test_class_typeError(field, value):
    
    params = {

        "backlog":100,
        "th_min":3,
        "th_ex":5,
        "th_max":9,
        "num_sim":1000
    }
     
    params[field] = value

    with pytest.raises((TypeError, ValueError)) as exc_info:
            SimulationParameters(**params)

@pytest.mark.parametrize("th_min, th_ex, th_max", [

        (5, 1, 3), #--th_min > th_ex < th_max-- should fail, it's trying to break the th_min < th_ex < th_max validation
        (3, 4, 2), #--th_min < th_ex > th_max-- should fail, it's trying to break the th_min < th_ex < th_max validation
        (8, 5, 3), #--th_min > th_ex > th_max-- should fail, it's trying to break the th_min < th_ex < th_max validation
 
])

def test_th_order(th_min, th_ex, th_max): 
     

     th_values = {
          
        "backlog":100,
        "th_min":th_min,
        "th_ex":th_ex,
        "th_max":th_max,
        "num_sim":1000
     }

     with pytest.raises(ValueError) as exc_info:
          SimulationParameters(**th_values)


     print (exc_info)
     print (exc_info.type)


@pytest.mark.parametrize("missing_key", [
    "backlog",
    "th_min",
    "th_ex",
    "th_max",
    "num_sim",
])
def test_missing_field_in_dict(missing_key):
    keys_values = {
        "backlog": 100,
        "th_min": 3,
        "th_ex": 5,
        "th_max": 9,
        "num_sim": 500
    }

    keys_values.pop(missing_key)

    with pytest.raises(ValueError) as exc_info:
        SimulationParameters.from_dict(keys_values)

    assert f"Field {missing_key} is missing" in str(exc_info.value)
    print(f"Missing field: {missing_key} -> {exc_info.value}")


def test_to_dict():
     
     input_data = {
          
          "backlog": 100,
          "th_min": 3,
          "th_ex": 5,
          "th_max": 9,
          "num_sim": 500

     }

     params = SimulationParameters(**input_data)
     
     assert params.to_dict() == input_data