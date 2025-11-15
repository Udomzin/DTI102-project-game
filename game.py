import pygame, sys, random, os
pygame.init()

#หน้าจอ ฟลุค
WIDTH, HEIGHT = 1440, 824
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

#โหลดภาพพื้นหลัง 
#background = pygame.image.load("background.png")
#background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # ปรับให้พอดีหน้าจอ

#โหลดภาพพื้นหลังเเละปรับขนาด
current_dir = os.path.dirname(__file__)
background_path = os.path.join(current_dir, "background.png")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

how_path = os.path.join(current_dir, "howtoplay.png")
how = pygame.image.load(how_path)

#กำหนดสีช่อง เตย
COLOR_SET = {
    0: (180, 160, 140),
    2: (210, 255, 120),
    4: (220, 180, 255),
    8: (250, 180, 110),
    16: (255, 140, 60),
    32: (200, 120, 255),
    64: (160, 130, 255),
    128: (120, 50, 160),
    256: (150, 80, 200),
    512: (180, 100, 240),
    1024: (210, 120, 255),
    2048: (255, 220, 130)
}

#สี แตง
PURPLE = (90, 0, 140)
WHITE = (255, 255, 255)
PLAYER1 = (120, 80, 200)
PLAYER2 = (200, 80, 80)
ORANGE = (240, 100, 40)
BG_COLOR = (66, 1, 105)
TILE_COLOR = (252, 220, 133)
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
score_p1, score_p2 = 0, 0

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

#สร้าง draw ปุ่ม แตง

BUTTONS_P1 = {"undo": None, "swap": None, "delete": None}
BUTTONS_P2 = {"undo": None, "swap": None, "delete": None}

BUTTON_USED_P1 = {"undo": False, "swap": False, "delete": False}
BUTTON_USED_P2 = {"undo": False, "swap": False, "delete": False}

def reset_buttons():
    for d in (BUTTON_USED_P1, BUTTON_USED_P2):
        for k in d:
            d[k] = False

Button_W = 160
Button_H = 60
Button_SPACE = 20

def draw_buttons(start_x, start_y, size, gap, for_player="p1"):
    board_w = size * 4 + gap * 3
    board_h = size * 4 + gap * 3
    bar_y = start_y + board_h + 25
    bar_w = Button_W * 3 + Button_SPACE * 2
    bar_x = start_x + (board_w - bar_w) // 2

    #กล่องปุ่ม
    undo_rect   = pygame.Rect(bar_x, bar_y, Button_W, Button_H)
    swap_rect   = pygame.Rect(bar_x + Button_W + Button_SPACE, bar_y, Button_W, Button_H)
    delete_rect = pygame.Rect(bar_x + 2 * (Button_W + Button_SPACE), bar_y, Button_W, Button_H)


    used_state = BUTTON_USED_P1 if for_player == "p1" else BUTTON_USED_P2

    normal_color = (205, 193, 180)     
    used_color   = (200, 0, 0)         

    undo_color   = used_color if used_state["undo"] else normal_color
    swap_color   = used_color if used_state["swap"] else normal_color
    delete_color = used_color if used_state["delete"] else normal_color

    pygame.draw.rect(screen, undo_color, undo_rect, border_radius=10)
    pygame.draw.rect(screen, swap_color, swap_rect, border_radius=10)
    pygame.draw.rect(screen, delete_color, delete_rect, border_radius=10)


    t1 = font_btn.render("Undo", True, (255, 255, 255))
    t2 = font_btn.render("Swap", True, (255, 255, 255))
    t3 = font_btn.render("Delete", True, (255, 255, 255))
    screen.blit(t1, t1.get_rect(center=undo_rect.center))
    screen.blit(t2, t2.get_rect(center=swap_rect.center))
    screen.blit(t3, t3.get_rect(center=delete_rect.center))

    #เก็บ rect เพื่อจับคลิก แยกผู้เล่น
    target = BUTTONS_P1 if for_player == "p1" else BUTTONS_P2
    target["undo"]   = undo_rect
    target["swap"]   = swap_rect
    target["delete"] = delete_rect

#วาดตารางเกมจัดให้อยู้ตรงกลางหน้าจอ ฟลุค
def draw_board(grid, start_x, start_y, label):
    size, gap = 120, 15
    
    if label:
        lbl = font_btn.render(label, True, WHITE)
        screen.blit(lbl, (start_x + 90, start_y - 60))
    for r in range(4):
        for c in range(4):
            x, y = start_x + c * (size + gap), start_y + r * (size + gap)
            rect = pygame.Rect(x, y, size, size)
            pygame.draw.rect(screen, TILE_COLOR, rect, border_radius=8)
            value = grid[r][c]
            
            #กำหนดสีในเเต่ละช่อง เตย
            color = COLOR_SET.get(value, (60, 58, 50))
            pygame.draw.rect(screen, color, rect, border_radius=8)

            #ถ้าช่องมีตัวเลข จะเลือกสีตัวเลขตามค่า เตย
            if value:
                if value in (2, 4):
                    text_color = (80, 80, 80)
                elif value >= 1024:
                    text_color = (60, 50, 40)
                else:
                    text_color = (255, 255, 255)

                text = font_num.render(str(value), True, text_color)
                screen.blit(text, text.get_rect(center=rect.center))

