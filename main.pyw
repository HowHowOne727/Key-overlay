import pygame
import keyboard
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
H = int(config['Settings']["display_height"])
W = int(config['Settings']["display_width"])

pygame.init()
window = pygame.display.set_mode((H,W), pygame.SRCALPHA)
pygame.display.set_caption("key overlay")

green = (0,0,0)
gap = int(config['Settings']['gap'])
width = int((W-gap)/2)
l_width = int(config['Settings']['border_width'])
font_size = int(config['Settings']['font_size'])

fps = int(config['Settings']['fps'])
speed = int(config['Settings']['speed'])
ks1 = [[False, H-width]]
ks2 = [[False, H-width]]
k1 = config['Settings']['k1']
k2 = config['Settings']['k2']
run_bar_color = tuple(map(int, config['colors']['run_bar_color'].split(',')))
key_color = tuple(map(int, config['colors']['key_color'].split(',')))
font_color = tuple(map(int, config['colors']['font_color'].split(',')))
g_t = 1/(fps*speed) # time gap
k_count = [0,0]
x_zoom = 0.25
y_zoom = 0.1
zoom_t = int(3*speed)
zv1 = 1
zv2 = 1

def zoom(a, z = zoom_t):
    if a > z:
        return 1
    if a <= 0:
        return 0
    return a/z

def k_update():
    if keyboard.is_pressed(k1) == ks1[-1][0]:
        ks1[-1][1] += 1
    else:
        ks1.append([not ks1[-1][0] , 1])
        if ks1[-1][0]:
            k_count[0] += 1
    if keyboard.is_pressed(k2) == ks2[-1][0]:
        ks2[-1][1] += 1
    else:
        ks2.append([not ks2[-1][0] , 1])
        if ks2[-1][0]:
            k_count[1] += 1

d_window = pygame.Surface((H,W), pygame.SRCALPHA)
fading_surface = pygame.Surface((int((H-width)/2), W), pygame.SRCALPHA)
for i in range(int((H-width)/2)):
    pygame.draw.rect(fading_surface, (0,0,0,255-int(i/((H-width)/2)*255)), (i, 0, 1, W))

def vset(k):
    a = 1
    for i in k:
        if i[0]:
            a -= zoom(i[1])
        else:
            a += zoom(i[1])
        a = zoom(a, 1)
    return a

def draws():
    d_window.fill((0,0,0,0))
    locate = 0
    for i in range(len(ks1)-1, -1, -1):
        locate += ks1[i][1]
        if ks1[i][0]:
            pygame.draw.rect(d_window, run_bar_color, (H-width-locate, 0, ks1[i][1], width), border_radius=3)
        if (locate-ks1[i][1]) > (H-width):
            ks1.pop(0)
            break
    locate = 0
    for j in range(len(ks2)-1, -1, -1):
        locate += ks2[j][1]
        if ks2[j][0]:
            pygame.draw.rect(d_window, run_bar_color, (H-width-locate, width+gap , ks2[j][1], width), border_radius=3)
        if (locate-ks2[j][1]) > (H-width):
            ks2.pop(0)
            break
    d_window.blit(fading_surface, (0,0))

    zv1 = vset(ks1)
    zv2 = vset(ks2)
    pygame.draw.rect(window, key_color, (H-width, (1-zv1)*y_zoom*width*0.5           , ((1-x_zoom)+(x_zoom*zv1))*width, ((1-y_zoom)+(y_zoom*zv1))*width), border_radius=5)
    pygame.draw.rect(window, key_color, (H-width, (1-zv2)*y_zoom*width*0.5+width+gap , ((1-x_zoom)+(x_zoom*zv2))*width, ((1-y_zoom)+(y_zoom*zv2))*width), border_radius=5)
    pygame.draw.rect(d_window,(*green,zv1*255), (H-width+l_width , (1-zv1)*y_zoom*width*0.5+l_width          , ((1-x_zoom)+(x_zoom*zv1))*width-2*l_width , ((1-y_zoom)+(y_zoom*zv1))*width-2*l_width), border_radius=5)
    pygame.draw.rect(d_window,(*green,zv2*255), (H-width+l_width , (1-zv2)*y_zoom*width*0.5+l_width+width+gap, ((1-x_zoom)+(x_zoom*zv2))*width-2*l_width , ((1-y_zoom)+(y_zoom*zv2))*width-2*l_width), border_radius=5)
    window.blit(d_window, (0,0))
    

font = pygame.font.Font(None, font_size)
def draw_text():
    key_texts = [
        (k1, (int(H-(width/2)), int(width/4))),
        (k2, (int(H-(width/2)), int(width/4+width+gap))),
        (str(k_count[0]), (int(H-(width/2)), int(width/3*2))),
        (str(k_count[1]), (int(H-(width/2)), int(width/3*2+width+gap)))]
    rendered_texts = []
    for t, p in key_texts:
        rendered_text = font.render(t,True,font_color)
        texts_rect = rendered_text.get_rect(center = p)
        rendered_texts.append((rendered_text, texts_rect))
    for t,p in rendered_texts:
        window.blit(t,p)

bg = pygame.Surface((H,W))
bg.fill(green)
bg.convert()

clock = pygame.time.Clock()
run = True
st = time.time()
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for i in range(speed):
        k_update()
        et = time.time()
        time.sleep(g_t-(st-et))
        st = time.time()

    window.blit(bg, (0,0))
    draws()
    draw_text()
    pygame.display.flip()

pygame.quit()