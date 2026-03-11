import pygame, time, sys, os

def path_getter(filename):
    if getattr(sys, 'frozen', False):

        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, filename)

def main(jsondata):
    global clock, name, width, height, filedata, gamedata, colorlist, displaysurf, bg_color, color, keys, text
    gamedata = {}
    filedata = jsondata

    # set the pygame vars.
    name = filedata['name']
    width = filedata['width']
    height = filedata['height']
    colorlist = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'orange': (255, 50, 0),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'purple': (100, 0, 255),
    'black': (0, 0, 0)
    }
    # pygame init
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption(name)
    displaysurf = pygame.display.set_mode((int(width), int(height)), 0, 32)
    keys = pygame.key.get_pressed()
    text = pygame.font.Font(path_getter(os.path.join('data', 'Font.ttf')), 70)

    # setting the bg color
    bg_color = filedata['bg']
    if 'color' in bg_color:
        color = colorlist[bg_color['color']]
    else:
        color = (255, 255, 255)



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        displaysurf.fill(color)
        pygame.display.update()
        clock.tick(60)

class Sprites:
    def __init__(self, type, name):
        self.type = type
        self.name = name
        if self.type == 'image':
            self.data = pygame.image.load(path_getter(os.path.join('data', str(filedata['sprites'][self.name]['data']))))
            self.rect = self.data.get_rect()
            self.rect.center = (width/2, height/2)
        elif self.type == 'text':
            self.data = text.render(filedata['sprites'][self.name]['data'], True, colorlist['black'])
            self.rect = self.data.get_rect()
            self.rect.center = (width/2, height/2)
        displaysurf.blit(self.data, self.rect)

    def set_xy(self, x, y):
        self.rect.center = (width/10*x, height/10*y)

    def if_key_pressed(self, key):
        return keys[key]
