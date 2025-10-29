import pygame, sys, random
pygame.init()

# --- หน้าจอ ---
WIDTH, HEIGHT = 1440, 1024
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# --- โหลดภาพพื้นหลัง ---
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # ปรับให้พอดีหน้าจอ

# --- สี ---
PURPLE = (90, 0, 140)
WHITE = (255, 255, 255)
PLAYER1 = (120, 80, 200)
PLAYER2 = (200, 80, 80)
ORANGE = (240, 100, 40)
#สีพื้นหลังบอร์ดเกม 2048 สีเดียวกับเกมออริจิ 
BG_COLOR = (187, 173, 160)
#สีช่องสี่เหลี่ยมของตาราง
TILE_COLOR = (205, 193, 180)
#สีตัวเลขบนช่อง 
TEXT_COLOR = (50, 50, 50)

# ฟอนต์หัวข้อใหญ่
font_title = pygame.font.Font(None, 180)
# ฟ้อนปุ่มเมนู
font_btn = pygame.font.Font(None, 50)
# ฟ้อนตัวเลขบนช่อง
font_num = pygame.font.Font(None, 60)
# นาฬิกาคุมเฟรมเรต 
clock = pygame.time.Clock()

# ปุ่มเมนูสี่เหลี่ยม player one , player two , how to play
player1_rect = pygame.Rect(0, 0, 260, 70)
player2_rect = pygame.Rect(0, 0, 260, 70)
how_rect = pygame.Rect(0, 0, 260, 70)
# คำนวนตำแหน่งกึ่งกลางจอ 
center_x = WIDTH // 2
start_y = HEIGHT // 2 - 50
# ระยะฟ่างระหวางปุ่ม
space = 90
# จัดให้ทุกปุ่มอยุ่กลางจอ 
player1_rect.center = (center_x, start_y)
player2_rect.center = (center_x, start_y + space)
how_rect.center = (center_x, start_y + space * 2)

# --- ตารางเกม ---
grid = [[0] * 4 for _ in range(4)]

def add_random_tile(): #สุ่มตัวเลขเริ่มต้น
    empty = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        grid[r][c] = 2

def reset_game():  #รีเซทตาราง
    global grid
    grid = [[0] * 4 for _ in range(4)]
    add_random_tile()
    add_random_tile()

def draw_menu():
    screen.blit(background, (0, 0))
    title = font_title.render("2048", True, (252, 220, 133))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 3)))

    for rect, text, color in [
        (player1_rect, "Player One", PLAYER1),
        (player2_rect, "Player Two", PLAYER2),
        (how_rect, "How to Play", ORANGE)
    ]:
        pygame.draw.rect(screen, color, rect, border_radius=10)
        screen.blit(font_btn.render(text, True, WHITE),
                    font_btn.render(text, True, WHITE).get_rect(center=rect.center))
    pygame.display.flip()

def draw_game(): #วาดตารางเกมจัดให้อยู้ตรงกลางหน้าจอ
    screen.blit(background, (0, 0))
    size, gap = 120, 15
    start_x = (WIDTH - (size * 4 + gap * 3)) // 2
    start_y = (HEIGHT - (size * 4 + gap * 3)) // 2 - 50

    for r in range(4):
        for c in range(4):
            x, y = start_x + c * (size + gap), start_y + r * (size + gap)
            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(screen, TILE_COLOR, rect, border_radius=8)
            if grid[r][c]:
                text = font_num.render(str(grid[r][c]), True, TEXT_COLOR)
                screen.blit(text, text.get_rect(center=rect.center))

    tip = font_btn.render("Press ESC to Menu", True, (80, 80, 80))
    screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT - 100)))
    pygame.display.flip()

def shift_left(g):
    """เลื่อน + รวมทางซ้าย"""
    new = []
    for r in g:
        row = [x for x in r if x]
        i = 0
        while i < len(row) - 1:
            if row[i] == row[i + 1]:
                row[i] *= 2
                row.pop(i + 1)
            i += 1
        row += [0] * (4 - len(row))
        new.append(row)
    return new

def main():
    global grid
    game_state = "menu"

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if game_state == "menu":
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if player1_rect.collidepoint(e.pos):
                        reset_game(); game_state = "play"
                    elif player2_rect.collidepoint(e.pos):
                        print("Player Two (ยังไม่ทำ)")
                    elif how_rect.collidepoint(e.pos):
                        print("ใช้ปุ่มลูกศรหรือ WASD เพื่อเลื่อนตัวเลข")

            elif game_state == "play":
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        game_state = "menu"

                    before = [r[:] for r in grid]

                    if e.key in (pygame.K_LEFT, pygame.K_a):
                        grid = shift_left(grid)
                    elif e.key in (pygame.K_RIGHT, pygame.K_d):
                        grid = [list(reversed(r)) for r in shift_left([list(reversed(r)) for r in grid])]
                    elif e.key in (pygame.K_UP, pygame.K_w):
                        grid = list(map(list, zip(*shift_left(list(map(list, zip(*grid)))))))
                    elif e.key in (pygame.K_DOWN, pygame.K_s):
                        grid = list(map(list, zip(*[list(reversed(r)) for r in shift_left([list(reversed(r)) for r in zip(*grid)])])))

                    if grid != before:
                        add_random_tile()

        if game_state == "menu": draw_menu()
        elif game_state == "play": draw_game()
        clock.tick(60)

if __name__ == "__main__":
    main()
