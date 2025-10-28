import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 700, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


BG_COLOR = (187, 173, 160)
PURPLE   = (90, 0, 140)
WHITE    = (255, 255, 255)
PLAYER1  = (120, 80, 200)
PLAYER2  = (200, 80, 80)
ORANGE   = (240, 100, 40)


FONT_TITLE = pygame.font.Font(None, 100)
FONT_MAIN  = pygame.font.Font(None, 72)
FONT_BTN   = pygame.font.Font(None, 40)


player1_rect = pygame.Rect(0, 0, 220, 60); player1_rect.center = (WIDTH // 2, 350)
player2_rect = pygame.Rect(0, 0, 220, 60); player2_rect.center = (WIDTH // 2, 420)
how_rect     = pygame.Rect(0, 0, 250, 60); how_rect.center     = (WIDTH // 2, 500)

def draw_start_screen():
    SCREEN.fill(BG_COLOR)
    title = FONT_MAIN.render("2048", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3)) 
    SCREEN.blit(title, title_rect)

    hint = pygame.font.Font(None, 36).render("Press Enter to Start", True, WHITE)
    hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 80))
    SCREEN.blit(hint, hint_rect)

    pygame.display.flip()

def draw_menu():
    SCREEN.fill(PURPLE)

    title = FONT_TITLE.render("2048", True, WHITE)
    SCREEN.blit(title, (WIDTH // 2 - 80, 150))

    pygame.draw.rect(SCREEN, PLAYER1, player1_rect)
    SCREEN.blit(FONT_BTN.render("Player One", True, WHITE), (player1_rect.x + 40, player1_rect.y + 15))

    pygame.draw.rect(SCREEN, PLAYER2, player2_rect)
    SCREEN.blit(FONT_BTN.render("Player Two", True, WHITE), (player2_rect.x + 40, player2_rect.y + 15))

    pygame.draw.rect(SCREEN, ORANGE, how_rect)
    SCREEN.blit(FONT_BTN.render("How to Play", True, WHITE), (how_rect.x + 35, how_rect.y + 15))

    pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    state = "START"   # START -> MENU

    running = True
    while running:
        if state == "START":
            draw_start_screen()
        else:
            draw_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "START":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    print("Start Game!")
                    state = "MENU"
            else:  # MENU
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player1_rect.collidepoint(event.pos):
                        print("Player One")
                    elif player2_rect.collidepoint(event.pos):
                        print("Player Two")
                    elif how_rect.collidepoint(event.pos):
                        print("How to Play")

        clock.tick(60)

if __name__ == "__main__":
    main()

