import random
from formulacao import EstadoDistribuicao

def simular_cenario(grafo, estado=None):
    """
    Simula alterações dinâmicas no ambiente
    """
    # Simular alterações climáticas
    simular_clima(grafo)
    
    # Simular mudanças nas necessidades das zonas
    if estado:
        simular_mudancas_necessidades(estado)
    
    # Simular bloqueios de rotas
    simular_bloqueios(grafo)

def simular_clima(grafo):
    """
    Simula mudanças nas condições climáticas
    """
    condicoes = ['bom', 'chuva', 'tempestade']
    
    for u, v, dados in grafo.edges(data=True):
        clima = random.choice(condicoes)
        
        if clima == 'chuva':
            print(f"Chuva entre {u} e {v}. Tempo de viagem aumentado em 50%")
            dados['tempo'] *= 1.5
        elif clima == 'tempestade':
            print(f"Tempestade entre {u} e {v}. Tempo de viagem dobrado!")
            dados['tempo'] *= 2
            # Drones não podem voar em tempestades
            if 'drone' in dados['acessibilidade']:
                dados['acessibilidade'].remove('drone')

def simular_mudancas_necessidades(estado):
    """
    Simula mudanças nas necessidades das zonas
    """
    for zona_id, zona in estado.zonas.items():
        # 20% de chance de aumentar necessidades
        if random.random() < 0.2:
            aumento = random.uniform(0.1, 0.3)  # 10-30% de aumento
            zona['necessidades_atuais'] *= (1 + aumento)
            print(f"Necessidades aumentaram em {zona_id}: +{aumento*100:.1f}%")

def simular_bloqueios(grafo):
    """
    Simula bloqueios em rotas
    """
    for u, v in list(grafo.edges()):
        if random.random() < 0.1:  # 10% de chance de bloqueio
            tipo_bloqueio = random.choice(['deslizamento', 'inundação', 'destruição'])
            print(f"Rota entre {u} e {v} bloqueada por {tipo_bloqueio}!")
            
            if tipo_bloqueio == 'deslizamento':
                # Apenas helicópteros podem passar
                grafo[u][v]['acessibilidade'] = ['helicoptero']
            elif tipo_bloqueio == 'inundação':
                # Apenas helicópteros e barcos podem passar
                grafo[u][v]['acessibilidade'] = ['helicoptero', 'barco']
            else:  # destruição
                grafo.remove_edge(u, v)