#วาดเกมเช็คสองผู้เล่น ฟลุค , แตงแก้ 
def draw_game(grid1, grid2=None):
    screen.blit(background, (0, 0))
    size, gap = 120, 15
    
    # โหมดผู้เล่นเดียว
    if grid2 is None:
        p1_x = WIDTH//2 - 240
        p1_y = HEIGHT//2 - 240
        draw_board(grid1, p1_x, p1_y, f"P1 | Score: {score_p1}")
        draw_buttons(p1_x, p1_y, size, gap, for_player="p1")
        
    # โหมดผู้เล่นสองคน
    else:
        p1_x = WIDTH//2 - 600
        p1_y = HEIGHT//2 - 240
        p2_x = WIDTH//2 + 120
        p2_y = HEIGHT//2 - 240

        draw_board(grid1, p1_x, p1_y, f"P1 | Score: {score_p1}")
        draw_board(grid2, p2_x, p2_y, f"P2 | Score: {score_p2}")

        draw_buttons(p1_x, p1_y, size, gap, for_player="p1")
        draw_buttons(p2_x, p2_y, size, gap, for_player="p2")

    pygame.display.flip()

def how_to_play():
    screen.blit(how, (0, 0))
    pygame.display.flip()
    
def draw_menu():
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BG_COLOR)

    #หัวข้อใหญ่
    title = font_title.render("2048", True, TILE_COLOR)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 180)))

    #วาดปุ่ม 3 ปุ่ม แตง 
    pygame.draw.rect(screen, PLAYER1, player1_rect, border_radius=12)
    pygame.draw.rect(screen, PLAYER2, player2_rect, border_radius=12)
    pygame.draw.rect(screen, ORANGE,   how_rect,   border_radius=12)

    t1 = font_btn.render("Player One", True, WHITE)
    t2 = font_btn.render("Player Two", True, WHITE)
    t3 = font_btn.render("How to Play", True, WHITE)

    screen.blit(t1, t1.get_rect(center=player1_rect.center))
    screen.blit(t2, t2.get_rect(center=player2_rect.center))
    screen.blit(t3, t3.get_rect(center=how_rect.center))

    pygame.display.flip()

#ขยับและรวมตัวเลขไปทางซ้าย ธี ,ฟลุคเพิ่มคะแนน
def move_left(g):
    new_grid = []
    gain = 0
    for r in g:
        row = [x for x in r if x != 0]
        i = 0
        while i < len(row) - 1:
            if row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
                gain += 1  
            i += 1
        row = [x for x in row if x != 0]
        row += [0] * (4 - len(row))
        new_grid.append(row)
    return new_grid, gain


#ขยับและรวมตัวเลขไปทางขวา ธี,ฟลุคเพิ่มคะแนน
def move_right(grid):
    new_grid = []
    gain = 0
    for row in grid:
        reversed_row = row[::-1]
        moved, g = move_left([reversed_row])
        new_grid.append(moved[0][::-1])
        gain += g
    return new_grid, gain


#ขยับและรวมตัวเลขขึ้นข้างบน ธี,ฟลุคเพิ่มคะแนน
def move_up(grid):
    new_grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    gain = 0

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
                gain += 1
            i += 1                     
        col = [x for x in col if x != 0]
        while len(col) < 4:
            col.append(0)
        for r in range(4):
            new_grid[r][c] = col[r]

    return new_grid , gain

#ขยับและรวมตัวเลขลงข้างล่าง ธี,ฟลุคเพิ่มคะแนน
def move_down(grid):
    new_grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    gain = 0

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
                gain += 1
            i += 1
        col = [x for x in col if x != 0]
        while len(col) < 4:
            col.append(0)
        for r in range(4):
            new_grid[3 - r][c] = col[r]

    return new_grid , gain

#เช็กว่าเกมจบรึยัง เตย
def is_game_over(grid):
    for r in range(4):
        for c in range(4):
            if grid[r][c] == 0 or (c < 3 and grid[r][c] == grid[r][c + 1]) or (r < 3 and grid[r][c] == grid[r + 1][c]):
                return False
    return True


#หน้าจบเกม เตย
def show_game_over(score):
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

    #รอคลิก เตย
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

