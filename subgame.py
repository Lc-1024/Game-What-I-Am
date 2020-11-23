import pygame
import random
import sys
from pygame.locals import *

help_size = (555, 12, 30, 16)
help_color  = [(220,220,220), (250,250,250)]
def show_help(play_sur_face, clock, place):
    pygame.draw.rect(play_sur_face, pygame.Color(255,255,255), Rect(0, 0, 600, 600))
    font = pygame.font.SysFont("simhei", 20) # 20 -- 字体大小
    tip_font = pygame.font.SysFont("simhei", 12)
    sentences = [["想要进入人体，你必须突破第一道防线", "按上键/空格或单击任意位置往上跳", "从皮肤的缝隙中进入人体吧", "小心重力会把你往下拉", "注意不要撞墙了哦"],
                 ["看呐，是食物，快吃了它", "小心避开那些免疫细胞", "被他们抓到，你的后代会被消灭", "但是吃到东西你就会增长", "努力吧，吃到一定数量后会通关", "按ESC可以逃跑，但是有的后代会死"],
                 ["好多食物啊", "四处走走，它们都可以吃", "小心别被免疫细胞抓住，它们会消灭你的后代", "吃完大部分食物后通关，你也可以剩一些不吃的", "按ESC可以逃跑，但是有的后代会死"], 
                 ["收集所有的钥匙吧", "收集完大部分钥匙之后大门会打开", "走出大门，你就能到另一个地方", "同样的，要小心那些免疫细胞", "要保护好你的后代呢"]]
    for i, sen in enumerate(sentences[place]):
        play_sur_face.blit(font.render(sen, True, (0,0,0)), (20, 30+i*40))
    play_sur_face.blit(tip_font.render("按任意键返回", True, (0,0,0)), (250, 550))
    pygame.display.flip()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                return
            elif event.type == MOUSEBUTTONDOWN:
                return

# 颜色可以自定义
germ_color = (0, 158, 128)
keys_color = (0, 0, 255)
food_color = (255, 255, 0)
cell_color = (0, 0, 0)
back_color = (255, 235, 215)
wall_color = (200, 0, 0)
bar_color  = (238, 207, 161)

# 第一个小游戏，细菌从皮肤破损中进入人体
def first_game(play_sur_face):
    pygame.init()
    time = 1000
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
    bird = [100, 200]
    size = [20, 10]
    bar_size = [100, 400]

    CREATE_ENEMY_EVENT = pygame.USEREVENT
    pygame.time.set_timer(CREATE_ENEMY_EVENT, 3500)
    pygame.display.update()

    bg = pygame.transform.scale(pygame.image.load("image/first.jpg"), (5500, 600))
    bd = pygame.image.load("image/germ.bmp")
    bar_up = pygame.image.load("image/photo.png")
    bar_down = pygame.image.load("image/photo.png")
    play_sur_face.blit(bg, (-time, 0))
    play_sur_face.blit(bd, (bird[0], bird[1]))
    pygame.display.update()
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("simhei", 12)
    clock.tick(3)
    while True:
        clock.tick(60)
        time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == CREATE_ENEMY_EVENT:
                U = random.randint(0, 255) - bar_size[1]
                D = U + bar_size[1] + random.randint(230, int(350-time/50))
                bar.append([600, U, D])
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
                    show_help(play_sur_face, clock, 0)
                else:
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
                elif event.key == pygame.K_UP or event.key == pygame.K_SPACE:
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
                elif event.key == ord('h'):
                    show_help(play_sur_face, clock, 0)

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

        play_sur_face.blit(bg, (-time, 0))
        for i in range(len(bar)):
            pygame.draw.rect(play_sur_face, bar_color, (bar[i][0], bar[i][1], bar_size[0], bar_size[1]))
            pygame.draw.rect(play_sur_face, bar_color, (bar[i][0], bar[i][2], bar_size[0], bar_size[1]))
            if time < 2000:
                bar[i][0] -= 5
            elif time < 3000:
                bar[i][0] -= 6
            elif time < 4000:
                bar[i][0] -= 7
            else:
                bar[i][0] -= 8
            bar_size[0] = 100 + int((time - 1000) * 80 / 3900)
            if i == len(bar)-1 and bar[0][0] < -bar_size[0]:
                bar.remove(bar[0])

        mouse = pygame.mouse.get_pos()
        if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
            pygame.draw.rect(play_sur_face, help_color[1], help_size)
        else:
            pygame.draw.rect(play_sur_face, help_color[0], help_size)
        play_sur_face.blit(font.render("Help", True, (0,0,0)), (help_size[0]+3, help_size[1]+1))
        # pygame.draw.rect(play_sur_face, (0,0,0), (bird[0], bird[1], 20,20))
        play_sur_face.blit(bd, (bird[0], bird[1]))
        pygame.display.update()

        for b in bar:
            if bird[0]+size[0] >= b[0] and bird[0] <= b[0]+bar_size[0] and not (bird[1]+5+size[1] <= b[2] and bird[1]+5 >= b[1]+bar_size[1]):
                return 1

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
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
                    show_help(play_sur_face, clock, 1)
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
                if event.key == ord('h'):
                    show_help(play_sur_face, clock, 1)
        
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
        mouse = pygame.mouse.get_pos()
        if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
            pygame.draw.rect(play_sur_face, help_color[1], help_size)
        else:
            pygame.draw.rect(play_sur_face, help_color[0], help_size)
        for c in cell:
            pygame.draw.rect(play_sur_face, cell_color, (c[0]+1, c[1]+1, 18, 18))
        for f in food:
            pygame.draw.rect(play_sur_face, food_color, (f[0]+1, f[1]+1, 18, 18))
        play_sur_face.blit(pygame.image.load("image/germ.bmp"), (germ[0], germ[1]))
        play_sur_face.blit(font.render("Help", True, (0,0,0)), (help_size[0]+3, help_size[1]+1))
        play_sur_face.blit(font.render("数量："+str(num), True, (0, 0, 0)), (10, 10))
        pygame.display.flip()

    return level+1, num

