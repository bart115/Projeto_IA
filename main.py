from grafo import criar_grafo, mostrar_grafo
from veiculos import inicializar_veiculos
from busca import encontrar_melhores_rotas
from simulacao import simular_cenario
from formulacao import definir_estado_inicial, EstadoDistribuicao, Operador

def executar_distribuicao(estado, grafo):
    """
    Executa o processo de distribuição de recursos
    """
    resultados = []
    tempo_total = 0
    
    # Para cada veículo, encontrar e executar melhor rota
    for veiculo_id, veiculo in estado.veiculos.items():
        print(f"\nPlanejando rota para {veiculo_id}...")
        
        # Encontrar zonas que precisam de suprimentos e são acessíveis ao veículo
        zonas_alvo = [
            zona_id for zona_id, zona in estado.zonas.items()
            if zona['necessidades_atuais'] > 0 
            and veiculo['tipo'] in zona['acessibilidade']
        ]
        
        if not zonas_alvo:
            print(f"Não há zonas acessíveis para {veiculo_id}")
            continue
            
        # Encontrar melhor rota para este veículo
        for zona_destino in zonas_alvo:
            rota = encontrar_melhores_rotas(grafo, [veiculo], zona_destino)
            
            if not rota:
                print(f"Não foi possível encontrar rota para {zona_destino}")
                continue
                
            # Executar movimentos
            for proxima_zona in rota[0]['rota']:
                novo_estado, tempo = Operador.mover_veiculo(
                    estado, 
                    veiculo_id, 
                    proxima_zona
                )
                
                if novo_estado is None:
                    print(f"Movimento impossível para {proxima_zona}")
                    break
                    
                estado = novo_estado
                tempo_total += tempo
                
                # Tentar entregar suprimentos
                if estado.zonas[proxima_zona]['necessidades_atuais'] > 0:
                    quantidade = min(
                        veiculo['carga_atual'],
                        estado.zonas[proxima_zona]['necessidades_atuais']
                    )
                    
                    novo_estado, tempo = Operador.entregar_suprimentos(
                        estado,
                        veiculo_id,
                        quantidade
                    )
                    
                    if novo_estado:
                        estado = novo_estado
                        tempo_total += tempo
                        print(f"Entregue {quantidade} unidades em {proxima_zona}")
                    mostrar_estado_distribuicao(grafo, estado)
        
        resultados.append({
            'veiculo': veiculo_id,
            'zonas_atendidas': zonas_alvo
        })
    
    return resultados, tempo_total

def main():
    print("Iniciando Sistema de Distribuição de Recursos...\n")
    
    # Inicializar estado e grafo
    estado_inicial = definir_estado_inicial()
    grafo = criar_grafo()
    
    # Exibir estado inicial
    print("Estado Inicial:")
    for zona_id, zona in estado_inicial.zonas.items():
        print(f"{zona_id}: {zona['necessidades_atuais']} unidades necessárias")
    print("\nVisualizando o grafo inicial...")
    mostrar_grafo(grafo)
    
    # Simular cenários dinâmicos
    print("\nSimulando cenários dinâmicos...")
    simular_cenario(grafo)
    
    # Executar distribuição
    print("\nIniciando processo de distribuição...")
    resultados, tempo_total = executar_distribuicao(estado_inicial, grafo)
    
    # Exibir resultados
    print("\nResultados da Distribuição:")
    print(f"Tempo total da operação: {tempo_total:.2f} horas")
    for resultado in resultados:
        print(f"\nVeículo: {resultado['veiculo']}")
        print(f"Zonas atendidas: {resultado['zonas_atendidas']}")
    
    # Verificar estado final
    print("\nEstado Final das Zonas:")
    for zona_id, zona in estado_inicial.zonas.items():
        print(f"{zona_id}: {zona['necessidades_atuais']} unidades ainda necessárias")

if __name__ == "__main__":
    main()