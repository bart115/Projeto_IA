import networkx as nx
import matplotlib.pyplot as plt

def criar_grafo():
    grafo = nx.Graph()

    # Adicionar zonas afetadas com mais informações
    grafo.add_node("zona1", 
                   populacao=1000, 
                   gravidade=5, 
                   tempo_critico=48, 
                   necessidades=500,
                   pos=(0, 0),
                   cor='lightblue')  # Cor base para as zonas
                   
    grafo.add_node("zona2", 
                   populacao=500, 
                   gravidade=8, 
                   tempo_critico=24, 
                   necessidades=300,
                   pos=(1, 1),
                   cor='lightblue')
                   
    grafo.add_node("zona3", 
                   populacao=200, 
                   gravidade=6, 
                   tempo_critico=36, 
                   necessidades=200,
                   pos=(2, 0),
                   cor='lightblue')
    
    # Adicionar rotas entre as zonas com mais detalhes
    grafo.add_edge("zona1", "zona2", 
                   distancia=10, 
                   tempo=1, 
                   acessibilidade=["camiao", "drone"],
                   condicao='normal',  # Estado da rota
                   cor='gray')         # Cor base para as rotas
                   
    grafo.add_edge("zona2", "zona3", 
                   distancia=15, 
                   tempo=2, 
                   acessibilidade=["camiao"],
                   condicao='normal',
                   cor='gray')
                   
    grafo.add_edge("zona1", "zona3", 
                   distancia=20, 
                   tempo=3, 
                   acessibilidade=["helicoptero"],
                   condicao='normal',
                   cor='gray')
    
    return grafo

def mostrar_grafo(grafo, titulo="Grafo de Zonas e Rotas"):
    plt.figure(figsize=(12, 8))
    pos = nx.get_node_attributes(grafo, 'pos')
    
    # Desenhar as arestas (rotas)
    edge_colors = [grafo[u][v]['cor'] for u, v in grafo.edges()]
    nx.draw_networkx_edges(grafo, pos, edge_color=edge_colors, width=2)
    
    # Desenhar os nós (zonas)
    node_colors = [grafo.nodes[node]['cor'] for node in grafo.nodes()]
    nx.draw_networkx_nodes(grafo, pos, node_color=node_colors, 
                          node_size=1000, alpha=0.7)
    
    # Adicionar rótulos aos nós com informações
    labels = {}
    for node in grafo.nodes():
        info = grafo.nodes[node]
        labels[node] = f"{node}\nPop: {info['populacao']}\nNec: {info['necessidades']}"
    nx.draw_networkx_labels(grafo, pos, labels, font_size=8)
    
    # Adicionar rótulos às arestas
    edge_labels = {}
    for u, v, data in grafo.edges(data=True):
        edge_labels[(u, v)] = f"D:{data['distancia']}\nT:{data['tempo']}"
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels, font_size=8)
    
    plt.title(titulo)
    plt.axis('off')
    plt.tight_layout()
    
    return plt.gcf()  # Retorna a figura para possível uso posterior

def atualizar_visualizacao(grafo, estado_atual=None):
    """
    Atualiza as cores do grafo baseado no estado atual
    """
    # Atualizar cores das zonas baseado nas necessidades
    for node in grafo.nodes():
        if estado_atual and node in estado_atual.zonas:
            necessidades = estado_atual.zonas[node]['necessidades_atuais']
            if necessidades == 0:
                grafo.nodes[node]['cor'] = 'lightgreen'  # Atendida
            elif necessidades < grafo.nodes[node]['necessidades'] * 0.5:
                grafo.nodes[node]['cor'] = 'yellow'      # Parcialmente atendida
            else:
                grafo.nodes[node]['cor'] = 'salmon'      # Crítica
    
    # Atualizar cores das rotas baseado nas condições
    for u, v in grafo.edges():
        condicao = grafo[u][v]['condicao']
        if condicao == 'bloqueada':
            grafo[u][v]['cor'] = 'red'
        elif condicao == 'comprometida':
            grafo[u][v]['cor'] = 'yellow'
        else:
            grafo[u][v]['cor'] = 'gray'

def mostrar_rota_veiculo(grafo, rota, veiculo_tipo, titulo=None):
    """
    Mostra uma rota específica de um veículo no grafo
    """
    fig = mostrar_grafo(grafo)
    
    # Destacar a rota do veículo
    if len(rota) > 1:
        path_edges = list(zip(rota[:-1], rota[1:]))
        nx.draw_networkx_edges(grafo, nx.get_node_attributes(grafo, 'pos'),
                             edgelist=path_edges, edge_color='blue', 
                             width=3, alpha=0.7)
    
    if titulo:
        plt.title(titulo)
    else:
        plt.title(f"Rota do {veiculo_tipo}")
    
    return fig

# Função para mostrar estado atual da distribuição
def mostrar_estado_distribuicao(grafo, estado):
    """
    Mostra o estado atual da distribuição com informações detalhadas
    """
    # Atualizar cores baseado no estado atual
    atualizar_visualizacao(grafo, estado)
    
    # Criar uma nova figura
    plt.figure(figsize=(15, 10))
    
    # Subplot para o grafo
    plt.subplot(121)
    mostrar_grafo(grafo, "Estado Atual da Distribuição")
    
    # Subplot para informações textuais
    plt.subplot(122)
    plt.axis('off')
    info_text = "Estado da Distribuição:\n\n"
    
    # Adicionar informações sobre as zonas
    for zona_id, zona in estado.zonas.items():
        info_text += f"Zona: {zona_id}\n"
        info_text += f"  Necessidades: {zona['necessidades_atuais']:.1f}\n"
        info_text += f"  Tempo Crítico: {zona['tempo_critico']}h\n"
        info_text += f"  Gravidade: {zona['gravidade']}/10\n\n"
    
    plt.text(0, 0.5, info_text, fontsize=10, verticalalignment='center')
    
    plt.tight_layout()
    plt.show()