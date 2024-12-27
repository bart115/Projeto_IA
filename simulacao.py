import random

def simular_cenario(grafo):
    # Simular alterações climáticas
    for u, v, dados in grafo.edges(data=True):
        if random.random() < 0.3:  # 30% de chance de mau tempo
            print(f"Condições climáticas pioraram entre {u} e {v}. Tempo de viagem aumentado.")
            dados["tempo"] *= 1.5  # Tempo de viagem aumenta 50%
            print(f"Novo tempo de viagem: {dados['tempo']} horas")
    # Simular bloqueios de rotas
    for u, v in list(grafo.edges()):
        if random.random() < 0.2:  # 20% de chance de bloqueio
            print(f"Rota entre {u} e {v} está bloqueada!")
            grafo.remove_edge(u, v)
