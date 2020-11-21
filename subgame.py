import pygame
import random
import sys
from pygame.locals import *

# 小怪类
class master:
    def __init__(self, x0, y0, d0):
        self.x = x0
        self.y = y0
        self.d = d0
        self.life = 3
        self.walking = False # 小怪是否在行走
        self.attack = False # 小怪是否在攻击主角
        self.time = 0 # 为了防止小怪走太快，只有在time为30的倍数的时候才会移动


# 第一个小游戏，细菌从皮肤破损中进入人体
def first_game(play_sur_face):
    pygame.init()
    time = 2000
    i = 0
    j = 0
    V = 0.0  # 速度
    A = 28.0  # 加速度
    t = 0.1  # 时间间隔
    I = -95   # 能量
    J = 0  # 起飞次数
    K = 0
    O = 1
    T = 0
    bar = []
    bird = [100, 300]
    size = [20, 20]
    bar_size = [100, 285]

    CREATE_ENEMY_EVENT = pygame.USEREVENT
    pygame.time.set_timer(CREATE_ENEMY_EVENT, 3500)
    pygame.display.update()

    bg = pygame.transform.scale(pygame.image.load("image/first.jpg"), (5500, 600))
    bd = pygame.image.load("image/d.png")
    bar_up = pygame.image.load("image/photo.png")
    bar_down = pygame.image.load("image/photo.png")
    play_sur_face.blit(bg, (-time, 0))
    play_sur_face.blit(bd, (bird[0]-20, bird[1]-20))
    pygame.display.update()
    clock = pygame.time.Clock()

    clock.tick(1)
    while True:
        clock.tick(60)
        time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == CREATE_ENEMY_EVENT:
                U = random.randint(0, 255) - bar_size[1]
                D = U + bar_size[1] + random.randint(200, int(350-time/50))
                bar.append([600, U, D])
            elif event.type == MOUSEBUTTONDOWN:
                clock.tick(26)
                O = random.randint(0, 3)
                if O != 0:
                    O = 1
                    T = 50
                else:
                    T = 100

                J += 1
                if J <= 39:
                    V = -95
                elif (J >= 28) and (J <= 50):
                    V = I
                    I += 0.2
                else:
                    V = I
                    I += 0.4
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:  
                    return 1
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    clock.tick(26)
                    O = random.randint(0, 3)
                    if O != 0:
                        O = 1
                        T = 50
                    else:
                        T = 100

                    J += 1
                    if J <= 39:
                        V = -95
                    elif (J >= 28) and (J <= 50):
                        V = I
                        I += 0.2
                    else:
                        V = I
                        I += 0.4
                elif event.key == ord('l'):
                    return 2

        bird[1] += round(V * t + 0.5 * A * t * t)
        V += A * t

        if (bird[1] >= 650) or (bird[1] <= -50):
            return 1
        j += 1
        if j == 3:
            i += 1
            j = 0

        if V <= -10:
            if i >= 4:
                i = 0

        elif (V > -10)and(V <= 55):
            if i >= 8:
                i = 4
        elif V > 55:
            i = 8

        for b in bar:
            if bird[0]+size[0] >= b[0] and bird[0] <= b[0]+bar_size[0] and not (bird[1]+size[1] <= b[2] and bird[1] >= b[1]+bar_size[1]):
                return 1

        play_sur_face.blit(bg, (-time, 0))
        for i in range(len(bar)):
            play_sur_face.blit(bar_up,   (bar[i][0], bar[i][1]))
            play_sur_face.blit(bar_down, (bar[i][0], bar[i][2]))
            if time < 3500:
                bar[i][0] -= 5
            if time >= 3500:
                bar[i][0] -= 7
            if i == len(bar)-1 and bar[0][0] < -bar_size[0]:
                bar.remove(bar[0])

        # pygame.draw.rect(play_sur_face, (0,0,0), (bird[0], bird[1], 20,20))
        play_sur_face.blit(bd, (bird[0]-20, bird[1]-20))
        pygame.display.update()

        if time >= 4900:
            return 2

