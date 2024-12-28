import pandas as pd  # Para manipulação de DataFrames
from networkx import is_connected  # Para testar conectividade de grafos

def validar_dados_csv(zonas_df, caminhos_df, veiculos_df):
    erros = []
    
    # Validar zonas
    if "nome" not in zonas_df.columns or "populacao" not in zonas_df.columns:
        erros.append("Faltando colunas obrigatórias em zonas.csv.")
    
    if zonas_df["populacao"].min() < 0:
        erros.append("População inválida em zonas.csv.")
    
    # Validar caminhos
    if "zona1" not in caminhos_df.columns or "zona2" not in caminhos_df.columns:
        erros.append("Faltando colunas obrigatórias em caminhos.csv.")
    
    zonas_existentes = set(zonas_df["nome"])
    for _, row in caminhos_df.iterrows():
        if row["zona1"] not in zonas_existentes or row["zona2"] not in zonas_existentes:
            erros.append(f"Zona inexistente no caminho: {row['zona1']} -> {row['zona2']}")
    
    # Validar veículos
    if "tipo" not in veiculos_df.columns or "capacidade" not in veiculos_df.columns:
        erros.append("Faltando colunas obrigatórias em veiculos.csv.")
    
    if veiculos_df["capacidade"].min() < 0:
        erros.append("Capacidade inválida em veiculos.csv.")
    
    return erros

def testar_conectividade_grafo(grafo):
    """
    Verifica se o grafo está conectado.
    """
    if not is_connected(grafo):
        return "O grafo não está conectado. Algumas zonas podem estar isoladas."
    return "O grafo está conectado. Todas as zonas são acessíveis."

def imprimir_veiculos(veiculos):
    """
    Exibe a lista de veículos carregados.
    """
    for veiculo in veiculos:
        print(f"Tipo: {veiculo['tipo']}, Capacidade: {veiculo['capacidade']}, "
              f"Velocidade: {veiculo['velocidade']}, Autonomia: {veiculo['autonomia']}")
