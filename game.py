import pygame
import sys

# --- ตั้งค่าเริ่มต้น ---
pygame.init()
WIDTH, HEIGHT = 700, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 - Start Screen")

# --- สีและฟอนต์ ---
BG_COLOR = (187, 173, 160)
WHITE = (255, 255, 255)
FONT = pygame.font.Font(None, 72)

# --- ฟังก์ชันสำหรับวาดหน้าจอเริ่มต้น ---
def draw_start_screen():
    SCREEN.fill(BG_COLOR)
    
    # ชื่อเกม
    title = FONT.render("2048", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
    SCREEN.blit(title, title_rect)
    
    pygame.display.flip()

# --- ลูปหลักของหน้าแรก ---
def main():
    running = True
    while running:
        draw_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # ถ้ากด ENTER
                    print("Start Game!") #ค่อยเข้า main ทีหลัง
                    running = False  # ปิดหน้า
        
        pygame.time.Clock().tick(60)

if __name__ == "__main__": 
   main()