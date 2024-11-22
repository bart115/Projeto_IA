def inicializar_veiculos():
    veiculos = [
        {"tipo": "drone", "capacidade": 10, "velocidade": 50, "autonomia": 20, "acessibilidade": ["drone"]},
        {"tipo": "camiao", "capacidade": 2000, "velocidade": 60, "autonomia": 500, "acessibilidade": ["camiao"]},
        {"tipo": "helicoptero", "capacidade": 500, "velocidade": 120, "autonomia": 100, "acessibilidade": ["helicoptero"]},
    ]
    return veiculos
