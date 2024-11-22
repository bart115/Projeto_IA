import networkx as nx
import matplotlib.pyplot as plt

def criar_grafo():
    grafo = nx.Graph()

    # Adicionar zonas afetadas
    grafo.add_node("zona1", populacao=1000, gravidade=5, tempo_critico=48, pos=(0, 0))
    grafo.add_node("zona2", populacao=500, gravidade=8, tempo_critico=24, pos=(1, 1))
    grafo.add_node("zona3", populacao=200, gravidade=6, tempo_critico=36, pos=(2, 0))
    
    # Adicionar rotas entre as zonas
    grafo.add_edge("zona1", "zona2", distancia=10, tempo=1, acessibilidade=["camiao", "drone"])
    grafo.add_edge("zona2", "zona3", distancia=15, tempo=2, acessibilidade=["camiao"])
    grafo.add_edge("zona1", "zona3", distancia=20, tempo=3, acessibilidade=["helicoptero"])
    
    return grafo

def mostrar_grafo(grafo):
    # Extrair as posições dos nós
    pos = nx.get_node_attributes(grafo, 'pos')
    
    # Desenhar o grafo
    plt.figure(figsize=(8, 6))
    nx.draw(grafo, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')
    
    # Adicionar rótulos de pesos (distâncias nas arestas)
    edge_labels = nx.get_edge_attributes(grafo, 'distancia')
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels)
    
    plt.gcf().canvas.manager.set_window_title("Grafo de Zonas e Rotas")
    plt.show()
