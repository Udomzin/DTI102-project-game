import pygame, sys, random, os
pygame.init()

#หน้าจอ ฟลุค
WIDTH, HEIGHT = 1440, 824
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")


#โหลดภาพพื้นหลัง 
#background = pygame.image.load("background.png")
#background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # ปรับให้พอดีหน้าจอ


current_dir = os.path.dirname(__file__)
background_path = os.path.join(current_dir, "background.png")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

#สี แตง
PURPLE = (90, 0, 140)
WHITE = (255, 255, 255)
PLAYER1 = (120, 80, 200)
PLAYER2 = (200, 80, 80)
ORANGE = (240, 100, 40)
BG_COLOR = (66, 1, 105)
TILE_COLOR = (205, 193, 180)
TEXT_COLOR = (50, 50, 50)

#ฟอนต์หัวข้อใหญ่ แตง
font_title = pygame.font.Font(None, 180)
font_btn = pygame.font.Font(None, 50)
font_num = pygame.font.Font(None, 60)
clock = pygame.time.Clock()

#ปุ่มเมนูสี่เหลี่ยม player one , player two , how to play แตง
player1_rect = pygame.Rect(0, 0, 260, 70)
player2_rect = pygame.Rect(0, 0, 260, 70)
how_rect = pygame.Rect(0, 0, 260, 70)
center_x = WIDTH // 2
start_y = HEIGHT // 2 - 50
space = 90
player1_rect.center = (center_x, start_y)
player2_rect.center = (center_x, start_y + space)
how_rect.center = (center_x, start_y + space * 2)

#ตารางเกม ฟลุค
def new_grid():
    return [[0] * 4 for G in range(4)]

def add_random_tile(grid):
    empty = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
    if empty:
        r, c = random.choice(empty)
        grid[r][c] = 2

#รีเซทตาราง ฟลุค
def reset_game():
    g = new_grid()
    add_random_tile(g)
    add_random_tile(g)
    return g

# ปุ่มในเกม #undo,swap,delete แตง        
Button_W, Button_H, Button_SPACE = 120, 60, 18
Button_undo_rect   = pygame.Rect(0, 0, Button_W, Button_H)
Button_swap_rect   = pygame.Rect(0, 0, Button_W, Button_H)
Button_delete_rect = pygame.Rect(0, 0, Button_W, Button_H)


def draw_buttons(start_x, start_y, size, gap):
    board_w = size * 4 + gap * 3
    board_h = size * 4 + gap * 3

    bar_y = start_y + board_h + 25
    bar_w = Button_W * 3 + Button_SPACE * 2
    bar_x = (WIDTH - bar_w) // 2
 
    Button_undo_rect.topleft   = (bar_x + 0 * (Button_W + Button_SPACE), bar_y)
    Button_swap_rect.topleft   = (bar_x + 1 * (Button_W + Button_SPACE), bar_y)
    Button_delete_rect.topleft = (bar_x + 2 * (Button_W + Button_SPACE), bar_y)
    
    bar_bg_rect = pygame.Rect(bar_x - 16, bar_y - 16, bar_w + 32, Button_H + 32)
    pygame.draw.rect(screen, (225, 218, 200), bar_bg_rect, border_radius=24)

    def draw_button(rect,label):
        pygame.draw.rect(screen, (205, 193, 180), rect, border_radius=16)
        icon = font_btn.render(label, True, (255, 255, 255))
        screen.blit(icon, icon.get_rect(center=rect.center))

    draw_button(Button_undo_rect,   "undo")
    draw_button(Button_swap_rect,   "swap")
    draw_button(Button_delete_rect, "delete")


def draw_menu():
    screen.blit(background, (0, 0))
    title = font_title.render("2048", True, (250, 220, 133))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 3.5)))

    for rect, text, color in [
        (player1_rect, "Player One", PLAYER1),
        (player2_rect, "Player Two", PLAYER2),
        (how_rect, "How to Play", ORANGE)
    ]:
        pygame.draw.rect(screen, color, rect, border_radius=10)
        screen.blit(font_btn.render(text, True, WHITE),
                    font_btn.render(text, True, WHITE).get_rect(center=rect.center))
    pygame.display.flip()

 #วาดตารางเกมจัดให้อยู้ตรงกลางหน้าจอ ฟลุค
