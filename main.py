import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

green = (0, 128, 0)
black = (0, 0, 0)

paddle_width, paddle_height = 10, 100
ball_size = 15

paddle1 = pygame.Rect(50, height // 2 - paddle_height // 2, paddle_width, paddle_height)
paddle2 = pygame.Rect(width - 50 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)
ball = pygame.Rect(width // 2 - ball_size // 2, height // 2 - ball_size // 2, ball_size, ball_size)


ball_speed_x, ball_speed_y = 4, 4
paddle_speed = 7

score1, score2 = 0, 0
win_score = 5
font = pygame.font.SysFont(None, 50)
game_over_font = pygame.font.SysFont(None, 70)

clock = pygame.time.Clock()
running = True
game_active = True


obstacles = []
for _ in range(4):
    obstacle = pygame.Rect(random.randint(150, width - 150), random.randint(50, height - 50), 30, 30)
    obstacles.append(obstacle)
obstacle_color = (200, 200, 200)


speed_increment = 0.2
max_speed = 10

def reset_ball():
    """Сбрасывает мяч в центр и задаёт ему случайное направление."""
    ball.center = (width // 2, height // 2)
  
    angle = random.uniform(-1, 1) * (3.14 / 4) 
    speed = random.choice([4, -4])

    
    global ball_speed_x, ball_speed_y
    ball_speed_x = speed
    ball_speed_y = speed * angle 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_active:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1.top > 0:
            paddle1.y -= paddle_speed
        if keys[pygame.K_s] and paddle1.bottom < height:
            paddle1.y += paddle_speed
        if keys[pygame.K_UP] and paddle2.top > 0:
            paddle2.y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle2.bottom < height:
            paddle2.y += paddle_speed

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        
        if ball.top <= 0 or ball.bottom >= height:
            ball_speed_y *= -1

        
        if ball.left <= 0:
            score2 += 1
            reset_ball()
        if ball.right >= width:
            score1 += 1
            reset_ball()

        
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            ball_speed_x *= -1

       
        for obstacle in obstacles:
            if ball.colliderect(obstacle):
                
                ball_speed_x *= -1
                ball_speed_y *= -1
               
                if abs(ball_speed_x) < max_speed:
                    ball_speed_x *= (1 + speed_increment)
                if abs(ball_speed_y) < max_speed:
                    ball_speed_y *= (1 + speed_increment)

        screen.fill(green)
        pygame.draw.rect(screen, black, paddle1)
        pygame.draw.rect(screen, black, paddle2)
        pygame.draw.ellipse(screen, black, ball)
        pygame.draw.aaline(screen, black, (width // 2, 0), (width // 2, height))

   
        for obstacle in obstacles:
            pygame.draw.rect(screen, obstacle_color, obstacle)

        score_text = font.render(f"{score1}  {score2}", True, black)
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))

       
        if score1 == win_score or score2 == win_score:
            game_active = False

    else:
        winner_text = f"Игрок {1 if score1 == win_score else 2} победил!"
        game_over_text = game_over_font.render(winner_text, True, black)
        restart_text = font.render("Нажмите R для рестарта", True, black)
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 20))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            score1, score2 = 0, 0
            game_active = True
            reset_ball() 

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()