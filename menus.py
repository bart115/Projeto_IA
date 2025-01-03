import pygame, sys
import threading
from busca import encontrar_melhores_rotas, exibir_grafo, a_star, dijkstra, dfs, bfs, greedy
from grafo import mostrar_grafo

# Inicia pygame
pygame.init()

def pausar_pygame():
    pygame.display.iconify()  # Minimiza a janela do Pygame
    pygame.event.clear()      # Limpa eventos pendentes


# Define as dimensões da janela
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu Principal")

# Definir as cores
White = (255, 255, 255)
Gray = (50, 50, 50)
Blue = (0, 0, 255)
Red = (255, 0, 0)

# Fonte para os botões 
font = pygame.font.Font(None, 36)

# Função para criar botões
def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

global veiculo_selecionado
veiculo_selecionado = None

# Menu principal
def menu_principal(grafo, veiculos): 
    global veiculo_selecionado
    running = True
    while running:
        screen.fill(Gray)
        draw_button("Exibir Grafo", 400, 200, 250, 50, Blue, White)
        draw_button("Selecionar Veículo", 400, 300, 250, 50, Blue, White)
        draw_button("Algoritmos", 400, 400, 250, 50, Blue, White)
        draw_button("Sair", 400, 500, 250, 50, Red, White)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
               mouse_x, mouse_y = event.pos
               # Verifica se o botão "Exibir Grafo" foi clicado
               if 400 <= mouse_x <= 600 and 200 <= mouse_y <= 250:
                     exibir_grafo(grafo) 

               # Verifica se o botão "Selecionar Veículo" foi clicado
               if 400 <= mouse_x <= 600 and 300 <= mouse_y <= 350:
                    menu_veiculos(grafo, veiculos) 
                   
               # Verifica se o botão "Algoritmos" foi clicado
               if 400 <= mouse_x <= 600 and 400 <= mouse_y <= 450:
                   menu_algoritmos(grafo, veiculos)
                
               # Verifica se o botão "Sair" foi clicado
               elif 400 <= mouse_x <= 600 and 500 <= mouse_y <= 550:
                   pygame.quit()
                   sys.exit()

        # Atualiza o ecra
        pygame.display.update() 

# Menu de escolha de veículo
def menu_veiculos(grafo, veiculos):
    global veiculo_selecionado
    running = True
    while running:
        screen.fill(Gray)
        draw_button("Drone", 400, 100, 250, 50, Blue, White)
        draw_button("Camião", 400, 200, 250, 50, Blue, White)
        draw_button("Helicoptero", 400, 300, 250, 50, Blue, White)  
        draw_button("Barco", 400, 400, 250, 50, Blue, White)
        draw_button("Mota", 400, 500, 250, 50, Blue, White)
        draw_button("Voltar", 400, 600, 250, 50, Red, White)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 400 <= mouse_x <= 600 and 100 <= mouse_y <= 150:
                    veiculo_selecionado = next(v for v in veiculos if v["tipo"] == "drone") # Seleciona o dicionario do veículo Drone e não apenas o tipo "Drone"
                    print(f"Veículo selecionado: {veiculo_selecionado}")
                    running = False
                elif 400 <= mouse_x <= 600 and 200 <= mouse_y <= 250:
                    veiculo_selecionado = next(v for v in veiculos if v["tipo"] == "camiao")
                    print(f"Veículo selecionado: {veiculo_selecionado}")
                    running = False
                elif 400 <= mouse_x <= 600 and 300 <= mouse_y <= 350:
                    veiculo_selecionado = next(v for v in veiculos if v["tipo"] == "helicoptero")
                    print(f"Veículo selecionado: {veiculo_selecionado}")
                    running = False
                elif 400 <= mouse_x <= 600 and 400 <= mouse_y <= 450:
                    veiculo_selecionado = next(v for v in veiculos if v["tipo"] == "barco")
                    print(f"Veículo selecionado: {veiculo_selecionado}")
                    running = False
                elif 400 <= mouse_x <= 600 and 500 <= mouse_y <= 550:
                    veiculo_selecionado = next(v for v in veiculos if v["tipo"] == "mota")
                    print(f"Veículo selecionado: {veiculo_selecionado}")
                    running = False
                elif 400 <= mouse_x <= 600 and 600 <= mouse_y <= 650:
                    menu_principal(grafo, veiculos)

        # Atualiza o ecra
        pygame.display.update()

# Menu de algoritmos
def menu_algoritmos(grafo, veiculos):
    global veiculo_selecionado
    running = True

     # Verificar se o veículo foi selecionado
    if veiculo_selecionado is None:
        # Mensagem visual
        while running:
            screen.fill(White)
            font = pygame.font.Font(None, 36)
            mensagem = font.render("Erro: Selecione um veículo no menu principal!", True, (255, 0, 0))
            screen.blit(mensagem, (200, 300))
            botao_voltar = pygame.Rect(400, 400, 250, 50)
            pygame.draw.rect(screen, (0, 0, 255), botao_voltar)
            texto_voltar = font.render("Voltar", True, (255, 255, 255))
            screen.blit(texto_voltar, (botao_voltar.x + 75, botao_voltar.y + 10))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    if botao_voltar.collidepoint(mouse_x, mouse_y):
                        return  # Retorna ao menu principal

            pygame.display.update()

    while running:
        screen.fill(White)
        draw_button("A*", 400, 100, 250, 50, Blue, White)   
        draw_button("Dijkstra", 400, 200, 250, 50, Blue, White)
        draw_button("DFS", 400, 300, 250, 50, Blue, White)
        draw_button("BFS", 400, 400, 250, 50, Blue, White)
        draw_button("Greedy", 400, 500, 250, 50, Blue, White)
        draw_button("Voltar", 400, 600, 250, 50, Red, White)  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if 400 <= mouse_x <= 600 and 100 <= mouse_y <= 150:
                   #print(f"Tipo de grafo: {type(grafo)}")  # Verifica o tipo de grafo 
                    rota = encontrar_melhores_rotas(grafo, [veiculo_selecionado], a_star)[0]
                    exibir_grafo(grafo, rota=rota["rota"], tipo_veiculo=veiculo_selecionado["tipo"])
                
                elif 400 <= mouse_x <= 600 and 200 <= mouse_y <= 250:
                    rota = encontrar_melhores_rotas(grafo, [veiculo_selecionado], a_star)[0]
                    exibir_grafo(grafo, rota=rota["rota"], tipo_veiculo=veiculo_selecionado["tipo"])
                
                elif 400 <= mouse_x <= 600 and 300 <= mouse_y <= 350:  
                    rota = encontrar_melhores_rotas(grafo, [veiculo_selecionado], a_star)[0]
                    exibir_grafo(grafo, rota=rota["rota"], tipo_veiculo=veiculo_selecionado["tipo"])
                
                elif 400 <= mouse_x <= 600 and 400 <= mouse_y <= 450:
                    rota = encontrar_melhores_rotas(grafo, [veiculo_selecionado], a_star)[0]
                    exibir_grafo(grafo, rota=rota["rota"], tipo_veiculo=veiculo_selecionado["tipo"])
                
                elif 400 <= mouse_x <= 600 and 500 <= mouse_y <= 550:
                    rota = encontrar_melhores_rotas(grafo, [veiculo_selecionado], a_star)[0]
                    exibir_grafo(grafo, rota=rota["rota"], tipo_veiculo=veiculo_selecionado["tipo"])
                
                elif 400 <= mouse_x <= 600 and 600 <= mouse_y <= 650:
                    menu_principal(grafo, veiculos)

        # Atualiza o ecra
        pygame.display.update()

        
