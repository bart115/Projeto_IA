import matplotlib.pyplot as plt
import networkx as nx
import threading
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

def encontrar_melhores_rotas(grafo, veiculos, func):
    resultados = []

    for veiculo in veiculos:
        print("Veículo recebido:", veiculo)
        autonomia_restante = veiculo["autonomia"]  # Verifique o tipo de `veiculo` aqui

    
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
                    caminho = func(grafo, rota_atual[-1], zona, veiculo)
                    if not caminho:
                        continue
                    
                    custo_caminho = 0
                    for i in range(len(caminho)-1):
                        dados = grafo[caminho[i]][caminho[i+1]]
                        custo_caminho += dados['distancia'] / veiculo['velocidade']
                    
                    if custo_caminho <= autonomia_restante:
                        score_ajustado = scores_zonas[zona] / custo_caminho
                        if score_ajustado > melhor_score:
                            melhor_score = score_ajustado
                            melhor_proxima_zona = zona
                            melhor_caminho = caminho[1:]
                            custo_total = custo_caminho
            
            if melhor_proxima_zona:
                rota_atual.extend(melhor_caminho)
                autonomia_restante -= custo_total
                if autonomia_restante < 0:
                    autonomia_restante = 0
            else:
                break
        
        resultados.append({
            "veiculo": veiculo["tipo"],
            "rota": rota_atual,
            "zonas_atendidas": len(rota_atual) - 1,
            "autonomia_restante": autonomia_restante
        })
    
    return resultados  # Apenas retorna os resultados, sem exibir


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

def exibir_grafo(grafo, rota=None, tipo_veiculo=None):
    """Exibe o grafo em uma thread separada para não haver 
       conflito com o Pygame.

       Se não houver rota, exibe o grafo básico. 
       Caso contrário, exibe o grafo com a rota destacada.
    """
    def exibir():
        # Extrair as posições dos nós
        pos = nx.get_node_attributes(grafo, 'pos')
        
        # Desenhar o grafo básico
        plt.figure(figsize=(8, 6))
        nx.draw(grafo, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
        
        # Destacar a rota encontrada
        if rota: 
            rota_arestas = [(rota[i], rota[i+1]) for i in range(len(rota) - 1)]
            nx.draw_networkx_edges(grafo, pos, edgelist=rota_arestas, edge_color='red', width=2.5)
        
            if tipo_veiculo: 
                plt.title(f"Rota Calculada para o Veículo: {tipo_veiculo}")
            else:
                plt.title("Rota Destacada")
        
        else:
            plt.title("Grafo Inicial")
        
        plt.gcf().canvas.manager.set_window_title("Exibição do Grafo")
        plt.show(block=True)

    # Iniciar o grafo em uma nova thread
    thread = threading.Thread(target=exibir)
    thread.start()

def dfs(grafo, origem, destino, veiculo):
        pilha = [(origem, [origem])]
        visitados = set()
    
        while pilha:
            (vertice, caminho) = pilha.pop()
            
            if vertice == destino:
                return caminho
                
            if vertice not in visitados:
                visitados.add(vertice)
                
                for vizinho, dados in grafo[vertice].items():
                    if vizinho not in visitados and veiculo["tipo"] in dados["acessibilidade"]:
                        pilha.append((vizinho, caminho + [vizinho]))
        
        return []

def bfs(grafo, origem, destino, veiculo):
    fila = [(origem, [origem])]
    visitados = set([origem])

    while fila:
        (vertice, caminho) = fila.pop(0)
        
        if vertice == destino:
            return caminho
            
        for vizinho, dados in grafo[vertice].items():
            if vizinho not in visitados and veiculo["tipo"] in dados["acessibilidade"]:
                visitados.add(vizinho)
                fila.append((vizinho, caminho + [vizinho]))
    
    return []

def greedy(grafo, origem, destino, veiculo):
    atual = origem
    caminho = [origem]
    visitados = set([origem])
    
    while atual != destino:
        melhor_vizinho = None
        menor_distancia = float('inf')
        
        for vizinho, dados in grafo[atual].items():
            if vizinho not in visitados and veiculo["tipo"] in dados["acessibilidade"]:
                distancia = heuristica(grafo, vizinho, destino)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    melhor_vizinho = vizinho
        
        if melhor_vizinho is None:
            return []  # Caminho não encontrado
            
        atual = melhor_vizinho
        caminho.append(atual)
        visitados.add(atual)
        
        if atual == destino:
            return caminho
            
    return caminho
