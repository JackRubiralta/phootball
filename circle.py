from vec import vec
import pygame

class circle:
    def __init__(self, position: vec, radius: float) -> None:
        self.radius: float = radius
        self.position: vec = position
        self.velocity: vec = vec(0.0, 0.0)
        self.acceleration: vec = vec(0.0, 0.0)

    def update(self, delta_time: float) -> None:
        self.velocity = self.velocity + (self.acceleration * delta_time)
        # Apply friction force as a scaling factor
        friction_force = self.velocity * self.friction
        self.velocity = self.velocity + friction_force * delta_time
        self.position = self.position + (self.velocity * delta_time)

    def render(self, window) -> None:
        scale_factor = 7 # Scale factor for anti-aliasing
        large_surface = pygame.Surface((self.radius * 2 * scale_factor, self.radius * 2 * scale_factor), pygame.SRCALPHA)
        pygame.draw.circle(large_surface, (0, 0, 255), (self.radius * scale_factor, self.radius * scale_factor), self.radius * scale_factor)
        smooth_surface = pygame.transform.smoothscale(large_surface, (self.radius * 2, self.radius * 2))
        window.blit(smooth_surface, (int(self.position.x - self.radius), int(self.position.y - self.radius)))

    @property
    def left(self) -> float:
        return self.position.x - self.radius
    
    @property
    def right(self) -> float:
        return self.position.x + self.radius
    
    @property
    def top(self) -> float:
        return self.position.y - self.radius
    
    @property
    def bottom(self) -> float:
        return self.position.y + self.radius

class Ball(circle):
    friction: float = -0.3  # Static friction force for all Ball instances

    def __init__(self, position: vec, radius: float) -> None:
        super().__init__(position, radius)

    def render(self, window) -> None:
        scale_factor = 7  # Scale factor for anti-aliasing
        large_surface = pygame.Surface((self.radius * 2 * scale_factor, self.radius * 2 * scale_factor), pygame.SRCALPHA)
        pygame.draw.circle(large_surface, (255, 0, 0), (self.radius * scale_factor, self.radius * scale_factor), self.radius * scale_factor)
        smooth_surface = pygame.transform.smoothscale(large_surface, (self.radius * 2, self.radius * 2))
        window.blit(smooth_surface, (int(self.position.x - self.radius), int(self.position.y - self.radius)))

class Player(circle):
    friction: float = -1.5  # Static friction force for all Player instances

    def __init__(self, position: vec, radius: float, shoot_force: int, player_id: int) -> None:
        super().__init__(position, radius)
        self.player_id: int = player_id
        self.attraction_radius: int = int(radius * 1.3)
        self.shoot_force = shoot_force


    def render(self, window) -> None:
        scale_factor = 10  # Scale factor for anti-aliasing
        large_surface = pygame.Surface((self.radius * 2 * scale_factor, self.radius * 2 * scale_factor), pygame.SRCALPHA)
        pygame.draw.circle(large_surface, (0, 255, 0), (self.radius * scale_factor, self.radius * scale_factor), self.radius * scale_factor)
        smooth_surface = pygame.transform.smoothscale(large_surface, (self.radius * 2, self.radius * 2))
        window.blit(smooth_surface, (int(self.position.x - self.radius), int(self.position.y - self.radius)))

        # Draw the attraction circle
        pygame.draw.circle(window, (0, 255, 0), (int(self.position.x), int(self.position.y)), self.attraction_radius, 1)

    def move(self, keys, delta_time: float) -> None:
        MAX_SPEED = 100
        ACCELERATION = 300
        self.acceleration = vec(0, 0)
        
        if keys[pygame.K_w]:
            self.acceleration.y -= ACCELERATION
        if keys[pygame.K_s]:
            self.acceleration.y += ACCELERATION
        if keys[pygame.K_a]:
            self.acceleration.x -= ACCELERATION
        if keys[pygame.K_d]:
            self.acceleration.x += ACCELERATION
        
        # Limit the velocity to the max speed
        self.velocity = self.velocity + (self.acceleration * delta_time)
        speed = vec.norm(self.velocity)
        if speed > MAX_SPEED:
            self.velocity = self.velocity * (MAX_SPEED / speed)

        # Apply friction force as a scaling factor
        friction_force = self.velocity * self.friction
        self.velocity = self.velocity + friction_force * delta_time
        self.position = self.position + (self.velocity * delta_time)
