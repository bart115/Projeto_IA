import networkx as nx
import subprocess
import pickle
import matplotlib.pyplot as plt
import threading
import csv

from busca import exibir_grafo

def carregar_grafo(zonas_csv, caminhos_csv):
    grafo = nx.Graph()
    
    with open(zonas_csv, mode='r', encoding='utf-8') as file:
        leitor_csv = csv.DictReader(file)
        for linha in leitor_csv:
            grafo.add_node(
                linha["nome"],
                populacao=int(linha["populacao"]),
                gravidade=int(linha["gravidade"]),
                tempo_critico=int(linha["tempo_critico"]),
                pos=(float(linha["pos_x"]), float(linha["pos_y"]))
            )

    with open(caminhos_csv, mode='r', encoding='utf-8') as file:
        leitor_csv = csv.DictReader(file)
        for linha in leitor_csv:
            # Converter acessibilidade para uma lista baseada no nível
            nivel_acess = int(float(linha["acessibilidade"]))
            tipos_permitidos = []
            if 8 <= nivel_acess <= 10: tipos_permitidos.extend(['drone', 'helicoptero', 'camiao', 'barco', 'mota'])
            elif 6 <= nivel_acess <= 7: tipos_permitidos.extend(['drone', 'helicoptero', 'camiao', 'mota'])
            elif 3 <= nivel_acess <= 5: tipos_permitidos.extend(['drone', 'helicoptero'])
            else: tipos_permitidos.append('drone')
            
            grafo.add_edge(
                linha["zona1"],
                linha["zona2"],
                distancia=float(linha["distancia"]),
                tempo=float(linha["tempo"]),
                acessibilidade=tipos_permitidos
            )
    
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
    plt.show(block=True)



