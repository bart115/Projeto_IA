from busca import encontrar_melhores_rotas
from simulacao import simular_cenario
from veiculos import carregar_veiculos_csv
from grafo import carregar_grafo, mostrar_grafo

import matplotlib
matplotlib.use('TkAgg')  # Altere para 'Qt5Agg' ou outro backend se necessário

# Qual é a origem de onde vamos sair? em que zona estamos?
def main():
    print("Iniciando Sistema de Distribuição de Recursos...\n")
    
    
    # Caminhos dos ficheiros CSV
    caminho_zonas = "zonas.csv"

    caminho_caminhos = "caminhos.csv"
    
     # Carregar grafo
    grafo = carregar_grafo(caminho_zonas, caminho_caminhos)
    print("Grafo carregado com sucesso!")



    # Exibir grafo inicial
    print("Visualizando o grafo inicial...")
    mostrar_grafo(grafo)
    
    # Carregar veículos a partir do CSV
    veiculos = carregar_veiculos_csv("veiculos.csv")
    print("Veículos carregados:")
    for veiculo in veiculos:
        print(veiculo)
    
    # Simular cenários dinâmicos
    print("Simulando cenários dinâmicos...")
    simular_cenario(grafo)
    
    # Encontrar melhores rotas
    print("\nCalculando rotas de distribuição...")
    resultados = encontrar_melhores_rotas(grafo, veiculos)
    
    # Exibir resultados
    print("\nResultados da Simulação:")
    for resultado in resultados:
        print(resultado)

if __name__ == "__main__":
    main()
