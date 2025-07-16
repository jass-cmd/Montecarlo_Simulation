# import pytest
# from my_module import my_function  # o tu clase

# @pytest.mark.parametrize("param1, param2, expected", [
#     (valor1, valor2, resultado_esperado),
#     (valor3, valor4, resultado_esperado),
#     (valor5, valor6, resultado_esperado),
# ])
# def test_nombre_claro(param1, param2, expected):
#     result = my_function(param1, param2)
#     assert result == expected

# for clases `@pytest.mark.parametrize("campo, valor",[
#     ("backlog", "string"),
#     ("th_min", -1),
# ])`

# 
# def test_input_invalido_para_clase(campo, valor):
#     params = {
#         "backlog": 100,
#         "th_min": 3,
#         "th_ex": 5,
#         "th_max": 9,
#         "num_sim": 500
#     }
#     params[campo] = valor

#     with pytest.raises(TypeError):
#         SimulationParameters(**params)
