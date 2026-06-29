import pandas as pd

def load_employees():

    data = [

        {
            "id":1,
            "nombre":"Juan Perez",
            "puesto":"Chofer",
            "salario_mensual":373093
        },

        {
            "id":2,
            "nombre":"Ana Mora",
            "puesto":"Operaciones",
            "salario_mensual":1200000
        },

        {
            "id":3,
            "nombre":"Carlos Soto",
            "puesto":"Bodega",
            "salario_mensual":650000
        }

    ]

    return pd.DataFrame(data)