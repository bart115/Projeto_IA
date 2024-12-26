class EstadoDistribuicao:
    def __init__(self, zonas, veiculos, tempo_atual=0):
        """
        Estado inicial/atual do problema de distribuição
        
        Args:
            zonas (dict): Dicionário com informações de cada zona
            veiculos (dict): Dicionário com estado atual dos veículos
            tempo_atual (int): Tempo decorrido desde o início da operação
        """
        self.zonas = zonas
        self.veiculos = veiculos
        self.tempo_atual = tempo_atual
        
    def is_objetivo(self):
        """
        Verifica se o estado atual é um estado objetivo
        Returns:
            bool: True se todas as zonas foram atendidas dentro do tempo crítico
        """
        for zona_id, zona in self.zonas.items():
            # Se alguma zona não recebeu suprimentos suficientes
            if zona['necessidades_atuais'] > 0:
                # E ainda está dentro do tempo crítico
                if self.tempo_atual < zona['tempo_critico']:
                    return False
        return True

def definir_estado_inicial():
    """
    Define o estado inicial do problema
    """
    zonas = {
        'zona1': {
            'populacao': 1000,
            'gravidade': 5,  # Escala 1-10
            'tempo_critico': 48,  # Horas
            'necessidades_atuais': 500,  # Kg de suprimentos necessários
            'pos': (0, 0),
            'acessibilidade': ['drone', 'camiao', 'helicoptero']
        },
        'zona2': {
            'populacao': 500,
            'gravidade': 8,
            'tempo_critico': 24,
            'necessidades_atuais': 300,
            'pos': (1, 1),
            'acessibilidade': ['drone', 'helicoptero']
        },
        'zona3': {
            'populacao': 200,
            'gravidade': 6,
            'tempo_critico': 36,
            'necessidades_atuais': 200,
            'pos': (2, 0),
            'acessibilidade': ['helicoptero']
        }
    }
    
    veiculos = {
        'drone1': {
            'tipo': 'drone',
            'capacidade': 10,
            'velocidade': 50,
            'autonomia': 20,
            'pos_atual': 'zona1',
            'carga_atual': 10,
            'combustivel': 100
        },
        'camiao1': {
            'tipo': 'camiao',
            'capacidade': 2000,
            'velocidade': 60,
            'autonomia': 500,
            'pos_atual': 'zona1',
            'carga_atual': 2000,
            'combustivel': 100
        },
        'helicoptero1': {
            'tipo': 'helicoptero',
            'capacidade': 500,
            'velocidade': 120,
            'autonomia': 100,
            'pos_atual': 'zona1',
            'carga_atual': 500,
            'combustivel': 100
        }
    }
    
    return EstadoDistribuicao(zonas, veiculos)

class Operador:
    """Define os operadores possíveis no problema"""
    
    @staticmethod
    def mover_veiculo(estado, veiculo_id, destino):
        """
        Move um veículo para uma nova zona
        
        Returns:
            tuple: (novo_estado, custo) ou (None, None) se movimento impossível
        """
        novo_estado = EstadoDistribuicao(
            estado.zonas.copy(), 
            estado.veiculos.copy(), 
            estado.tempo_atual
        )
        
        veiculo = novo_estado.veiculos[veiculo_id]
        origem = veiculo['pos_atual']
        
        # Verificar se movimento é possível
        if destino not in estado.zonas:
            return None, None
            
        if veiculo['tipo'] not in estado.zonas[destino]['acessibilidade']:
            return None, None
            
        # Calcular custos
        distancia = calcular_distancia(
            estado.zonas[origem]['pos'], 
            estado.zonas[destino]['pos']
        )
        tempo_gasto = distancia / veiculo['velocidade']
        combustivel_gasto = (distancia / veiculo['autonomia']) * 100
        
        # Verificar recursos
        if veiculo['combustivel'] < combustivel_gasto:
            return None, None
            
        # Atualizar estado
        veiculo['pos_atual'] = destino
        veiculo['combustivel'] -= combustivel_gasto
        novo_estado.tempo_atual += tempo_gasto
        
        return novo_estado, tempo_gasto
    
    @staticmethod
    def entregar_suprimentos(estado, veiculo_id, quantidade):
        """
        Entrega suprimentos na zona atual do veículo
        
        Returns:
            tuple: (novo_estado, custo) ou (None, None) se entrega impossível
        """
        novo_estado = EstadoDistribuicao(
            estado.zonas.copy(), 
            estado.veiculos.copy(), 
            estado.tempo_atual
        )
        
        veiculo = novo_estado.veiculos[veiculo_id]
        zona_atual = veiculo['pos_atual']
        
        # Verificar se entrega é possível
        if quantidade > veiculo['carga_atual']:
            return None, None
            
        if quantidade > estado.zonas[zona_atual]['necessidades_atuais']:
            quantidade = estado.zonas[zona_atual]['necessidades_atuais']
        
        # Realizar entrega
        veiculo['carga_atual'] -= quantidade
        novo_estado.zonas[zona_atual]['necessidades_atuais'] -= quantidade
        
        # Tempo fixo para operação de entrega
        tempo_entrega = 0.5  # 30 minutos
        novo_estado.tempo_atual += tempo_entrega
        
        return novo_estado, tempo_entrega

def calcular_distancia(pos1, pos2):
    """Calcula distância euclidiana entre duas posições"""
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
