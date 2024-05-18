# collision.py

from vec import vec
from circle import Ball, Player, circle
from box import Box

def check_circle_collision(circle1: circle, circle2: circle) -> bool:
    """Check if two circles are colliding."""
    distance = vec.dist(circle1.position, circle2.position)
    return distance < (circle1.radius + circle2.radius)

def resolve_collision(circle1: circle, circle2: circle) -> None:
    """Resolve collision between two circles by updating their velocities."""
    if check_circle_collision(circle1, circle2):
        # Calculate the normal vector
        normal = circle2.position - circle1.position
        distance = vec.norm(normal)
        if distance == 0:
            return  # Avoid division by zero

        overlap = (circle1.radius + circle2.radius) - distance
        normal = normal * (1 / distance)

        # Move circles apart based on their masses
        circle1.position = circle1.position - (normal * (overlap / 2))
        circle2.position = circle2.position + (normal * (overlap / 2))

        # Adjust velocities to reflect pushing each other
        relative_velocity = circle2.velocity - circle1.velocity
        velocity_along_normal = vec.dot(relative_velocity, normal)
        
        if velocity_along_normal > 0:
            return

        restitution = 0  # No bounce
        impulse_scalar = -(1 + restitution) * velocity_along_normal
        impulse_scalar /= 1 / circle1.radius + 1 / circle2.radius

        impulse = normal * impulse_scalar

        circle1.velocity = circle1.velocity - (impulse / circle1.radius)
        circle2.velocity = circle2.velocity + (impulse / circle2.radius)

def handle_ball_player_collision(ball: Ball, player: Player) -> None:
    """Handle collision between the ball and a player."""
    resolve_collision(player, ball)

def handle_player_player_collision(player1: Player, player2: Player) -> None:
    """Handle collision between two players."""
    resolve_collision(player1, player2)

def handle_ball_box_collision(ball: Ball, box: Box) -> None:
    """Handle collision between the ball and the box."""
    if ball.left < box.position.x:
        ball.position.x = box.position.x + ball.radius
        ball.velocity.x = -ball.velocity.x
    elif ball.right > box.position.x + box.width:
        ball.position.x = box.position.x + box.width - ball.radius
        ball.velocity.x = -ball.velocity.x

    if ball.top < box.position.y:
        ball.position.y = box.position.y + ball.radius
        ball.velocity.y = -ball.velocity.y
    elif ball.bottom > box.position.y + box.height:
        ball.position.y = box.position.y + box.height - ball.radius
        ball.velocity.y = -ball.velocity.y

def handle_player_box_collision(player: Player, box: Box) -> None:
    """Handle collision between the player and the box."""
    if player.left < box.position.x:
        player.position.x = box.position.x + player.radius
        player.velocity.x = 0
    elif player.right > box.position.x + box.width:
        player.position.x = box.position.x + box.width - player.radius
        player.velocity.x = 0

    if player.top < box.position.y:
        player.position.y = box.position.y + player.radius
        player.velocity.y = 0
    elif player.bottom > box.position.y + box.height:
        player.position.y = box.position.y + box.height - player.radius
        player.velocity.y = 0

def attract_ball(player: Player, ball: Ball) -> None:
    """Apply an attraction force to the ball if it is within the player's attraction radius."""
    distance_to_ball = vec.dist(player.position, ball.position) - ball.radius
    if distance_to_ball < player.attraction_radius:
        # Apply a slight attraction force to the ball
        attraction_force = (player.position - ball.position) * 0.003  # Arbitrary small force value
        ball.velocity = ball.velocity + attraction_force

def shoot(player: Player, ball: Ball) -> None:
    """Shoot the ball if it is within the player's attraction radius."""
    distance_to_ball = vec.dist(player.position, ball.position) - ball.radius
    if distance_to_ball < player.attraction_radius:
        # Apply a shooting force to the ball
        shooting_force = (ball.position - player.position) * player.shoot_force  # Arbitrary shooting force value
        
        ball.velocity = ball.velocity + shooting_force
