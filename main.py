import pygame
from vec import vec
from circle import Ball, Player
from box import Box
from collision import handle_ball_player_collision, handle_ball_box_collision, handle_player_box_collision, attract_ball, shoot

# Initialize Pygame and create window
pygame.init()
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))

# Create box
box = Box(width=700, height=400, window_width=window_width, window_height=window_height)

# Create ball and player
ball = Ball(position=vec(400, 300), radius=10)
player = Player(position=vec(100, 300), radius=20, player_id=1, shoot_force=9)
ball.velocity.x = 30
ball.velocity.y = 30

MAX_SPEED = 400  # Maximum speed for the player

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Update game state
    delta_time = clock.get_time() / 1000.0

    ball.update(delta_time)
    player.move(keys, delta_time)
    player.update(delta_time)  # Call the update method to apply the acceleration and friction

    # Handle collisions
    handle_ball_box_collision(ball, box)
    handle_ball_player_collision(ball, player)
    handle_player_box_collision(player, box)
    attract_ball(player, ball)  # Apply attraction force to the ball if it is within the attraction circle

    # Shoot the ball if space is pressed
    if keys[pygame.K_SPACE]:
        shoot(player, ball)

    # Render game state
    window.fill((255, 255, 255))
    box.render(window)
    ball.render(window)
    player.render(window)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
