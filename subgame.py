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

# 子弹类
class bullet:
    def __init__(self, x0, y0, d0):
        self.x = x0
        self.y = y0
        self.d = d0
        self.alive = True
        self.time = 0  # 为了防止子弹飞太快，只有在time为10的倍数的时候才会移动
        # 判断是否在墙内生成
        if [x0, y0] in Wall:
            self.alive = False


class things:
    def __init__(self, x0, y0):
        self.x = x0
        self.y = y0

'''
# TODO 设计游戏
# 第一关，进入人体，如果输入2，则表示进入躯干，如果输入3，则表示进入头部    
def first_game(t):



'''


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
    bd = pygame.image.load("d.png")
    bar_up = pygame.image.load("photo.png")
    bar_down = pygame.image.load("photo.png")
    clock = pygame.time.Clock()

    clock.tick(1)
    while True:
        clock.tick(60)
        time += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == CREATE_ENEMY_EVENT:
                U = random.randint(0, 255) - bar_size[1]
                D = U + bar_size[1] + random.randint(200, int(350-time/50))
                bar.append([600, U, D])

            elif event.type == pygame.KEYDOWN:
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

        bird[1] += round(V * t + 0.5 * A * t * t)
        V += A * t

        if (bird[1] >= 650) or (bird[1] <= -50):
            return False
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
                return False

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
            return


# 贪吃蛇
def snake_game(play_sur_face, a):
    class Point():
        row = 0
        clo = 0

        def __init__(self, row, clo):
            self.row = row
            self.clo = clo

        def copy(self):
            return Point(row=self.row, clo=self.clo)

    # 初始化
    pygame.init()
    width = 600
    hight = 600

    ROW = 30
    CLO = 40

    # 蛇头坐标定在中间
    head = Point(row=int(ROW / 2), clo=int(CLO / 2))
    # 初始化蛇身的元素数量
    snake = [
        Point(row=head.row, clo=head.clo + 1),
        Point(row=head.row, clo=head.clo + 2),
        Point(row=head.row, clo=head.clo + 3)
    ]

    # 生成食物并且不让食物生成在蛇的身体里面
    def gen_food():
        while 1:
            position = Point(row=random.randint(0, ROW - 1), clo=random.randint(0, CLO - 1))
            is_coll = False
            if head.row == position.row and head.clo == position.clo:
                is_coll = True
            for body in snake:
                if body.row == position.row and body.clo == position.clo:
                    is_coll = True
                    break
            if not is_coll:
                break
        return position

    # 定义坐标
    # 蛇头颜色可以自定义
    head_color = (0, 158, 128)
    # 食物坐标
    snakeFood = gen_food()
    # 食物颜色
    snakeFood_color = (255, 255, 0)
    snake_color = (200, 147, 158)

    # 需要执行很多步画图操作 所以定义一个函数
    def rect(point, color):
        # 定位 画图需要left和top
        left = point.clo * width / CLO
        top = point.row * hight / ROW
        # 将方块涂色
        pygame.draw.rect(play_sur_face, color, (left, top, width / CLO, hight / ROW))

    quit = True
    # 设置帧频率
    clock = pygame.time.Clock()
    while quit:
        # 处理帧频 锁帧
        clock.tick(30)
        # pygame.event.get()获取当前事件的队列 可以同时发生很多事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = False
            elif event.type == pygame.KEYDOWN:
                # 这里小细节蛇不可以直接左右上下 要判断当前是在什么状态下前行
                if event.key == 273 or event.key == 119:
                    if direct == 'left' or direct == 'right':
                        direct = 'top'
                if event.key == 274 or event.key == 115:
                    if direct == 'left' or direct == 'right':
                        direct = 'bottom'
                if event.key == 276 or event.key == 97:
                    if direct == 'top' or direct == 'bottom':
                        direct = 'left'
                if event.key == 275 or event.key == 100:
                    if direct == 'top' or direct == 'bottom':
                        direct = 'right'
        # 吃东西
        eat = (head.row == snakeFood.row and head.clo == snakeFood.clo)

        # 处理蛇的身子
        # 1.把原来的头插入到snake的头上
        # 2.把最后一个snake删掉
        if eat:
            snakeFood = Point(row=random.randint(0, ROW - 1), clo=random.randint(0, CLO - 1))
        snake.insert(0, head.copy())
        if not eat:
            snake.pop()

        # 移动一下
        if direct == 'left':
            head.clo -= 1
        if direct == 'right':
            head.clo += 1
        if direct == 'top':
            head.row -= 1
        if direct == 'bottom':
            head.row += 1
        dead = False
        if head.clo < 0 or head.row < 0 or head.clo >= CLO or head.row >= ROW:
            dead = True
        for body in snake:
            if head.clo == body.clo and head.row == body.row:
                dead = True
                break
        if dead:
            print('Game Over')
            quit = False
        # 背景画图
        pygame.draw.rect(play_sur_face, (245, 135, 155), (0, 0, width, hight))

        # 蛇头
        rect(head, head_color)
        # 绘制食物
        rect(snakeFood, snakeFood_color)
        # 绘制蛇的身子
        for body in snake:
            rect(body, snake_color)

        # 交还控制权
        pygame.display.flip()

