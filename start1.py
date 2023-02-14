import pygame
from os.path import join
pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 850, 550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SHOOTERS")
ICON = pygame.image.load(join("images", "spaceship.png"))
pygame.display.set_icon(ICON)

BG = pygame.image.load(join("images", "milky-way.jpg"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))
PLAYER_SHIP_1 = pygame.image.load(join("images", "spaceship1.png"))
PLAYER_SHIP_1 = pygame.transform.scale(PLAYER_SHIP_1, (100, 110))
PLAYER_SHIP_1 = pygame.transform.rotate(PLAYER_SHIP_1, -90)
LASER_RED = pygame.image.load(join("images", "pixel_laser_red.png"))
LASER_RED = pygame.transform.rotate(LASER_RED, 90)
PLAYER_SHIP_2 = pygame.image.load(join("images", "spaceship2.png"))
PLAYER_SHIP_2 = pygame.transform.scale(PLAYER_SHIP_2, (100, 100))
PLAYER_SHIP_2 = pygame.transform.rotate(PLAYER_SHIP_2, 180)
LASER_BLUE = pygame.image.load(join("images", "pixel_laser_blue.png"))
LASER_BLUE = pygame.transform.rotate(LASER_BLUE, 270)

class Player:
    COOLDOWN = 30
    def __init__(self, x, y, ship_img, laser_img, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = ship_img
        self.laser_img = laser_img
        self.mask = pygame.mask.from_surface(ship_img)
        self.lasers = []
        self.cool_down_counter = 0
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Lasers(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(WIDTH):
                self.lasers.remove(laser)
            elif laser.collison(obj):
                self.lasers.remove(laser)
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    def get_height(self):
        return self.ship_img.get_height()
    def get_width(self):
        return self.ship_img.get_width()

class Lasers:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.x += vel
    def off_screen(self, width):
        return self.x < width and self.x >= 0
    def collison(self, obj):
        return collide(self, obj)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None    

score1 = 0
score2 = 0
player_vel = 5
laser_vel = 5
main_font = pygame.font.SysFont("comicsans", 40)
player1 = Player(50 , HEIGHT/2 - 25, PLAYER_SHIP_1, LASER_RED)
player2 = Player(WIDTH - 150, HEIGHT/2 - 25, PLAYER_SHIP_2, LASER_BLUE)

def player_move(key):
    if key[pygame.K_w] and player1.y - player_vel > 0:
        player1.y -= player_vel
    if key[pygame.K_s] and player1.y + player_vel + player1.get_height() < HEIGHT:
        player1.y += player_vel
    if key[pygame.K_i] and player2.y - player_vel > 0:
        player2.y -= player_vel
    if key[pygame.K_k] and player2.y + player_vel + player2.get_height() < HEIGHT:
        player2.y += player_vel
    if key[pygame.K_SPACE]:
        player1.shoot()
    if key[pygame.K_0]:
        player2.shoot()
        
def draw_window():
    WIN.blit(BG, (0,0))
    score1_label = main_font.render(f"SCORE : {score1}", 1, (255,255,255))
    score2_label = main_font.render(f"SCORE : {score2}", 1, (255,255,255))
    WIN.blit(score1_label, (10, 10))
    WIN.blit(score2_label, (WIDTH - score2_label.get_width() - 10, 10))
    player1.draw(WIN)
    player2.draw(WIN)
    pygame.display.update()

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()

    while run:
        draw_window()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
    key_pressed = pygame.key.get_pressed()
    player_move(key_pressed)        
    player1.move_lasers(laser_vel, player2)    
    player2.move_lasers(laser_vel, player1)    
    
    pygame.quit()

if __name__=="__main__":
    main()