# 吃豆子
def beens_game(play_sur_face, level, num):
    def gen_germ():
        while True:
            pos = [random.randint(1, 29), random.randint(1, 29)]
            if w[pos[0]][pos[1]] == 0:
                pos = [pos[0]*20-10, pos[1]*20-10]
                break
        return pos
    def gen_cell():
        while True:
            pos = [random.randint(1, 29), random.randint(1, 29)]
            if w[pos[0]][pos[1]] == 0 and pos[0]*20-10 != germ[0] and pos[1]*20-10 != germ[1]:
                pos = [pos[0]*20-10, pos[1]*20-10]
                break
        return pos
    # 墙
    wall, w = beens_page()
    germ = gen_germ()
    time = 0
    di = ''
    dx = [[20,0], [-20,0], [0,-20], [0,20]]
    # 保卫细胞
    cell = []
    food = []
    for i in range(2*level+2):
        cell.append(gen_cell())
    for i in range(31):
        for j in range(31):
            if w[i][j] == 0:
                food.append([i*20-10, j*20-10])
    food.remove(germ)

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
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
                    show_help(play_sur_face, clock, 2)
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
                if event.key == ord('h'):
                    show_help(play_sur_face, clock, 1)

        # 如果前进方向没有墙主角可以运动
        if di != '' and time % 10 == 0:
            tmp = [germ[0]+dx[di][0], germ[1]+dx[di][1]]
            if tmp not in wall:
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
        for w in wall:
            pygame.draw.rect(play_sur_face, wall_color, Rect(w[0], w[1], 20, 20)) 

        # 判断每个保卫细胞的状态
        for i in range(len(cell)):
            if time % (20-level) != 0:
                break
            d = random.randint(0,3)
            tmp = [cell[i][0]+dx[d][0], cell[i][1]+dx[d][1]]
            if tmp not in wall:
                cell[i] = tmp

        mouse = pygame.mouse.get_pos()
        if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
            pygame.draw.rect(play_sur_face, help_color[1], help_size)
        else:
            pygame.draw.rect(play_sur_face, help_color[0], help_size)
        for f in food:
            pygame.draw.rect(play_sur_face, food_color, (f[0]+6, f[1]+6, 8, 8))
        for c in cell:
            pygame.draw.rect(play_sur_face, cell_color, (c[0], c[1], 20, 20))
        play_sur_face.blit(font.render("Help", True, (0,0,0)), (help_size[0]+3, help_size[1]+1))
        play_sur_face.blit(font.render("数量："+str(num), True, (0, 0, 0)), (10, 10))
        play_sur_face.blit(pygame.image.load("image/germ.bmp"), (germ[0], germ[1]))
        pygame.display.flip()

    return