def draw_board(grid, start_x, start_y, label=None):
    size, gap = 120, 15
    if label:
        lbl = font_btn.render(label, True, WHITE)
        screen.blit(lbl, (start_x + 90, start_y - 60))
    for r in range(4):
        for c in range(4):
            x, y = start_x + c * (size + gap), start_y + r * (size + gap)
            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(screen, TILE_COLOR, rect, border_radius=8)
            if grid[r][c]:
                text = font_num.render(str(grid[r][c]), True, TEXT_COLOR)
                screen.blit(text, text.get_rect(center=rect.center))

# วาดเกมเช็คสองผู้เล่น ฟลุค
def draw_game(grid1, grid2=None):
    screen.blit(background, (0, 0))
    if grid2 is None:
        draw_board(grid1, WIDTH//2 - 240, HEIGHT//2 - 240, "P1")
    else:
        draw_board(grid1, WIDTH//2 - 600, HEIGHT//2 - 240, "P1")
        draw_board(grid2, WIDTH//2 + 120, HEIGHT//2 - 240, "P2")
    draw_buttons(WIDTH//2 - 240, HEIGHT//2 - 240, 120, 15)
    screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT - 60)))
    pygame.display.flip()

def shift_left(g): #ขยับและรวมตัวเลขไปทางซ้าย ธี
    
    new_grid = [] 
    for r in g:
        row = [x for x in r if x != 0]
        i = 0
        while i < len(row) - 1:
            if row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
            i += 1
        row += [0] * (4 - len(row))
        new_grid.append(row)
    return new_grid

def shift_right(grid): #ขยับและรวมตัวเลขไปทางขวา ธี
    
    new_grid = []
    for row in grid:
        reversed_row = row[::-1]
        shifted = shift_left([reversed_row])[0]
        new_grid.append(shifted[::-1])
    return new_grid

def shift_up(grid): #ขยับและรวมตัวเลขขึ้นข้างบน ธี
    new_grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]

    for c in range(4):
        col = []
        for r in range(4):
            if grid[r][c] != 0:
                col.append(grid[r][c])
        i = 0
        while i < len(col) - 1: 
            if col[i] == col[i + 1]: 
                col[i] *= 2         
                col[i + 1] = 0     
            i += 1                     
        col = [x for x in col if x != 0]
        while len(col) < 4:
            col.append(0)
        for r in range(4):
            new_grid[r][c] = col[r]

    return new_grid

def shift_down(grid): #ขยับและรวมตัวเลขลงข้างล่าง ธี
    new_grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]

    for c in range(4):
        col = []  
        for r in range(3, -1, -1):
            if grid[r][c] != 0: 
                col.append(grid[r][c])
        i = 0
        while i < len(col) - 1:
            if col[i] == col[i + 1]:
                col[i] *= 2 
                col[i + 1] = 0 
            i += 1
        col = [x for x in col if x != 0]
        while len(col) < 4:
            col.append(0)
        for r in range(4):
            new_grid[3 - r][c] = col[r]

    return new_grid

def is_game_over(grid): #เช็กว่าเกมจบรึยัง เตย
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0:
                return False
    for r in range(4):
        for c in range(4):
            if c < 3 and grid[r][c] == grid[r][c + 1]:
                return False
            if r < 3 and grid[r][c] == grid[r + 1][c]:
                return False
    return True

def get_score(grid): #ดูคะแนนตอนเกมจบ เตย
    return sum(sum(r) for r in grid)

