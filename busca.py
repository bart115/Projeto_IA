import matplotlib.pyplot as plt
import networkx as nx
from heapq import heappop, heappush

def heuristica(grafo, atual, destino):
    """Calcula distância euclidiana entre dois pontos"""
    x1, y1 = grafo.nodes[atual]['pos']
    x2, y2 = grafo.nodes[destino]['pos']
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def a_star(grafo, origem, destino, veiculo):
    fronteira = [(0, origem, [])]  # (f_score, node, path)
    g_score = {origem: 0}
    f_score = {origem: heuristica(grafo, origem, destino)}
    
    while fronteira:
        _, atual, caminho = heappop(fronteira)
        
        if atual == destino:
            return caminho + [atual]
            
        for vizinho, dados in grafo[atual].items():
            if veiculo["tipo"] not in dados["acessibilidade"]:
                continue
                
            # Calcular g_score para este vizinho
            tempo_base = dados["tempo"]
            velocidade_relativa = veiculo["velocidade"] / 60.0
            peso = tempo_base / velocidade_relativa
            tentative_g = g_score[atual] + peso
            
            if vizinho not in g_score or tentative_g < g_score[vizinho]:
                g_score[vizinho] = tentative_g
                f_score[vizinho] = tentative_g + heuristica(grafo, vizinho, destino)
                heappush(fronteira, (f_score[vizinho], vizinho, caminho + [atual]))
    
    return []

def encontrar_melhores_rotas(grafo, veiculos):
    resultados = []
    
    for veiculo in veiculos:
        scores_zonas = {
            zona: (grafo.nodes[zona]['populacao'] * grafo.nodes[zona]['gravidade']) / 100
            for zona in grafo.nodes()
        }
        
        rota_atual = ['zona1']
        autonomia_restante = veiculo['autonomia']
        
        while autonomia_restante > 0:
            melhor_proxima_zona = None
            melhor_score = 0
            melhor_caminho = []
            custo_total = float('inf')
            
            for zona in grafo.nodes():
                if zona not in rota_atual:
                    # Usar A* para encontrar caminho
                    caminho = a_star(grafo, rota_atual[-1], zona, veiculo)
                    if not caminho:
                        continue
                        
                    # Calcular custo total do caminho
                    custo_caminho = 0
                    for i in range(len(caminho)-1):
                        dados = grafo[caminho[i]][caminho[i+1]]
                        custo_caminho += dados['distancia'] / veiculo['velocidade']
                    
                    # Verificar se a autonomia permite completar o caminho
                    if custo_caminho <= autonomia_restante:
                        score_ajustado = scores_zonas[zona] / custo_caminho
                        if score_ajustado > melhor_score:
                            melhor_score = score_ajustado
                            melhor_proxima_zona = zona
                            melhor_caminho = caminho[1:]  # Excluir nó atual
                            custo_total = custo_caminho
            
            if melhor_proxima_zona:
                rota_atual.extend(melhor_caminho)
                autonomia_restante -= custo_total
                if autonomia_restante < 0:  # Segurança extra para evitar valores negativos
                    autonomia_restante = 0
            else:
                break  # Nenhuma zona acessível com a autonomia restante
        
        resultados.append({
            "veiculo": veiculo["tipo"],
            "rota": rota_atual,
            "zonas_atendidas": len(rota_atual) - 1,
            "autonomia_restante": autonomia_restante
        })
        
        mostrar_rota(grafo, rota_atual, veiculo["tipo"])
    
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
            # Verificar se o veículo pode usar esta rota
            if veiculo["tipo"] in dados["acessibilidade"]:
                # Calcular tempo considerando velocidade do veículo
                tempo_base = dados["tempo"]
                velocidade_relativa = veiculo["velocidade"] / 60.0  # Normalizar velocidade
                peso = tempo_base / velocidade_relativa
                
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