# 细菌传播，从a到b
def move(play_sur_face, a, b, num):
    def gen():
        while True:
            pos = [random.randint(1, 29)*20-10, random.randint(1, 29)*20-10]
            if germ[0] == pos[0] and germ[1] == pos[1]:
                continue
            elif pos in wall or pos in keys:
                continue
            else:
                break
        return pos
    # 墙
    germ, door, wall = move_page(a, b)
    time = 0
    di = ''
    dx = [[20,0], [-20,0], [0,-20], [0,20]]
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
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
                    show_help(play_sur_face, clock, 3)
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
                if event.key == ord('h'):
                    show_help(play_sur_face, clock, 1)

        # 如果前进方向没有墙主角可以运动
        if di != '' and time % 10 == 0:
            tmp = [germ[0]+dx[di][0], germ[1]+dx[di][1]]
            if tmp not in wall:
                germ = tmp
            if germ in cell and num > 1:
                num = int(0.85 * num)
            # di = ''
            if germ in keys:
                keys.remove(germ)
                if len(keys) == 0:
                    wall.remove(door)
            if germ == door:
                return b, num

        # 改变每个保卫细胞的状态
        for i in range(len(cell)):
            if time % 15 != 0:
                break
            d = random.randint(0,3)
            tmp = [cell[i][0]+dx[d][0], cell[i][1]+dx[d][1]]
            if tmp not in wall:
                cell[i] = tmp

        play_sur_face.fill(back_color)
        pygame.draw.rect(play_sur_face, keys_color, Rect(door[0], door[1], 20, 20)) 
        for w in wall:
            pygame.draw.rect(play_sur_face, wall_color, Rect(w[0], w[1], 20, 20)) 
        mouse = pygame.mouse.get_pos()
        if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
            pygame.draw.rect(play_sur_face, help_color[1], help_size)
        else:
            pygame.draw.rect(play_sur_face, help_color[0], help_size)
        for k in keys:
            pygame.draw.rect(play_sur_face, keys_color, (k[0]+6, k[1]+3, 8, 12))
        for c in cell:
            pygame.draw.rect(play_sur_face, cell_color, (c[0], c[1], 20, 20))
        play_sur_face.blit(pygame.image.load("image/germ.bmp"), (germ[0], germ[1]))

        play_sur_face.blit(font.render("Help", True, (0,0,0)), (help_size[0]+3, help_size[1]+1))
        play_sur_face.blit(font.render("数量："+str(num), True, (0, 0, 0)), (10, 10))
        pygame.display.flip()

    return a, num


def getNeighbours(wall, node):
    di = [[0,1], [1,0], [0,-1], [-1,0]]
    n = []
    for i in range(4):
        if 0 < node[0]+2*di[i][0] < 30 and 0 < node[1]+2*di[i][1] < 30 and wall[node[0]+di[i][0]][node[1]+di[i][1]] != 0 and wall[node[0]+2*di[i][0]][node[1]+2*di[i][1]] != 0:
            n.append([node[0]+di[i][0], node[1]+di[i][1]])
            n.append([node[0]+2*di[i][0], node[1]+2*di[i][1]])
    return n

def beens_page():
    wall = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1
            , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1
            , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
            , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
            , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
            , 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
            , 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
            1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    node = [1,1]
    wall[1][1] = 0
    stack = []
    while True:
        n = getNeighbours(wall, node)
        if len(n) == 0:
            if len(stack) == 0:
                break
            node = stack[0]
            stack.remove(stack[0])
        else:
            i = 2*random.randint(0, int(len(n)/2-1))
            wall[n[i][0]][n[i][1]] = 0
            wall[n[i+1][0]][n[i+1][1]] = 0
            node = n[i+1]
            stack.append(n[i+1])
    for i in range(10):
        while True:
            p = [random.randint(1,29), random.randint(1,29)]
            if wall[p[0]][p[1]] == 1:
                wall[p[0]][p[1]] = 0
                break
    w = []
    for i in range(31):
        for j in range(31):
            if wall[i][j] == 1:
                w.append([20*i-10,20*j-10])
    return w, wall

def move_page(a, b):
    germ = []
    door = []
    if (b != 5 and a < b) or (a == 5):
        germ = [10, 10]
        door = [570, 590]
    else:
        germ = [570, 570]
        door = [10, -10]
    w = []
    wall = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1
        , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        , 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1
        , 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    node = [1,1]
    wall[1][1] = 0
    stack = []
    while True:
        n = getNeighbours(wall, node)
        if len(n) == 0:
            if len(stack) == 0:
                break
            node = stack[0]
            stack.remove(stack[0])
        else:
            i = 2*random.randint(0, int(len(n)/2-1))
            wall[n[i][0]][n[i][1]] = 0
            wall[n[i+1][0]][n[i+1][1]] = 0
            node = n[i+1]
            stack.append(n[i+1])
    for i in range(31):
        for j in range(31):
            if wall[i][j] == 1:
                w.append([20*i-10,20*j-10])
    return germ, door, w