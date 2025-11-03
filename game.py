import pygame, sys, random
pygame.init()

# --- หน้าจอ ---
WIDTH, HEIGHT = 1440, 824
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# --- โหลดภาพพื้นหลัง ---
#background = pygame.image.load("background.png")
#background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # ปรับให้พอดีหน้าจอ

import os
current_dir = os.path.dirname(__file__)
background_path = os.path.join(current_dir, "background.png")
background = pygame.image.load(background_path)
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# --- สี ---
PURPLE = (90, 0, 140)
WHITE = (255, 255, 255)
PLAYER1 = (120, 80, 200)
PLAYER2 = (200, 80, 80)
ORANGE = (240, 100, 40) 
BG_COLOR = (66, 1, 105)
TILE_COLOR = (205, 193, 180) 
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
    #เลื่อนและรวมตัวเลขไปทางซ้าย  
    new_grid = [] #เก็บตารางใหม่
    for r in g: #วนแถวในตาราง
        row = [x for x in r if x != 0] #วนเลขในแถว ถ้า !=0 จะเก็บใน new
        i = 0 #ใช้เป็นตัวนับสำหรับวนเช็กตัวเลข
        while i < len(row) - 1: #วนจนกว่าจะถึงตัวก่อนสุดท้าย
            if row[i] == row[i + 1]: #ถ้าค่าตัวติดกันเท่ากัน
                row[i] *= 2 #รวมตัวเลขสองตัวนั้น(x2) แล้วเก็บค่าใหม่ไว้
                row[i + 1] = 0 #ลบค่าตัวถัดไปออก (เพราะถูกรวมแล้ว)
            i += 1 #ขยับ i เพื่อเช็กแถวถัดไป
        row += [0] * (4 - len(row)) #หลังจากรวมเลข เติม 0 ให้แถวมีครบ 4 ตัว
        new_grid.append(row) #เพิ่มแถวที่เลื่อนและรวมเสร็จแล้ว เข้าในลิสต์ new
    return new_grid #ส่งคืนตารางใหม่ที่แต่ละแถวถูกเลื่อนและรวมเรียบร้อยแล้ว

def shift_right(grid):
    #เลื่อนและรวมตัวเลขไปทางขวา
    new_grid = []
    for row in grid:
        reversed_row = row[::-1] # กลับด้านไปทางซ้ายเพื่อรวมเลข
        shifted = shift_left([reversed_row])[0] #เลื่อนและรวม เอาที่ได้กลับมาเก็บ [0]คือแถวเดียว
        new_grid.append(shifted[::-1]) #กลับให้เป็นขวาเหมือนเดิม
    return new_grid

def shift_up(grid):
    # สร้างตารางใหม่ขนาด 4x4 ที่เต็มไปด้วยศูนย์ เพื่อเก็บค่าหลังจากเลื่อนขึ้น
    new_grid = [[0]*4 for _ in range(4)]

    # วนลูปทีละคอลัมน์ (แนวตั้ง) ทั้งหมด 4 คอลัมน์
    for c in range(4):
        col = []  # สร้างลิสต์ว่างสำหรับเก็บตัวเลขในคอลัมน์นั้น

        for r in range(4):
            if grid[r][c] != 0:
                col.append(grid[r][c])

        i = 0
        while i < len(col) - 1: 
            if col[i] == col[i + 1]: 
                col[i] *= 2         
                col[i + 1] = 0     
            i += 1                     

        # ลบศูนย์ที่เกิดจากการรวมออก เพื่อให้ตัวเลขขยับขึ้นไปติดกัน
        col = [x for x in col if x != 0]

        # เติม 0 ด้านล่างให้ครบ 4 ตัว (เพราะเลื่อนขึ้น ด้านล่างจะว่าง)
        while len(col) < 4:
            col.append(0)

        # ใส่ค่าที่ได้กลับลงในตำแหน่งคอลัมน์เดิมของตารางใหม่
        for r in range(4):
            new_grid[r][c] = col[r]

    # ส่งคืนตารางใหม่ที่เลื่อนและรวมเสร็จแล้ว
    return new_grid


def shift_down(grid):
    # สร้างตารางใหม่ขนาด 4x4 ที่เต็มไปด้วยศูนย์ เพื่อเก็บค่าหลังจากเลื่อนลง
    new_grid = [[0]*4 for _ in range(4)]

    for c in range(4):
        col = []  # 

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

        # เติม 0 ด้านบนให้ครบ 4 ตัว (เพราะเลื่อนลง ด้านบนจะว่าง)
        while len(col) < 4:
            col.append(0)

        for r in range(4):
            new_grid[3 - r][c] = col[r]

    # ส่งคืนตารางใหม่ที่เลื่อนและรวมเสร็จแล้ว
    return new_grid

def is_game_over(): #เช็กว่าเกมจบหรือยัง
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

def get_score(): #ดูคะแนนตอนเกมจบ
    return sum(sum(r) for r in grid)

def show_game_over(score):
    screen.fill(BG_COLOR)
    text1 = font_title.render("Game Over", True, WHITE)
    text2 = font_num.render(f"Score: {score}", True, WHITE)
    screen.blit(text1, text1.get_rect(center=(WIDTH//2, HEIGHT//2 - 140)))
    screen.blit(text2, text2.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))
    pygame.display.flip()
    
     # สร้างปุ่ม
    btn_width, btn_height = 260, 70
    play_again_rect = pygame.Rect(0, 0, btn_width, btn_height)
    menu_rect = pygame.Rect(0, 0, btn_width, btn_height)
    play_again_rect.center = (WIDTH//2, HEIGHT//2 + 150)
    menu_rect.center = (WIDTH//2, HEIGHT//2 + 240)

    # วาดปุ่ม
    pygame.draw.rect(screen, PLAYER1, play_again_rect, border_radius=10)
    pygame.draw.rect(screen, ORANGE, menu_rect, border_radius=10)

    screen.blit(font_btn.render("Play Again", True, WHITE),
                font_btn.render("Play Again", True, WHITE).get_rect(center=play_again_rect.center))
    screen.blit(font_btn.render("Back to Menu", True, WHITE),
                font_btn.render("Back to Menu", True, WHITE).get_rect(center=menu_rect.center))

    pygame.display.flip()

    # รอคลิก
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
                        grid = shift_right(grid) 
                    elif e.key in (pygame.K_UP, pygame.K_w):
                        grid = shift_up(grid)
                    elif e.key in (pygame.K_DOWN, pygame.K_s):
                        grid = shift_down(grid) 
                        
                    if grid != before:
                        add_random_tile()
                    if is_game_over():
                        score = get_score()
                        show_game_over(score)
                        game_state = "menu"

        if game_state == "menu": draw_menu()
        elif game_state == "play": draw_game()
        clock.tick(60)

if __name__ == "__main__":
    main()