# 细菌以贪吃蛇的形态在人体内吃东西增殖
def snake_game(play_sur_face, level, num):
    # 生成食物并且不让食物生成在细菌的身体里面
    def gen():
        while True:
            pos = [random.randint(0, 29)*20, random.randint(0, 29)*20]
            if germ[0] == pos[0] and germ[1] == pos[1]:
                continue
            else:
                break
        return pos

    germ = [200, 200]
    food = [gen()]
    cell = []
    dx = [[20,0], [-20,0], [0,-20], [0,20], [0,0]]

    # 颜色可以自定义
    germ_color = (0, 158, 128)
    food_color = (255, 255, 0)
    cell_color = (0, 0, 0)
    back_color = (255, 235, 215)

    font = pygame.font.SysFont("simhei", 12)
    play_sur_face.blit(font.render("数量："+str(num), True, (0, 0, 0)), (10, 10))

    clock = pygame.time.Clock()
    di = 0
    time = 0
    time_gap = 10 - level
    while True:
        # 处理帧频 锁帧
        clock.tick(60)
        time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return level, num
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    if num != 1:
                        num = int((0.8+0.02*level)*num)
                    return level, num
                if event.key == K_RIGHT or event.key == ord('d'):
                    di = 0
                if event.key == K_LEFT or event.key == ord('a'):
                    di = 1
                if event.key == K_UP or event.key == ord('w'):
                    di = 2
                if event.key == K_DOWN or event.key == ord('s'):
                    di = 3
                if event.key == ord('c'):
                    num *= 2
                if event.key == ord('l'):
                    num *= 100
                    return level+1, num
        
        # 移动一下
        if time % time_gap == 0:
            germ[0] += dx[di][0]
            germ[1] += dx[di][1]
            
        # 处理细菌数量
        if germ in food:
            food.remove(germ)
            food.append(gen())
            if num <= 10:
                num += 2
            elif num <= 20 * (100 ** level):
                num = int(num * 1.25)
            else:
                num = int(num * 1.1)

        if num >= 100 ** (level+1):
            return level+1, num
        while num / (100 ** level) * (level+1) >= 20 * len(cell):
            cell.append(gen())
        while num / (100 ** level) >= 20 * len(food):
            food.append(gen())

        # 判定越界：数量折半
        if germ[0] < 0 or germ[1] < 0 or germ[0] >= 600 or germ[1] >= 600:
            if num != 1:
                num = int(0.5*num)
            return level, num
        
        for i in range(len(cell)):
            if time % time_gap == i % (10 - level):
                tmp = random.randint(0, 4)
                if 0 <= cell[i][0] + dx[tmp][0] <= 580 and 0 <= cell[i][1] + dx[tmp][1] <= 580:
                     cell[i][0] += dx[tmp][0]
                     cell[i][1] += dx[tmp][1]

        # 判定被保卫细胞发现：数量：变为0.8
        if germ in cell and time % time_gap == 0:
            num = int((0.8+0.02*level)*num) + 1
        if num == 0:
            return level, 0

        pygame.draw.rect(play_sur_face, back_color, (0, 0, 600, 600))
        for c in cell:
            pygame.draw.rect(play_sur_face, cell_color, (c[0]+1, c[1]+1, 18, 18))
        for f in food:
            pygame.draw.rect(play_sur_face, food_color, (f[0]+1, f[1]+1, 18, 18))
        pygame.draw.rect(play_sur_face, germ_color, (germ[0], germ[1], 20, 20))
        play_sur_face.blit(font.render("数量："+str(num), True, (0, 0, 0)), (10, 10))
        pygame.display.flip()

    return level+1, num

