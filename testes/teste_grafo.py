import unittest
from grafo import criar_grafo

class TestGrafo(unittest.TestCase):
    def test_criacao_grafo(self):
        grafo = criar_grafo()
        self.assertEqual(len(grafo.nodes), 3)
        self.assertEqual(len(grafo.edges), 3)

if __name__ == "__main__":
    unittest.main()