def show_game_over(score): #หน้าจบเกม เตย
    screen.fill(BG_COLOR)
    text1 = font_title.render("Game Over", True, WHITE)
    text2 = font_num.render(f"Score: {score}", True, WHITE)
    screen.blit(text1, text1.get_rect(center=(WIDTH//2, HEIGHT//2 - 140)))
    screen.blit(text2, text2.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
    pygame.display.flip()
    
    #สร้างปุ่ม เตย
    btn_width, btn_height = 260, 70
    play_again_rect = pygame.Rect(0, 0, btn_width, btn_height)
    menu_rect = pygame.Rect(0, 0, btn_width, btn_height)
    play_again_rect.center = (WIDTH//2, HEIGHT//2 + 150)
    menu_rect.center = (WIDTH//2, HEIGHT//2 + 240)

    #วาดปุ่ม เตย
    pygame.draw.rect(screen, PLAYER1, play_again_rect, border_radius=10)
    pygame.draw.rect(screen, ORANGE, menu_rect, border_radius=10)

    screen.blit(font_btn.render("Play Again", True, WHITE),
                font_btn.render("Play Again", True, WHITE).get_rect(center=play_again_rect.center))
    screen.blit(font_btn.render("Back to Menu", True, WHITE),
                font_btn.render("Back to Menu", True, WHITE).get_rect(center=menu_rect.center))

    pygame.display.flip()

        #รอคลิก
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if play_again_rect.collidepoint(e.pos):
                    return "play_again"
                elif menu_rect.collidepoint(e.pos):
                    return "menu"


#ลูปหลักของเกม ฟลุค ธี เตย
def main():
    game_state = "menu"
    grid1, grid2 = new_grid(), new_grid()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if game_state == "menu":
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if player1_rect.collidepoint(e.pos):
                        grid1 = reset_game()
                        game_state = "play1"
                    elif player2_rect.collidepoint(e.pos):
                        grid1 = reset_game()
                        grid2 = reset_game()
                        game_state = "play2"
                    elif how_rect.collidepoint(e.pos):
                        print("WASD / ลูกศร เพื่อเลื่อนช่องเลข")

            elif game_state in ("play1", "play2"):
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        game_state = "menu"

                    if game_state == "play1":
                        before = [r[:] for r in grid1]
                        if e.key in (pygame.K_LEFT, pygame.K_a): grid1 = shift_left(grid1)
                        elif e.key in (pygame.K_RIGHT, pygame.K_d): grid1 = shift_right(grid1)
                        elif e.key in (pygame.K_UP, pygame.K_w): grid1 = shift_up(grid1)
                        elif e.key in (pygame.K_DOWN, pygame.K_s): grid1 = shift_down(grid1)
                        
                        if grid1 != before:
                            add_random_tile(grid1)

                            #ตรวจสอบว่าเกมจบหรือยัง
                            if is_game_over(grid1):
                                score = get_score(grid1)
                                result = show_game_over(score)
                                if result == "play_again":
                                    grid1 = reset_game()
                                elif result == "menu":
                                    game_state = "menu"


                    elif game_state == "play2":
                        before1 = [r[:] for r in grid1]
                        before2 = [r[:] for r in grid2]

                        # Player 1 (WASD)
                        if e.key == pygame.K_a: grid1 = shift_left(grid1)
                        elif e.key == pygame.K_d: grid1 = shift_right(grid1)
                        elif e.key == pygame.K_w: grid1 = shift_up(grid1)
                        elif e.key == pygame.K_s: grid1 = shift_down(grid1)

                        # Player 2 (Arrow keys)
                        if e.key == pygame.K_LEFT: grid2 = shift_left(grid2)
                        elif e.key == pygame.K_RIGHT: grid2 = shift_right(grid2)
                        elif e.key == pygame.K_UP: grid2 = shift_up(grid2)
                        elif e.key == pygame.K_DOWN: grid2 = shift_down(grid2)

                        if grid1 != before1: add_random_tile(grid1)
                        if grid2 != before2: add_random_tile(grid2)

        # วาด หน้าจอ
        if game_state == "menu":
            draw_menu()
        elif game_state == "play1":
            draw_game(grid1)
        elif game_state == "play2":
            draw_game(grid1, grid2)

        clock.tick(60)

if __name__ == "__main__":
    main()