# 吃豆子
def beens_game(play_sur_face, level, num):
    def gen():
        while True:
            pos = [random.randint(0, 19)*30, random.randint(0, 19)*30]
            if germ[0] == pos[0] and germ[1] == pos[1]:
                continue
            elif pos in Wall or pos in food:
                continue
            else:
                break
        return pos
    # 墙
    Wall = beens_page(level)
    germ = [210, 210]
    time = 0
    di = ''
    dx = [[30,0], [-30,0], [0,-30], [0,30], [0,0]]
    # 颜色可以自定义
    germ_color = (0, 158, 128)
    food_color = (255, 255, 0)
    cell_color = (0, 0, 0)
    back_color = (255, 235, 215)
    wall_color = (200, 0, 0)
    # 保卫细胞
    cell = []
    food = []
    for i in range(2*level+3):
        cell.append(gen())
    for i in range(400-220):
        food.append(gen())

    font = pygame.font.SysFont("simhei", 12)
    play_sur_face.blit(font.render("数量："+str(num), True, (0, 0, 0)), (10, 10))

    # 设置时钟
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    if num != 1:
                        num = int((0.8+0.02*level)*num)
                    return level, num
                if event.key == K_RIGHT or event.key == ord('d'):
                    di = 0
                if event.key == K_LEFT or event.key == ord('a'):
                    di = 1
                if event.key == K_UP or event.key == ord('w'):
                    di = 2
                if event.key == K_DOWN or event.key == ord('s'):
                    di = 3
                if event.key == ord('l'):
                    num *= 100
                    return level+1, num

        # 如果前进方向没有墙主角可以运动
        if di != '' and time % 10 == 0:
            tmp = [germ[0]+dx[di][0], germ[1]+dx[di][1]]
            if tmp not in Wall:
                germ = tmp
            if germ in cell and num > 1:
                num = int(0.85 * num)
            # di = ''
            if germ in food:
                food.remove(germ)
                num += 100 ** level
            if len(food) < 30:
                return level+1, num

        # 开始绘制地图
        play_sur_face.fill(back_color)
        for w in Wall:
            pygame.draw.rect(play_sur_face, wall_color, Rect(w[0], w[1], 30, 30)) 

        # 判断每个保卫细胞的状态
        for i in range(len(cell)):
            if time % (20-level) != 0:
                break
            d = random.randint(0,3)
            tmp = [cell[i][0]+dx[d][0], cell[i][1]+dx[d][1]]
            if tmp not in Wall:
                cell[i] = tmp

        for f in food:
            pygame.draw.rect(play_sur_face, food_color, (f[0]+10, f[1]+10, 10, 10))
        for c in cell:
            pygame.draw.rect(play_sur_face, cell_color, (c[0], c[1], 30, 30))
        pygame.draw.rect(play_sur_face, germ_color, (germ[0], germ[1], 30, 30))
        
        play_sur_face.blit(font.render("数量："+str(num), True, (0, 0, 0)), (10, 10))
        pygame.display.flip()

    return

# 细菌传播，从a到b
def move(play_sur_face, a, b, num):
    def gen():
        while True:
            pos = [random.randint(0, 19)*30, random.randint(0, 19)*30]
            if germ[0] == pos[0] and germ[1] == pos[1]:
                continue
            elif pos in Wall or pos in keys:
                continue
            else:
                break
        return pos
    # 墙
    germ, door, Wall = move_page(a, b)
    time = 0
    di = ''
    dx = [[30,0], [-30,0], [0,-30], [0,30], [0,0]]
    # 颜色可以自定义
    germ_color = (0, 158, 128)
    keys_color = (255, 255, 0)
    cell_color = (0, 0, 0)
    back_color = (255, 235, 215)
    wall_color = (200, 0, 0)
    # 保卫细胞
    cell = []
    keys = []
    for i in range(b+4):
        cell.append(gen())
    for i in range(b+1):
        keys.append(gen())

    font = pygame.font.SysFont("simhei", 12)
    play_sur_face.blit(font.render("数量："+str(num), True, (0, 0, 0)), (10, 10))

    # 设置时钟
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        time += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    if num != 1:
                        num = int(0.5*num)
                    return a, num
                if event.key == K_RIGHT or event.key == ord('d'):
                    di = 0
                if event.key == K_LEFT or event.key == ord('a'):
                    di = 1
                if event.key == K_UP or event.key == ord('w'):
                    di = 2
                if event.key == K_DOWN or event.key == ord('s'):
                    di = 3
                if event.key == ord('c'):
                    if len(keys) != 0:
                        germ = keys[0]
                    else:
                        germ = door
                if event.key == ord('l'):
                    return b, num

        # 如果前进方向没有墙主角可以运动
        if di != '' and time % 10 == 0:
            tmp = [germ[0]+dx[di][0], germ[1]+dx[di][1]]
            if tmp not in Wall:
                germ = tmp
            if germ in cell and num > 1:
                num = int(0.85 * num)
            di = ''
            if germ in keys:
                keys.remove(germ)
                if len(keys) == 0:
                    Wall.remove(door)
            if germ == door:
                return b, num

        # 改变每个保卫细胞的状态
        for i in range(len(cell)):
            if time % 15 != 0:
                break
            d = random.randint(0,3)
            tmp = [cell[i][0]+dx[d][0], cell[i][1]+dx[d][1]]
            if tmp not in Wall:
                cell[i] = tmp

        play_sur_face.fill(back_color)
        pygame.draw.rect(play_sur_face, keys_color, Rect(door[0], door[1], 30, 30)) 
        for w in Wall:
            pygame.draw.rect(play_sur_face, wall_color, Rect(w[0], w[1], 30, 30)) 
        for k in keys:
            pygame.draw.rect(play_sur_face, keys_color, (k[0]+10, k[1]+5, 10, 20))
        for c in cell:
            pygame.draw.rect(play_sur_face, cell_color, (c[0], c[1], 30, 30))
        pygame.draw.rect(play_sur_face, germ_color, (germ[0], germ[1], 30, 30))

        play_sur_face.blit(font.render("数量："+str(num), True, (0, 0, 0)), (10, 10))
        pygame.display.flip()

    return a, num

