import pytmx


class Map:
    def __init__(self, filename):
        self.map = pytmx.load_pygame(f'/{filename}') # здесь будем указывать путь к карте
        self.width = self.map.width
        self.height = self.map.height
        self.tile_size = self.map.tilewidth

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                image = self.map.get_tile_image(j, i, 0) # по сути: x, y и слой
                screen.blit(image, (j * self.tile_size, i * self.tile_size))

    def update(self):
        pass

