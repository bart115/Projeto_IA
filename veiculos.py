import csv

def carregar_veiculos_csv(caminho_csv):
    """
    Lê o ficheiro CSV contendo informações sobre os veículos e retorna uma lista de dicionários.
    
    :param caminho_csv: Caminho para o ficheiro CSV.
    :return: Lista de veículos representados como dicionários.
    """
    veiculos = []
    
    with open(caminho_csv, mode='r', encoding='utf-8') as file:
        leitor_csv = csv.DictReader(file)
        
        for linha in leitor_csv:
            veiculo = {
                "tipo": linha["tipo"],
                "capacidade": int(linha["capacidade"]),
                "velocidade": int(linha["velocidade"]),
                "autonomia": int(linha["autonomia"]),
                "acessibilidade": linha["acessibilidade"].split(";")  # Converter acessibilidade para uma lista
            }
            veiculos.append(veiculo)
    
    return veiculos