def beens_page(i):
    Wall = [
        [0, 0], [30, 0], [60, 0], [90, 0], [120, 0], [150, 0], [180, 0], [210, 0], [240, 0], [270, 0], [300, 0], [330, 0], [360, 0], [390, 0], [420, 0], [450, 0], [480, 0], [510, 0], [540, 0], [570, 0], 
        [0, 30], [60, 30], [180, 30], [300, 30], [420, 30], [510, 30], [570, 30],
        [0, 60], [60, 60], [120, 60], [180, 60], [240, 60], [270, 60], [300, 60], [360, 60], [420, 60], [450, 60], [510, 60], [570, 60], 
        [0, 90], [120, 90], [360, 90], [570, 90], 
        [0, 120], [60, 120], [90, 120], [120, 120], [150, 120], [180, 120], [240, 120], [300, 120], [330, 120], [360, 120], [390, 120], [420, 120], [450, 120], [480, 120], [510, 120], [540, 120], [570, 120], 
        [0, 150], [120, 150], [240, 150], [300, 150], [570, 150], 
        [0, 180], [30, 180], [60, 180], [120, 180], [180, 180], [210, 180], [240, 180], [270, 180], [300, 180], [360, 180], [390, 180], [420, 180], [450, 180], [480, 180], [510, 180], [540, 180], [570, 180], 
        [0, 210], [60, 210], [120, 210], [360, 210], [570, 210], 
        [0, 240], [60, 240], [120, 240], [180, 240], [210, 240], [240, 240], [300, 240], [330, 240], [360, 240], [390, 240], [420, 240], [450, 240], [480, 240], [510, 240], [570, 240], 
        [0, 270], [60, 270], [120, 270], [180, 270], [510, 270], [570, 270], 
        [0, 300], [60, 300], [120, 300], [180, 300], [240, 300], [270, 300], [300, 300], [330, 300], [360, 300], [390, 300], [420, 300], [450, 300], [510, 300], [570, 300], 
        [0, 330], [60, 330], [120, 330], [180, 330], [240, 330], [300, 330], [420, 330], [510, 330], [570, 330], 
        [0, 360], [60, 360], [120, 360], [180, 360], [240, 360], [360, 360], [480, 360], [510, 360], [570, 360], 
        [0, 390], [60, 390], [90, 390], [120, 390], [180, 390], [240, 390], [270, 390], [300, 390], [330, 390], [360, 390], [390, 390], [510, 390], [570, 390], 
        [0, 420], [180, 420], [240, 420], [450, 420], [480, 420], [510, 420], [570, 420], 
        [0, 450], [30, 450], [60, 450], [90, 450], [120, 450], [150, 450], [180, 450], [240, 450], [270, 450], [300, 450], [330, 450], [360, 450], [390, 450], [570, 450], 
        [0, 480], [60, 480], [180, 480], [210, 480], [240, 480], [300, 480], [510, 480], [570, 480], 
        [0, 510], [60, 510], [120, 510], [210, 510], [300, 510], [360, 510], [420, 510], [450, 510], [480, 510], [510, 510], [570, 510], 
        [0, 540], [120, 540], [150, 540], [360, 540], [510, 540], 
        [0, 570], [30, 570], [60, 570], [90, 570], [120, 570], [150, 570], [180, 570], [210, 570], [240, 570], [270, 570], [300, 570], [330, 570], [360, 570], [390, 570], [420, 570], [450, 570], [480, 570], [510, 570], [540, 570], [570, 570],
        [570, 540]
    ]
    return Wall

