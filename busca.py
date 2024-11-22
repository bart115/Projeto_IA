import matplotlib.pyplot as plt
import networkx as nx
from heapq import heappop, heappush

def encontrar_melhores_rotas(grafo, veiculos):
    resultados = []
    
    for veiculo in veiculos:
        melhor_rota = dijkstra(grafo, "zona1", "zona3", veiculo)
        resultados.append({
            "veiculo": veiculo["tipo"],
            "rota": melhor_rota,
        })
        
        # Mostrar grafo com a rota destacada
        mostrar_rota(grafo, melhor_rota, veiculo["tipo"])
    
    return resultados

def dijkstra(grafo, origem, destino, veiculo):
    distancias = {no: float('inf') for no in grafo}
    distancias[origem] = 0
    fila = [(0, origem, [])]
    melhor_rota = []

    while fila:
        dist, atual, caminho = heappop(fila)

        if atual == destino:
            melhor_rota = caminho + [atual]
            break

        for vizinho, dados in grafo[atual].items():
            if veiculo["tipo"] in dados["acessibilidade"]:
                peso = dados["tempo"]
                nova_dist = dist + peso

                if nova_dist < distancias[vizinho]:
                    distancias[vizinho] = nova_dist
                    heappush(fila, (nova_dist, vizinho, caminho + [atual]))

    return melhor_rota

def mostrar_rota(grafo, rota, tipo_veiculo):
    # Extrair as posições dos nós
    pos = nx.get_node_attributes(grafo, 'pos')
    
    # Desenhar o grafo básico
    plt.figure(figsize=(8, 6))
    nx.draw(grafo, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
    
    # Destacar a rota encontrada
    rota_arestas = [(rota[i], rota[i+1]) for i in range(len(rota) - 1)]
    nx.draw_networkx_edges(grafo, pos, edgelist=rota_arestas, edge_color='red', width=2.5)
    
    plt.title(f"Rota Calculada para o Veículo: {tipo_veiculo}")
    plt.gcf().canvas.manager.set_window_title("Rota Calculada")

    plt.show()
