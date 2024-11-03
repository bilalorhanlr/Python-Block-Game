import pygame
import random
import sys

# Pygame'i başlat
pygame.init()

# Renk tanımları
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Ekran boyutları
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Paddle (Raketi) ayarları
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 10

# Top ayarları
BALL_SIZE = 10
BALL_SPEED = [5, -5]

# Tuğla ayarları
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_PADDING = 5

# Harita tanımları
maps = [
    {'rows': 5, 'columns': 10},
    {'rows': 3, 'columns': 5},
    {'rows': 7, 'columns': 12}
]
selected_map_index = 0

# Ekranı oluştur
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tuğla Kırma Oyunu")

# Menüdeki seçenekler
font = pygame.font.Font(None, 36)
def draw_menu():
    screen.fill(BLACK)
    title = font.render("Tuğla Kırma Oyunu", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))

    start_button = font.render("Başla", True, GREEN)
    start_rect = start_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(start_button, start_rect)

    quit_button = font.render("Çıkış", True, RED)
    quit_rect = quit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(quit_button, quit_rect)

    map_button = font.render(f"Harita: {selected_map_index + 1}", True, BLUE)
    map_rect = map_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    screen.blit(map_button, map_rect)

    pygame.display.flip()
    return start_rect, quit_rect, map_rect

# Paddle (Raket) pozisyonu
paddle = pygame.Rect((SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2, SCREEN_HEIGHT - 30), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Top pozisyonu
balls = [pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_SIZE, BALL_SIZE))]
ball_speeds = [BALL_SPEED.copy()]

# Tuğlaları oluşturma fonksiyonu
def create_bricks(rows, columns):
    bricks = []
    for row in range(rows):
        for column in range(columns):
            brick_x = column * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
            brick_y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_PADDING
            bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))
    return bricks

# Başlangıç tuğlaları
bricks = create_bricks(maps[selected_map_index]['rows'], maps[selected_map_index]['columns'])

# Puan tablosu
score = 0

# Ana oyun döngüsü
clock = pygame.time.Clock()
game_active = False

def draw_game_over():
    screen.fill(BLACK)
    game_over_text = font.render("Oyun Bitti!", True, YELLOW)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    restart_button = font.render("Yeniden Başla", True, GREEN)
    restart_rect = restart_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_button, restart_rect)
    quit_button = font.render("Çıkış", True, RED)
    quit_rect = quit_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(quit_button, quit_rect)
    pygame.display.flip()
    return restart_rect, quit_rect

while True:
    # Menü ekranı
    if not game_active:
        start_rect, quit_rect, map_rect = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    # Yeni oyun başlat
                    bricks = create_bricks(maps[selected_map_index]['rows'], maps[selected_map_index]['columns'])
                    balls = [pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_SIZE, BALL_SIZE))]
                    ball_speeds = [BALL_SPEED.copy()]
                    score = 0
                    game_active = True
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif map_rect.collidepoint(event.pos):
                    selected_map_index = (selected_map_index + 1) % len(maps)
        continue

    # Olay kontrolü
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Klavye girişleri
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.move_ip(-PADDLE_SPEED, 0)
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.move_ip(PADDLE_SPEED, 0)

    # Top hareketi ve çarpışma kontrolü
    for i, ball in enumerate(balls):
        ball.move_ip(ball_speeds[i])

        # Topun duvara çarpması
        if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
            ball_speeds[i][0] = -ball_speeds[i][0]
        if ball.top <= 0:
            ball_speeds[i][1] = -ball_speeds[i][1]

        # Topun paddle'a (rakete) çarpması
        if ball.colliderect(paddle) and ball_speeds[i][1] > 0:
            ball_speeds[i][1] = -ball_speeds[i][1]

        # Topun tuğlalara çarpması
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_speeds[i][1] = -ball_speeds[i][1]
                score += 10

                # Ara ara top çoğaltma veya delici ışın efekti
                if random.randint(1, 5) == 1:
                    new_ball = pygame.Rect(ball.x, ball.y, BALL_SIZE, BALL_SIZE)
                    new_speed = [random.choice([-5, 5]), random.choice([-5, 5])]
                    balls.append(new_ball)
                    ball_speeds.append(new_speed)
                elif random.randint(1, 5) == 2:
                    # Delici ışın efekti (birden fazla tuğlayı kır)
                    for b in bricks[:]:
                        if b.colliderect(ball):
                            bricks.remove(b)
                            score += 10
                break

        # Topun aşağı düşmesi (oyun bitimi)
        if ball.bottom >= SCREEN_HEIGHT:
            balls.remove(ball)
            ball_speeds.pop(i)
            if not balls:
                game_active = False
                restart_rect, quit_rect = draw_game_over()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if restart_rect.collidepoint(event.pos):
                                # Yeni oyun başlat
                                bricks = create_bricks(maps[selected_map_index]['rows'], maps[selected_map_index]['columns'])
                                balls = [pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_SIZE, BALL_SIZE))]
                                ball_speeds = [BALL_SPEED.copy()]
                                score = 0
                                game_active = True
                                break
                            elif quit_rect.collidepoint(event.pos):
                                pygame.quit()
                                sys.exit()
                    if game_active:
                        break

    # Eğer tüm tuğlalar kırıldıysa oyun bitti
    if not bricks:
        game_active = False
        restart_rect, quit_rect = draw_game_over()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_rect.collidepoint(event.pos):
                        # Yeni oyun başlat
                        bricks = create_bricks(maps[selected_map_index]['rows'], maps[selected_map_index]['columns'])
                        balls = [pygame.Rect((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (BALL_SIZE, BALL_SIZE))]
                        ball_speeds = [BALL_SPEED.copy()]
                        score = 0
                        game_active = True
                        break
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()
            if game_active:
                break

    # Ekranı yenileme
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, paddle)
    for ball in balls:
        pygame.draw.ellipse(screen, ORANGE, ball)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    # Puanı çiz
    score_text = font.render(f"Skor: {score}", True, GREEN)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    # FPS kontrolü
    clock.tick(60)