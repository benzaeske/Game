import pygame

pygame.init()

# Get the current display information
infoObject = pygame.display.Info()

# Set global screen size based on display size and set full screen
WIDTH = infoObject.current_w
HEIGHT = infoObject.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

# Set background asset scaling based on global screen size
BACKGROUND_WIDTH = (HEIGHT if (HEIGHT < WIDTH) else WIDTH) - 60
BACKGROUND_HEIGHT = (HEIGHT if (HEIGHT < WIDTH) else WIDTH) - 60
BACKGROUND_X_PADDING = (WIDTH / 2) - (BACKGROUND_WIDTH / 2)
BACKGROUND_Y_PADDING = (HEIGHT / 2) - (BACKGROUND_HEIGHT / 2)

# Load background asset
original_background = pygame.image.load("images/basic_background.png").convert()
scaled_background = pygame.transform.scale(
    original_background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT)
)

# Load player asset
player = pygame.image.load("images/turtle.png").convert_alpha()
PLAYER_WIDTH = player.get_width()
PLAYER_HEIGHT = player.get_height()
PLAYER_STARTING_POS_X = (WIDTH / 2) - (PLAYER_WIDTH / 2)
PLAYER_STARTING_POS_Y = HEIGHT / 7


class GameObject:
    def __init__(self, asset, init_x, init_y, speed):
        self.speed = speed
        self.asset = asset
        self.pos = asset.get_rect().move(
            init_x, init_y
        )  # Get the Rect for the asset's Surface and move it

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self.pos.right += self.speed
        if left:
            self.pos.right -= self.speed
        if down:
            self.pos.top += self.speed
        if up:
            self.pos.top -= self.speed
        # Don't let objects go out of bounds relative to background
        if self.pos.right > BACKGROUND_X_PADDING + BACKGROUND_WIDTH:
            self.pos.right = BACKGROUND_X_PADDING + BACKGROUND_WIDTH
        if self.pos.bottom > BACKGROUND_Y_PADDING + BACKGROUND_HEIGHT:
            self.pos.bottom = BACKGROUND_Y_PADDING + BACKGROUND_HEIGHT
        if self.pos.left < BACKGROUND_X_PADDING:
            self.pos.left = BACKGROUND_X_PADDING
        if self.pos.top < BACKGROUND_Y_PADDING:
            self.pos.top = BACKGROUND_Y_PADDING


# Create the player object
p = GameObject(player, PLAYER_STARTING_POS_X, PLAYER_STARTING_POS_Y, 3)

# Get clock and start game loop
clock = pygame.time.Clock()
screen.blit(scaled_background, (BACKGROUND_X_PADDING, BACKGROUND_Y_PADDING))
while True:
    screen.blit(
        scaled_background,
        p.pos,
        (
            p.pos.x - BACKGROUND_X_PADDING + 1,
            p.pos.y - BACKGROUND_Y_PADDING,
            p.pos.width,
            p.pos.height,
        ),
    )
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        p.move(up=True)
    if keys[pygame.K_DOWN]:
        p.move(down=True)
    if keys[pygame.K_LEFT]:
        p.move(left=True)
    if keys[pygame.K_RIGHT]:
        p.move(right=True)
    if keys[pygame.K_ESCAPE]:
        sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    screen.blit(p.asset, p.pos)
    pygame.display.update()
    clock.tick(60)
