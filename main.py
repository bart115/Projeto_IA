from busca import encontrar_melhores_rotas, a_star, dijkstra, dfs, bfs, greedy, mostrar_rota
from simulacao import simular_cenario
from veiculos import carregar_veiculos_csv
from grafo import carregar_grafo, mostrar_grafo
from validacao import validar_dados_csv, testar_conectividade_grafo, imprimir_veiculos

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Altere para 'Qt5Agg' ou outro backend se necessário

# Qual é a origem de onde vamos sair? em que zona estamos?
def main():
    print("Iniciando Sistema de Distribuição de Recursos...\n")
    
    
    # Caminhos dos ficheiros CSV
    caminho_zonas = "zonas.csv"
    caminho_caminhos = "caminhos.csv"
    caminho_veiculos = "veiculos.csv" # Não é usado diretamente, mas é necessário para a validação

    # Carregar DataFrames
    zonas_df = pd.read_csv(caminho_zonas)
    caminhos_df = pd.read_csv(caminho_caminhos)
    veiculos_df = pd.read_csv(caminho_veiculos)

     # Validar dados
    print("A validar dados...")
    erros = validar_dados_csv(zonas_df, caminhos_df, veiculos_df)
    if erros: 
        print("Erros encontrados:")
        for erro in erros:
            print(f"- {erro}")
        return 
    print("Dados validados com sucesso!")


     # Carregar grafo
    grafo = carregar_grafo(caminho_zonas, caminho_caminhos)
    print("Grafo carregado com sucesso!")

    # Testar conectividade do grafo
    conectividade = testar_conectividade_grafo(grafo)
    print(conectividade)

    # Exibir grafo inicial
    print("Visualizando o grafo inicial...")
    mostrar_grafo(grafo)
    
    # Carregar veículos a partir do CSV
    veiculos = carregar_veiculos_csv("veiculos.csv")
    print("Veículos carregados:")
    imprimir_veiculos(veiculos)
    
    # Simular cenários dinâmicos
    print("Simulando cenários dinâmicos...")
    simular_cenario(grafo)

 
    # Escolher origem, destino
    #print("\nDefina os pontos de partida e destino:")
    #origem = input("Digite a zona de origem (ex: zona1): ")
    #destino = input("Digite a zona de destino (ex: zona2): ")

     # Menu de seleção
    print("\nEscolha o algoritmo:")
    print("1. A*")
    print("2. Dijkstra")
    print("3. DFS (Busca em Profundidade)")
    print("4. BFS (Busca em Largura)")
    print("5. Greedy")

    escolha = input("Digite o número do algoritmo: ")
    
     # Executar algoritmo escolhido
    algoritmos = {
        "1": ("A*", a_star),
        "2": ("Dijkstra", dijkstra),
        "3": ("DFS", dfs),
        "4": ("BFS", bfs),
        "5": ("Greedy", greedy)
    }
     
    # Executar algoritmo escolhido para todos os veículos
    if escolha in algoritmos:
        nome, func = algoritmos[escolha]
    else:
        print("Escolha inválida!")
        return
   
    # Encontrar melhores rotas
    print("\nCalculando rotas de distribuição...")
    resultados = encontrar_melhores_rotas(grafo, veiculos, func)
    
    # Exibir resultados
    print("\nResultados da Simulação:")
    for resultado in resultados:
        print(resultado)

if __name__ == "__main__":
    main()
