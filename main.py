from busca import encontrar_melhores_rotas, a_star, dijkstra, dfs, bfs, greedy, exibir_grafo
from simulacao import simular_cenario
from veiculos import carregar_veiculos_csv
from grafo import carregar_grafo, mostrar_grafo
from validacao import validar_dados_csv, testar_conectividade_grafo, imprimir_veiculos
from menus import menu_principal

import pandas as pd
import matplotlib
matplotlib.use('TkAgg')  # Altere para 'Qt5Agg' ou outro backend se necessário


# Qual é a origem de onde vamos sair? em que zona estamos?
def carregar_dados():
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
    print("A validar dados...\n")
    erros = validar_dados_csv(zonas_df, caminhos_df, veiculos_df)
    if erros: 
        print("Erros encontrados:\n")
        for erro in erros:
            print(f"- {erro}")
        return 
    print("Dados validados com sucesso!\n")

    grafo = carregar_grafo(caminho_zonas, caminho_caminhos)
    print(f"Grafo carregado: {type(grafo)}, Nós: {grafo.nodes(data=True)}")
    
    veiculos = carregar_veiculos_csv(caminho_veiculos)

    return grafo, veiculos

# Exibir informações
def exibir_informacoes(grafo, veiculos):

   
    # Testar conectividade do grafo
    print("\nA testar a conectividade do grafo...")
    conectividade = testar_conectividade_grafo(grafo)
    print(conectividade)

    """
    # Exibir grafo inicial
    print("\nVisualizar o grafo inicial...")
    mostrar_grafo(grafo)
    """

    # Carregar veículos a partir do CSV
    print("\nVeículos carregados:")
    imprimir_veiculos(veiculos)
    
    # Simular cenários dinâmicos
    print("\nA simular cenários dinâmicos...")
    simular_cenario(grafo)


# Função principal
def main():
    print("A iniciar o sistema de Distribuição de Recursos...\n")

    # Carregar dados
    grafo, veiculos = carregar_dados()
    if grafo is None or veiculos is None:
        print("Erro ao carregar dados! A terminar o programa...")
        return
    
    # Exibir informações no terminal 
    exibir_informacoes(grafo, veiculos)

    # Iniciar o menu principal
    menu_principal(grafo,veiculos)


if __name__ == "__main__":
    main()
