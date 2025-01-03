import unittest
from grafo import mostrar_grafo
from busca import a_star, dijkstra



def test_visualizar_grafo(self):
    """Mostra o grafo criado."""
    mostrar_grafo(self.grafo)

class TestGrafo(unittest.TestCase):
    def setUp(self):
        """Configuração inicial para os testes."""
        self.grafo = criar_grafo()
        self.veiculo = {
            "tipo": "drone",
            "capacidade": 10,
            "velocidade": 50,
            "autonomia": 20
        }

    def test_criacao_grafo(self):
        """Testa se o grafo é criado corretamente."""
        self.assertEqual(len(self.grafo.nodes), 3)
        self.assertEqual(len(self.grafo.edges), 3)

    def test_atributos_nos(self):
        """Verifica atributos dos nós."""
        zona1 = self.grafo.nodes["zona1"]
        self.assertEqual(zona1["populacao"], 1000)
        self.assertEqual(zona1["gravidade"], 5)
        self.assertEqual(zona1["tempo_critico"], 48)

    def test_atributos_arestas(self):
        """Verifica atributos das arestas."""
        aresta = self.grafo["zona1"]["zona2"]
        self.assertEqual(aresta["distancia"], 10)
        self.assertIn("camiao", aresta["acessibilidade"])

    def test_a_star(self):
        """Testa o algoritmo A* para encontrar rotas."""
        rota = a_star(self.grafo, "zona1", "zona3", self.veiculo)
        self.assertIsNotNone(rota)
        self.assertEqual(rota, ["zona1", "zona3"])  # Verifique o caminho esperado

    def test_dijkstra(self):
        """Testa o algoritmo Dijkstra para encontrar rotas."""
        rota = dijkstra(self.grafo, "zona1", "zona3", self.veiculo)
        self.assertIsNotNone(rota)
        self.assertEqual(rota, ["zona1", "zona3"])  # Verifique o caminho esperado

if __name__ == "__main__":
    unittest.main()
