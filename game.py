import pygame, sys, random

pygame.init()

#หน้าจอ
WIDTH, HEIGHT = 1500, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 Start Menu")

#สี
PURPLE = (90, 0, 140)
WHITE = (255, 255, 255)
PLAYER1 = (120, 80, 200)
PLAYER2 = (200, 80, 80)
ORANGE = (240, 100, 40)
BG_COLOR = (187, 173, 160)
TILE_COLOR = (205, 193, 180)
TEXT_COLOR = (50, 50, 50)

#ฟอนต์
font_title = pygame.font.Font(None, 120)
font_btn = pygame.font.Font(None, 50)
font_num = pygame.font.Font(None, 60)

clock = pygame.time.Clock()

#ปุ่มเมนู
player1_rect = pygame.Rect(0, 0, 260, 70)
player2_rect = pygame.Rect(0, 0, 260, 70)
how_rect = pygame.Rect(0, 0, 260, 70)

#จัดตำแหน่งให้อยู่กลางแนว X และเรียงในแนวตั้ง
center_x = WIDTH // 2
start_y = HEIGHT // 2 - 50
space = 90  # ระยะห่างระหว่างปุ่ม

player1_rect.center = (center_x, start_y)
player2_rect.center = (center_x, start_y + space)
how_rect.center = (center_x, start_y + space * 2)

#ตารางเกม (4x4)
grid = [[0 for _ in range(4)] for _ in range(4)]


def add_random_tile():
    """เพิ่มเลข 2 หรือ 4 ลงในช่องว่างแบบสุ่ม"""
    empty = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        grid[r][c] = random.choice([2, 2, 4])  # โอกาสออก 2 มากกว่า 4


def reset_game():
    """รีเซ็ตตารางใหม่"""
    global grid
    grid = [[0 for _ in range(4)] for _ in range(4)]
    add_random_tile()
    add_random_tile()


def draw_menu():
    """หน้าจอเมนูเริ่มต้น"""
    screen.fill(PURPLE)

    # ชื่อเกม
    title = font_title.render("2048", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    screen.blit(title, title_rect)

    # ปุ่ม Player 1
    pygame.draw.rect(screen, PLAYER1, player1_rect, border_radius=10)
    text1 = font_btn.render("Player One", True, WHITE)
    screen.blit(text1, text1.get_rect(center=player1_rect.center))

    # ปุ่ม Player 2
    pygame.draw.rect(screen, PLAYER2, player2_rect, border_radius=10)
    text2 = font_btn.render("Player Two", True, WHITE)
    screen.blit(text2, text2.get_rect(center=player2_rect.center))

    # ปุ่ม How to Play
    pygame.draw.rect(screen, ORANGE, how_rect, border_radius=10)
    text3 = font_btn.render("How to Play", True, WHITE)
    screen.blit(text3, text3.get_rect(center=how_rect.center))

    pygame.display.flip()


def draw_game(): #วาดตารางเกมให้อยู่กลางจอ
    screen.fill(BG_COLOR)

    size = 120   # ขนาดช่อง
    gap = 15     # ช่องว่างระหว่างช่อง
    grid_size = 4

    # คำนวณตำแหน่งเริ่มต้นให้อยู่กลาง
    total_width = grid_size * size + (grid_size - 1) * gap
    total_height = grid_size * size + (grid_size - 1) * gap
    start_x = (WIDTH - total_width) // 2
    start_y = (HEIGHT - total_height) // 2 - 50

    # วาดช่อง
    for r in range(grid_size):
        for c in range(grid_size):
            x = start_x + c * (size + gap)
            y = start_y + r * (size + gap)
            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(screen, TILE_COLOR, rect, border_radius=8)

            value = grid[r][c]
            if value != 0:
                text = font_num.render(str(value), True, TEXT_COLOR)
                screen.blit(text, text.get_rect(center=rect.center))

    # ปุ่มกลับเมนู
    back_text = font_btn.render("Press ESC to Menu", True, (80, 80, 80))
    screen.blit(back_text, back_text.get_rect(center=(WIDTH // 2, HEIGHT - 100)))

    pygame.display.flip()


# ลูปเกม
def main():
    game_state = "menu"  # เริ่มต้นที่หน้าเมนู

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player1_rect.collidepoint(event.pos):
                        reset_game()
                        game_state = "play"
                    elif player2_rect.collidepoint(event.pos):
                        print("Player Two (ยังไม่ทำ)")
                    elif how_rect.collidepoint(event.pos):
                        print("How to Play: ใช้ปุ่มลูกศรเลื่อนตัวเลข")

            elif game_state == "play":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game_state = "menu"

        # วาดหน้าจอตามสถานะ
        if game_state == "menu":
            draw_menu()
        elif game_state == "play":
            draw_game()

        clock.tick(60)


if __name__ == "__main__":
    main()
