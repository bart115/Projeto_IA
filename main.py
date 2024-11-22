from grafo import criar_grafo, mostrar_grafo
from veiculos import inicializar_veiculos
from busca import encontrar_melhores_rotas
from simulacao import simular_cenario

def main():
    print("Iniciando Sistema de Distribuição de Recursos...\n")
    
    # Criar grafo de zonas afetadas e rotas
    grafo = criar_grafo()
    
    # Exibir grafo inicial
    print("Visualizando o grafo inicial...")
    mostrar_grafo(grafo)
    
    # Inicializar os veículos disponíveis
    veiculos = inicializar_veiculos()
    
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
