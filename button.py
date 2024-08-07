import pygame

class Button():
    def __init__(self, x, y, image, scale):
        self.original_image = pygame.transform.smoothscale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.image = self.original_image.copy()
        self.original_rect = self.original_image.get_rect(topleft=(x, y))
        self.rect = self.original_rect.copy()
        self.clicked = False
        self.mouse_released = False
        self.scale = scale
        self.enlarged = False

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()
        click_sfx = pygame.mixer.Sound("sounds/click.mp3")

        # Check if mouse has been released
        if not self.mouse_released and pygame.mouse.get_pressed()[0] == 0:
            self.mouse_released = True

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if not self.enlarged:
                self.enlarge()
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and self.mouse_released:
                self.clicked = True
                self.mouse_released = False
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked:
                self.clicked = False
                action = True
                click_sfx.play()
        else:
            if self.enlarged:
                self.shrink()

        # Draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action

    def enlarge(self):
        self.image = pygame.transform.smoothscale(self.original_image, 
                                            (int(self.original_image.get_width() * 1.1), 
                                             int(self.original_image.get_height() * 1.1)))
        self.rect = self.image.get_rect(center=self.original_rect.center)
        self.enlarged = True

    def shrink(self):
        self.image = self.original_image.copy()
        self.rect = self.original_rect.copy()
        self.enlarged = False

    def reset(self):
        self.clicked = False
        self.mouse_released = False
