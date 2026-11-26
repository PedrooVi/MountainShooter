class Entity:
    def __init__(self, name, image, position):
        self.name = name
        self.image = image
        self.surf = image
        self.rect = self.image.get_rect(topleft=position)
        self.speed = 0

    def update(self, dt):
        pass

    def hitbox(self):
        return self.rect.inflate(-self.rect.width * 0.2, -self.rect.height * 0.15)
