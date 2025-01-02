import sys
import pickle
import networkx as nx
import matplotlib.pyplot as plt

def mostrar_rota(grafo, rota, tipo_veiculo):
    pos = nx.get_node_attributes(grafo, 'pos')
    plt.figure(figsize=(8, 6))
    nx.draw(grafo, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=10, font_weight='bold')

    if rota:
        rota_arestas = [(rota[i], rota[i + 1]) for i in range(len(rota) - 1)]
        nx.draw_networkx_edges(grafo, pos, edgelist=rota_arestas, edge_color='red', width=2.5)
        plt.title(f"Rota Calculada para o Veículo: {tipo_veiculo}")
    else:
        plt.title("Grafo Geral")

    plt.gcf().canvas.manager.set_window_title("Exibição do Grafo")
    plt.show()

if __name__ == "__main__":
    # Recebe os dados serializados como entrada
    data = pickle.load(sys.stdin.buffer)
    mostrar_rota(*data)