def move_page(a, b):
    germ = [30, 0]
    door = [570, 540]
    Wall = [
        [0, 0], [30, -30], [60, 0], [90, 0], [120, 0], [150, 0], [180, 0], [210, 0], [240, 0], [270, 0], [300, 0], [330, 0], [360, 0], [390, 0], [420, 0], [450, 0], [480, 0], [510, 0], [540, 0], [570, 0], 
        [0, 30], [60, 30], [180, 30], [300, 30], [420, 30], [510, 30], [570, 30],
        [0, 60], [60, 60], [120, 60], [180, 60], [240, 60], [270, 60], [300, 60], [360, 60], [420, 60], [450, 60], [510, 60], [570, 60], 
        [0, 90], [120, 90], [360, 90], [570, 90], 
        [0, 120], [60, 120], [90, 120], [120, 120], [150, 120], [180, 120], [240, 120], [300, 120], [330, 120], [360, 120], [390, 120], [420, 120], [450, 120], [480, 120], [510, 120], [540, 120], [570, 120], 
        [0, 150], [120, 150], [240, 150], [300, 150], [570, 150], 
        [0, 180], [30, 180], [60, 180], [120, 180], [180, 180], [210, 180], [240, 180], [270, 180], [300, 180], [360, 180], [390, 180], [420, 180], [450, 180], [480, 180], [510, 180], [540, 180], [570, 180], 
        [0, 210], [60, 210], [120, 210], [360, 210], [570, 210], 
        [0, 240], [60, 240], [120, 240], [180, 240], [210, 240], [240, 240], [300, 240], [330, 240], [360, 240], [390, 240], [420, 240], [450, 240], [480, 240], [510, 240], [570, 240], 
        [0, 270], [60, 270], [120, 270], [180, 270], [510, 270], [570, 270], 
        [0, 300], [60, 300], [120, 300], [180, 300], [240, 300], [270, 300], [300, 300], [330, 300], [360, 300], [390, 300], [420, 300], [450, 300], [510, 300], [570, 300], 
        [0, 330], [60, 330], [120, 330], [180, 330], [240, 330], [300, 330], [420, 330], [510, 330], [570, 330], 
        [0, 360], [60, 360], [120, 360], [180, 360], [240, 360], [360, 360], [480, 360], [510, 360], [570, 360], 
        [0, 390], [60, 390], [90, 390], [120, 390], [180, 390], [240, 390], [270, 390], [300, 390], [330, 390], [360, 390], [390, 390], [510, 390], [570, 390], 
        [0, 420], [180, 420], [240, 420], [450, 420], [480, 420], [510, 420], [570, 420], 
        [0, 450], [30, 450], [60, 450], [90, 450], [120, 450], [150, 450], [180, 450], [240, 450], [270, 450], [300, 450], [330, 450], [360, 450], [390, 450], [570, 450], 
        [0, 480], [60, 480], [180, 480], [210, 480], [240, 480], [300, 480], [510, 480], [570, 480], 
        [0, 510], [60, 510], [120, 510], [210, 510], [300, 510], [360, 510], [420, 510], [450, 510], [480, 510], [510, 510], [570, 510], 
        [0, 540], [120, 540], [150, 540], [360, 540], [510, 540], 
        [0, 570], [30, 570], [60, 570], [90, 570], [120, 570], [150, 570], [180, 570], [210, 570], [240, 570], [270, 570], [300, 570], [330, 570], [360, 570], [390, 570], [420, 570], [450, 570], [480, 570], [510, 570], [540, 570], [570, 570],
        [570, 540]
    ]
    return germ, door, Wall