import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 700, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 - Start Screen")


BG_COLOR = (187, 173, 160)
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 72)

def draw_start_screen():
    SCREEN.fill(BG_COLOR)
    
 
    title = FONT.render("2048", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3)
    SCREEN.blit(title, title_rect)
    
    pygame.display.flip()

def main():
    running = True
    while running:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    print("Start Game!") 
                    running = False 
        
        pygame.time.Clock().tick(60)

if __name__ == "__main__": 
   main() 


import pygame
import sys

pygame.init() 

screen = pygame.display.set_mode((600, 600))  
pygame.display.set_caption("2048 Start Menu")  


PURPLE = (90, 0, 140)     
WHITE = (255, 255, 255)  
PLAYER1 = (120, 80, 200)  
PLAYER2 = (200, 80, 80)   
ORANGE = (240, 100, 40)   

font_title = pygame.font.Font(None, 100) 
font_btn = pygame.font.Font(None, 40)    

player1_rect = pygame.Rect(0, 0, 220, 60)
player1_rect.center = (300, 350)  #ปุ่ม Player One

player2_rect = pygame.Rect(0, 0, 220, 60)
player2_rect.center = (300, 420)  #ปุ่ม Player Two

how_rect = pygame.Rect(0, 0, 250, 60)
how_rect.center = (300, 500)      #ปุ่ม How to Play
def draw_menu():
    screen.fill(PURPLE)

    title = font_title.render("2048", True, WHITE)
    screen.blit(title, (230, 150))

    pygame.draw.rect(screen, PLAYER1, player1_rect, border_radius=10)
    text1 = font_btn.render("Player One", True, WHITE)
    screen.blit(text1, (player1_rect.x + 40, player1_rect.y + 15))

    pygame.draw.rect(screen, PLAYER2, player2_rect, border_radius=10)
    text2 = font_btn.render("Player Two", True, WHITE)
    screen.blit(text2, (player2_rect.x + 40, player2_rect.y + 15))

    pygame.draw.rect(screen, ORANGE, how_rect, border_radius=10)
    text3 = font_btn.render("How to Play", True, WHITE)
    screen.blit(text3, (how_rect.x + 40, how_rect.y + 15))

    pygame.display.flip() 


running = True
while running:
    draw_menu() 

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN: 
            if player1_rect.collidepoint(event.pos): 
                print("Player One")
            elif player2_rect.collidepoint(event.pos):  
                print("Player Two")
            elif how_rect.collidepoint(event.pos):  
                print("How to play")

    pygame.time.Clock().tick(60)  


