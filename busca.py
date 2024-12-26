import matplotlib.pyplot as plt
import networkx as nx
from heapq import heappop, heappush
from formulacao import EstadoDistribuicao, Operador

def encontrar_melhores_rotas(grafo, veiculos, destino):
    """
    Encontra as melhores rotas para cada veículo até o destino
    """
    resultados = []
    
    for veiculo in veiculos:
        # Usar A* para encontrar o melhor caminho
        melhor_rota = astar_search(
            grafo, 
            veiculo['pos_atual'],
            destino,
            veiculo,
            heuristica_distancia
        )
        
        if melhor_rota:
            resultados.append({
                'veiculo': veiculo['tipo'],
                'rota': melhor_rota,
            })
            
            # Mostrar grafo com a rota destacada
            mostrar_rota(grafo, melhor_rota, veiculo['tipo'])
    
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


def astar_search(grafo, inicio, destino, veiculo, heuristica):
    """
    Implementa o algoritmo A* para encontrar o melhor caminho
    """
    fronteira = [(0, inicio, [])]
    explorados = set()
    g_score = {inicio: 0}
    
    while fronteira:
        f_atual, no_atual, caminho = heappop(fronteira)
        
        if no_atual == destino:
            return caminho + [no_atual]
            
        if no_atual in explorados:
            continue
            
        explorados.add(no_atual)
        
        for vizinho in grafo[no_atual]:
            if veiculo['tipo'] not in grafo[no_atual][vizinho]['acessibilidade']:
                continue
                
            novo_g = g_score[no_atual] + grafo[no_atual][vizinho]['tempo']
            
            if vizinho not in g_score or novo_g < g_score[vizinho]:
                g_score[vizinho] = novo_g
                f_score = novo_g + heuristica(grafo, vizinho, destino)
                heappush(fronteira, (f_score, vizinho, caminho + [no_atual]))
    
    return None

def heuristica_distancia(grafo, atual, destino):
    """
    Calcula a heurística baseada na distância euclidiana
    """
    pos_atual = grafo.nodes[atual]['pos']
    pos_destino = grafo.nodes[destino]['pos']
    return ((pos_atual[0] - pos_destino[0])**2 + 
            (pos_atual[1] - pos_destino[1])**2)**0.5

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