#ลูปหลักของเกม ฟลุค(ส่วน+คะแนน) ธี เตย
def main():
    global score_p1, score_p2   
    score_p1, score_p2 = 0, 0   
    game_state = "menu"
    grid1, grid2 = new_grid(), new_grid()
    start_time = 0
    time_over = 60

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if game_state == "menu":
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if player1_rect.collidepoint(e.pos):
                        grid1 = reset_game()
                        score_p1 = 0
                        reset_buttons()
                        game_state = "play1" 
                    elif player2_rect.collidepoint(e.pos):
                        grid1 = reset_game()
                        grid2 = reset_game()
                        score_p1 = 0  
                        score_p2 = 0
                        reset_buttons()
                        start_time = pygame.time.get_ticks()
                        game_state = "play2"
                    elif how_rect.collidepoint(e.pos):
                        game_state = "howtoplay"

            elif game_state in ("play1", "play2", "howtoplay"):
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        game_state = "menu"

                    if game_state == "play1":
                        before = [r[:] for r in grid1]
                        gain = 0
                        if e.key in (pygame.K_LEFT, pygame.K_a):
                            grid1, gain = move_left(grid1)
                        elif e.key in (pygame.K_RIGHT, pygame.K_d):
                            grid1, gain = move_right(grid1)
                        elif e.key in (pygame.K_UP, pygame.K_w):
                            grid1, gain = move_up(grid1)
                        elif e.key in (pygame.K_DOWN, pygame.K_s):
                            grid1, gain = move_down(grid1)

                        score_p1 += gain 

                        if grid1 != before:
                            add_random_tile(grid1)
                            if is_game_over(grid1):
                                result = show_game_over(score_p1)
                                if result == "play_again":
                                    grid1 = reset_game()
                                    score_p1 = 0
                                elif result == "menu":
                                    game_state = "menu"

                    elif game_state == "play2":
                        before1, before2 = [r[:] for r in grid1], [r[:] for r in grid2]
                        gain1 = gain2 = 0

                        # Player 1 
                        if e.key == pygame.K_a:
                            grid1, gain1 = move_left(grid1)
                        elif e.key == pygame.K_d:
                            grid1, gain1 = move_right(grid1)
                        elif e.key == pygame.K_w:
                            grid1, gain1 = move_up(grid1)
                        elif e.key == pygame.K_s:
                            grid1, gain1 = move_down(grid1)

                        # Player 2 
                        if e.key == pygame.K_LEFT:
                            grid2, gain2 = move_left(grid2)
                        elif e.key == pygame.K_RIGHT:
                            grid2, gain2 = move_right(grid2)
                        elif e.key == pygame.K_UP:
                            grid2, gain2 = move_up(grid2)
                        elif e.key == pygame.K_DOWN:
                            grid2, gain2 = move_down(grid2)

                        score_p1 += gain1
                        score_p2 += gain2

                        if grid1 != before1:
                            add_random_tile(grid1)
                        if grid2 != before2:
                            add_random_tile(grid2)

                # คลิกปุ่ม แตง
                elif e.type == pygame.MOUSEBUTTONDOWN and game_state in ("play1", "play2"):
                    mx, my = e.pos

                    
                    if BUTTONS_P1["undo"] and BUTTONS_P1["undo"].collidepoint(mx, my):
                        BUTTON_USED_P1["undo"] = True
                    elif BUTTONS_P1["swap"] and BUTTONS_P1["swap"].collidepoint(mx, my):
                        BUTTON_USED_P1["swap"] = True
                    elif BUTTONS_P1["delete"] and BUTTONS_P1["delete"].collidepoint(mx, my):
                        BUTTON_USED_P1["delete"] = True


                    
                    if game_state == "play2":
                        if BUTTONS_P2["undo"] and BUTTONS_P2["undo"].collidepoint(mx, my):
                            BUTTON_USED_P2["undo"] = True
                        elif BUTTONS_P2["swap"] and BUTTONS_P2["swap"].collidepoint(mx, my):
                            BUTTON_USED_P2["swap"] = True
                        elif BUTTONS_P2["delete"] and BUTTONS_P2["delete"].collidepoint(mx, my):
                            BUTTON_USED_P2["delete"] = True


        #วาดหน้าจอ
        if game_state == "menu":
            draw_menu()
        elif game_state == "play1":
            draw_game(grid1)
        elif game_state == "play2":
            draw_game(grid1, grid2)
        elif game_state == "howtoplay":
            how_to_play()

        #จับเวลา
        if game_state in ("play2"):
            #AI
            time = (pygame.time.get_ticks() - start_time) / 1000
            remaining = max(0, int(time_over - time)) 
            # time_over เวลาทั้งหมดลบด้วย time ที่ผ่านไปแล้วเพื่อหาเวลาที่ยังเหลืออยู่

            #วาดtextเวลา
            timer_text = font_btn.render(f"Time: {remaining}", True, WHITE)
            timer_rect = timer_text.get_rect(center=(WIDTH // 2, 40))
            screen.blit(timer_text, timer_rect)
            pygame.display.flip()

            #ถ้าหมดเวลา
            if remaining <= 0:
                score = score_p1
                result = show_game_over(score)

                if result == "play_again":
                    grid1 = reset_game()
                    start_time = pygame.time.get_ticks()
                    reset_buttons()     

                if game_state == "play2":
                    grid2 = reset_game()

                elif result == "menu":
                    game_state = "menu"

        
        clock.tick(10)

if __name__ == "__main__":
    main()