# 吃豆人
def beens_game():
    # 第一关的初始化
    # 主角
    x, y = 0, 30
    life = 3
    d = 'd'
    state = {'d': pygame.image.load("d.png"), 'a': pygame.image.load("a.png"), 'w': pygame.image.load("w.png"), 's': pygame.image.load("s.png")}

    # 墙
    Wall = [
        [0, 0], [30, 0], [60, 0], [90, 0], [120, 0], [150, 0], [180, 0], [210, 0], [240, 0], [270, 0], [300, 0], [330, 0], [360, 0], [390, 0], [420, 0], [450, 0], [480, 0], [510, 0], [540, 0], [570, 0], 
        [-30, 30], [60, 30], [180, 30], [300, 30], [420, 30], [510, 30], [570, 30],
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

    # 小怪
    Master = [master(480, 90, 'w'), master(270, 270, 'w'), master(210, 540, 'w'), master(90, 420, 'w')]
    m_state = {'d': pygame.image.load("m_d.png"), 'a': pygame.image.load("m_a.png"), 'w': pygame.image.load("m_w.png"), 's': pygame.image.load("m_s.png")}

    # 子弹
    Bullet = []
    b_state = pygame.image.load("b.png")

    # 钥匙
    Key = [things(30, 480)]
    k_state = pygame.image.load("key.png")

    # 宝藏
    Treasure = [things(540, 30), things(30, 210), things(270, 330)]
    t_state = pygame.image.load("treasure.png")
    take_treasure = 0

    # 行进方向
    walk = {'d': [30, 0], 'a': [-30, 0], 's': [0, 30], 'w': [0, -30]}

    # 设置时钟
    clock = pygame.time.Clock()

    # 第一关开始
    while True:
        clock.tick(60)                      # 每秒执行60次
        change_direction = ""               # 将参数初始化
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 判断键盘事件
                if event.key == K_RIGHT or event.key == ord('d'):
                    change_direction = 'd'
                if event.key == K_LEFT or event.key == ord('a'):
                    change_direction = 'a'
                if event.key == K_UP or event.key == ord('w'):
                    change_direction = "w"
                if event.key == K_DOWN or event.key == ord('s'):
                    change_direction = 's'
                # 按下空格键发射子弹
                if event.key == ord(' '):
                    Bullet.append(bullet(x+walk[d][0], y+walk[d][1], d))
                if event.key == K_ESCAPE:  # 按esc键
                    pygame.quit()
                    sys.exit()

        # 如果前进方向没有墙主角可以运动
        if change_direction == "d":
            d = change_direction
            if [x+30, y] not in Wall:
                x += 30
        if change_direction == "a":
            d = change_direction
            if [x-30, y] not in Wall:
                x -= 30
        if change_direction == "w":
            d = change_direction
            if [x, y-30] not in Wall:
                y -= 30
        if change_direction == "s":
            d = change_direction
            if [x, y+30] not in Wall:
                y += 30

        # 通关
        if x == 600 and y == 540:
            break

        # 开始绘制，背景为全黑，将墙画入地图
        play_sur_face.fill(pygame.Color(255, 255, 255))
        # 开始画墙
        for w in Wall:
            pygame.draw.rect(play_sur_face, pygame.Color(255, 0, 0), Rect(w[0], w[1], 30, 30)) 
        # 出口大门
        if len(Key) > 0:
            pygame.draw.rect(play_sur_face, pygame.Color(255, 255, 0), Rect(570, 540, 30, 30)) 

        # 判断是否吃到钥匙
        for k in Key:
            if k.x == x and k.y == y:
                Key.remove(k)
                if len(Key) == 0:
                    Wall.remove([570, 540])
            else:
                play_sur_face.blit(k_state, (k.x-17, k.y-15))

        # 判断是否吃到宝藏
        for t in Treasure:
            if t.x == x and t.y == y:
                Treasure.remove(t)
                take_treasure += 1
            else:
                play_sur_face.blit(t_state, (t.x-17, t.y-15))

        # 显示宝藏和钥匙数量
        text_surface = pygame.font.SysFont("", 20).render("Key: {lk}".format(lk = 1-len(Key)), True, (0, 0, 0))
        play_sur_face.blit(text_surface, (10, 570))
        text_surface = pygame.font.SysFont("", 20).render("Treasure: {lt}".format(lt = take_treasure), True, (0, 0, 0))
        play_sur_face.blit(text_surface, (10, 585))

        # 判断每个子弹的状态
        for b in Bullet:
            b.fly()
            # 运动之前判断是否射到小怪
            for m in Master:
                if b.x == m.x and b.y == m.y:
                    m.life -= 1
                    b.alive = False
                    continue
            
            b.time += 1
            if b.time % 10 != 0:
                continue
            
            if [b.x+walk[b.d][0], b.y+walk[b.d][1]] not in Wall:
                b.x += walk[b.d][0]
                b.y += walk[b.d][1]
            else:
                b.alive = False
                continue

            # 运动之后判断是否射到小怪
            for m in Master:
                if b.x == m.x and b.y == m.y:
                    m.life -= 1
                    b.alive = False
                    continue
            # 如果子弹还未消失，则运动
            if b.alive:
                play_sur_face.blit(b_state, (b.x-17, b.y-15))
            else:
                Bullet.remove(b)

        # 判断每个小怪的状态
        for m in Master:
            # 如果小怪还活着
            if m.life > 0:
                m.time += 1
            if m.time % 30 != 0:
                continue

            # 如果小怪此前已经静止，则赋予新的方向
            if m.walking == False:
                m.d = random.choice('wsad')
            # 小怪面对的方向没有墙则可以运动
            if [m.x+walk[m.d][0], m.y+walk[m.d][1]] not in Wall:
                m.walking = True
                # 但是如果小怪前进后可以打到主角则攻击，并不运动
                if m.x+walk[m.d][0] == x and m.y+walk[m.d][1] == y:
                    m.attack = True
                    m.walking = False
            else:
                m.walking = False
            
            # 如果小怪现在可以攻击，则攻击
            if m.x == x and m.y == y:
                m.attack = True
                m.walking = False

            # 小怪可以的情况下则运动
            if m.walking:
                m.x += walk[m.d][0]
                m.y += walk[m.d][1]

            play_sur_face.blit(m_state[m.d], (m.x-15, m.y-15))
            if m.attack:
                life -= 1
                if life == 0:
                    show_lose()
                m.attack = False
            else:
                Master.remove(m)

        # 最后显示主角的位置
        play_sur_face.blit(state[d], (x-10, y-25))
        # 显示生命值
        text_surface = pygame.font.SysFont("", 20).render("Life: {l}".format(l = life), True, (0, 0, 0))
        play_sur_face.blit(text_surface, (10, 10))
        pygame.display.flip()

    return





# 细菌传播，从a到b
def move(play_sur_face, a, b):
    # 第一关的初始化
    # 主角
    x, y = 0, 30
    life = 3
    d = 'd'
    state = {'d': pygame.image.load("d.png"), 'a': pygame.image.load("a.png"), 'w': pygame.image.load("w.png"), 's': pygame.image.load("s.png")}

    # 墙
    Wall = [
        [0, 0], [30, 0], [60, 0], [90, 0], [120, 0], [150, 0], [180, 0], [210, 0], [240, 0], [270, 0], [300, 0], [330, 0], [360, 0], [390, 0], [420, 0], [450, 0], [480, 0], [510, 0], [540, 0], [570, 0], 
        [-30, 30], [60, 30], [180, 30], [300, 30], [420, 30], [510, 30], [570, 30],
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

    # 小怪
    Master = [master(480, 90, 'w'), master(270, 270, 'w'), master(210, 540, 'w'), master(90, 420, 'w')]
    m_state = {'d': pygame.image.load("m_d.png"), 'a': pygame.image.load("m_a.png"), 'w': pygame.image.load("m_w.png"), 's': pygame.image.load("m_s.png")}

    # 子弹
    Bullet = []
    b_state = pygame.image.load("b.png")

    # 钥匙
    Key = [things(30, 480)]
    k_state = pygame.image.load("key.png")

    # 宝藏
    Treasure = [things(540, 30), things(30, 210), things(270, 330)]
    t_state = pygame.image.load("treasure.png")
    take_treasure = 0

    # 行进方向
    walk = {'d': [30, 0], 'a': [-30, 0], 's': [0, 30], 'w': [0, -30]}

    # 设置时钟
    clock = pygame.time.Clock()

    # 第一关开始
    while True:
        clock.tick(60)                      # 每秒执行60次
        change_direction = ""               # 将参数初始化
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 判断键盘事件
                if event.key == K_RIGHT or event.key == ord('d'):
                    change_direction = 'd'
                if event.key == K_LEFT or event.key == ord('a'):
                    change_direction = 'a'
                if event.key == K_UP or event.key == ord('w'):
                    change_direction = "w"
                if event.key == K_DOWN or event.key == ord('s'):
                    change_direction = 's'
                # 按下空格键发射子弹
                if event.key == ord(' '):
                    Bullet.append(bullet(x+walk[d][0], y+walk[d][1], d))
                if event.key == K_ESCAPE:  # 按esc键
                    pygame.quit()
                    sys.exit()

        # 如果前进方向没有墙主角可以运动
        if change_direction == "d":
            d = change_direction
            if [x+30, y] not in Wall:
                x += 30
        if change_direction == "a":
            d = change_direction
            if [x-30, y] not in Wall:
                x -= 30
        if change_direction == "w":
            d = change_direction
            if [x, y-30] not in Wall:
                y -= 30
        if change_direction == "s":
            d = change_direction
            if [x, y+30] not in Wall:
                y += 30

        # 通关
        if x == 600 and y == 540:
            break

        # 开始绘制，背景为全黑，将墙画入地图
        play_sur_face.fill(pygame.Color(255, 255, 255))
        # 开始画墙
        for w in Wall:
            pygame.draw.rect(play_sur_face, pygame.Color(255, 0, 0), Rect(w[0], w[1], 30, 30)) 
        # 出口大门
        if len(Key) > 0:
            pygame.draw.rect(play_sur_face, pygame.Color(255, 255, 0), Rect(570, 540, 30, 30)) 

        # 判断是否吃到钥匙
        for k in Key:
            if k.x == x and k.y == y:
                Key.remove(k)
                if len(Key) == 0:
                    Wall.remove([570, 540])
            else:
                play_sur_face.blit(k_state, (k.x-17, k.y-15))

        # 判断是否吃到宝藏
        for t in Treasure:
            if t.x == x and t.y == y:
                Treasure.remove(t)
                take_treasure += 1
            else:
                play_sur_face.blit(t_state, (t.x-17, t.y-15))

        # 显示宝藏和钥匙数量
        text_surface = pygame.font.SysFont("", 20).render("Key: {lk}".format(lk = 1-len(Key)), True, (0, 0, 0))
        play_sur_face.blit(text_surface, (10, 570))
        text_surface = pygame.font.SysFont("", 20).render("Treasure: {lt}".format(lt = take_treasure), True, (0, 0, 0))
        play_sur_face.blit(text_surface, (10, 585))

        # 判断每个子弹的状态
        for b in Bullet:
            b.fly()
            # 运动之前判断是否射到小怪
            for m in Master:
                if b.x == m.x and b.y == m.y:
                    m.life -= 1
                    b.alive = False
                    continue
            
            b.time += 1
            if b.time % 10 != 0:
                continue
            
            if [b.x+walk[b.d][0], b.y+walk[b.d][1]] not in Wall:
                b.x += walk[b.d][0]
                b.y += walk[b.d][1]
            else:
                b.alive = False
                continue

            # 运动之后判断是否射到小怪
            for m in Master:
                if b.x == m.x and b.y == m.y:
                    m.life -= 1
                    b.alive = False
                    continue
            # 如果子弹还未消失，则运动
            if b.alive:
                play_sur_face.blit(b_state, (b.x-17, b.y-15))
            else:
                Bullet.remove(b)

        # 判断每个小怪的状态
        for m in Master:
            # 如果小怪还活着
            if m.life > 0:
                m.time += 1
            if m.time % 30 != 0:
                continue

            # 如果小怪此前已经静止，则赋予新的方向
            if m.walking == False:
                m.d = random.choice('wsad')
            # 小怪面对的方向没有墙则可以运动
            if [m.x+walk[m.d][0], m.y+walk[m.d][1]] not in Wall:
                m.walking = True
                # 但是如果小怪前进后可以打到主角则攻击，并不运动
                if m.x+walk[m.d][0] == x and m.y+walk[m.d][1] == y:
                    m.attack = True
                    m.walking = False
            else:
                m.walking = False
            
            # 如果小怪现在可以攻击，则攻击
            if m.x == x and m.y == y:
                m.attack = True
                m.walking = False

            # 小怪可以的情况下则运动
            if m.walking:
                m.x += walk[m.d][0]
                m.y += walk[m.d][1]

            play_sur_face.blit(m_state[m.d], (m.x-15, m.y-15))
            if m.attack:
                life -= 1
                if life == 0:
                    show_lose()
                m.attack = False
            else:
                Master.remove(m)

        # 最后显示主角的位置
        play_sur_face.blit(state[d], (x-10, y-25))
        # 显示生命值
        text_surface = pygame.font.SysFont("", 20).render("Life: {l}".format(l = life), True, (0, 0, 0))
        play_sur_face.blit(text_surface, (10, 10))
        pygame.display.flip()

    return
