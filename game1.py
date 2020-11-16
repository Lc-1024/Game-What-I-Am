import random
import pygame
import sys
from pygame.locals import *
import subgame

# 显示游戏失败界面
def show_lose():
    pygame.draw.rect(play_sur_face, pygame.Color(255, 255, 255), Rect(0, 0, 600, 600))
    play_sur_face.blit(pygame.image.load("lose.png") , (0, 0))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 判断键盘事件
                if event.key == K_ESCAPE:  # 按esc键
                    pygame.quit()
                    sys.exit()  # 退出游戏

# 等待玩家继续或退出
def wait_to_continue():
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:  
                    pygame.quit()
                    sys.exit()
                else:
                    return
            elif event.type == MOUSEBUTTONDOWN:
                return

class game:
    def __init__(self):
        self.place = 1          # 1体外；2身体；3心肺；4肠胃；5大脑
        self.num = 1            # 细菌数量
        self.time = 0
        self.alive = True
        self.rect_size = [(405, 200, 20, 20)]

        self.first = False      # 从体外入侵到头部/躯干的关卡，False表示尚未通关，通关后不再开启
        self.level = 0          # 通过贪吃蛇、吃豆人进行增长，数字表示难度

    def show(self):
        if self.place == 2:
            play_sur_face.blit(pygame.image.load("image/body.jpg"), (0, 0))
            # rect[2]-心肺，rect[3]-大脑
            self.rect_size = [(300,230,20,20),(380,280,20,20), (342,370,25,25), (355,180,25,25)]
            pygame.draw.rect(play_sur_face, green, self.rect_size[3])
        if self.place == 3:
            play_sur_face.blit(pygame.image.load("image/heart.jpg"), (0, 0))
            # rect[2]-身体，rect[3]-肠胃
            self.rect_size = [(210,365,20,20),(380,260,20,20), (303,145,22,22), (355,415,22,22)]
            pygame.draw.rect(play_sur_face, green, self.rect_size[3])
        if self.place == 4:
            play_sur_face.blit(pygame.image.load("image/gut.jpg"), (0, 0))
            # rect[2]-肠胃
            self.rect_size = [(210,445,20,20),(370,520,20,20), (354,299,25,25)]
        if self.place == 5:
            play_sur_face.blit(pygame.image.load("image/brain.jpg"), (0, 0))
            # rect[2]-身体
            self.rect_size = [(245,200,20,20),(350,180,20,20), (318,325,23,23)]
        pygame.draw.rect(play_sur_face, green, self.rect_size[0])
        pygame.draw.rect(play_sur_face, green, self.rect_size[1])
        pygame.draw.rect(play_sur_face, green, self.rect_size[2])

    def click(self, mouse):
        if self.place == 2:
            if self.rect_size[2][0] + self.rect_size[2][2] > mouse[0] > self.rect_size[2][0] and self.rect_size[2][1] + self.rect_size[2][3] > mouse[1] > self.rect_size[2][1]:
                self.place, self.num = subgame.move(play_sur_face, 2, 3, self.num)
            if self.rect_size[3][0] + self.rect_size[3][2] > mouse[0] > self.rect_size[3][0] and self.rect_size[3][1] + self.rect_size[3][3] > mouse[1] > self.rect_size[3][1]:
                self.place, self.num = subgame.move(play_sur_face, 2, 5, self.num)
        elif self.place == 3:
            if self.rect_size[2][0] + self.rect_size[2][2] > mouse[0] > self.rect_size[2][0] and self.rect_size[2][1] + self.rect_size[2][3] > mouse[1] > self.rect_size[2][1]:
                self.place, self.num = subgame.move(play_sur_face, 3, 2, self.num)
            if self.rect_size[3][0] + self.rect_size[3][2] > mouse[0] > self.rect_size[3][0] and self.rect_size[3][1] + self.rect_size[3][3] > mouse[1] > self.rect_size[3][1]:
                self.place, self.num = subgame.move(play_sur_face, 3, 4, self.num)
        elif self.place == 4:
            if self.rect_size[2][0] + self.rect_size[2][2] > mouse[0] > self.rect_size[2][0] and self.rect_size[2][1] + self.rect_size[2][3] > mouse[1] > self.rect_size[2][1]:
                self.place, self.num = subgame.move(play_sur_face, 4, 3, self.num)
        elif self.place == 5:
            if self.rect_size[2][0] + self.rect_size[2][2] > mouse[0] > self.rect_size[2][0] and self.rect_size[2][1] + self.rect_size[2][3] > mouse[1] > self.rect_size[2][1]:
                self.place, self.num = subgame.move(play_sur_face, 5, 2, self.num)
        
        if self.rect_size[0][0] + self.rect_size[0][2] > mouse[0] > self.rect_size[0][0] and self.rect_size[0][1] + self.rect_size[0][3] > mouse[1] > self.rect_size[0][1]:
            self.level, self.num = subgame.snake_game(play_sur_face, self.level, self.num)
        if self.rect_size[1][0] + self.rect_size[1][2] > mouse[0] > self.rect_size[1][0] and self.rect_size[1][1] + self.rect_size[1][3] > mouse[1] > self.rect_size[1][1]:
            self.level, self.num = subgame.beens_game(play_sur_face, self.level, self.num)



# 初始化pygame
pygame.init()
white = (255,255,255)
black = (0,0,0)
gray = (128,128,128)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
blue = (0,0,255)
text_color = [(96,96,96), (192,192,192), (255,255,255)]
size = (600, 600)
clock = pygame.time.Clock()

germ = game()
# 这是游戏框
play_sur_face = pygame.display.set_mode(size)
# 设置标题
pygame.display.set_caption("What I Am?")
# 加载图标
pygame.display.set_icon(pygame.image.load("photo.png"))
# 获得当前系统所有可用字体
font = pygame.font.SysFont("simhei", 20) # 20 -- 字体大小
tip_font = pygame.font.SysFont("simhei", 10)


# 开始动画
if True:
    play_sur_face.blit(pygame.image.load("image/out.jpg"), (0, 0))
    play_sur_face.blit(font.render("开始游戏", True, (0,0,0)), (250, 200))
    pygame.display.flip()
    wait_to_continue()
    pygame.draw.rect(play_sur_face, pygame.Color(0, 0, 0), Rect(0, 0, 600, 600))
    for i in range(3):
        clock.tick(5)
        play_sur_face.blit(font.render("我是谁？", True, text_color[i]), (20, 30))
        pygame.display.flip()
    clock.tick(1)
    for i in range(3):
        clock.tick(5)
        play_sur_face.blit(font.render("我在哪？", True, text_color[i]), (20, 70))
        pygame.display.flip()
    clock.tick(1)
    for i in range(3):
        clock.tick(5)
        play_sur_face.blit(font.render("我要做什么？", True, text_color[i]), (20, 110))
        pygame.display.flip()
    clock.tick(1)
    for i in range(3):
        clock.tick(5)
        play_sur_face.blit(font.render("那个大家伙...是什么？", True, text_color[i]), (20, 150))
        pygame.display.flip()
    clock.tick(1)
    for i in range(3):
        clock.tick(5)
        play_sur_face.blit(tip_font.render("按任意键继续", True, text_color[i]), (250, 550))
        pygame.display.flip()
    wait_to_continue()

# 第一关
while germ.place == 1:
    clock.tick(60)
    # 插入开始图片
    play_sur_face.blit(pygame.image.load("image/out.jpg"), (0, 0))
    # 检测退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if germ.rect_size[0][0] + germ.rect_size[0][2] > mouse[0] > germ.rect_size[0][0] and germ.rect_size[0][1] + germ.rect_size[0][3] > mouse[1] > germ.rect_size[0][1]:
                germ.place = subgame.first_game(play_sur_face)
        # 回车进入身体，esc退出
        elif event.type == KEYDOWN:
            # 按esc键退出游戏
            if event.key == K_ESCAPE:  
                pygame.quit()
                sys.exit()
            elif event.key == ord('l'):
                germ.place = 2
            else:
                germ.place = subgame.first_game(play_sur_face)
    mouse = pygame.mouse.get_pos()
    if germ.rect_size[0][0] + germ.rect_size[0][2] > mouse[0] > germ.rect_size[0][0] and germ.rect_size[0][1] + germ.rect_size[0][3] > mouse[1] > germ.rect_size[0][1]:
        pygame.draw.rect(play_sur_face, bright_green, germ.rect_size[0])
    else:
        pygame.draw.rect(play_sur_face, green, germ.rect_size[0])
    pygame.display.update()

germ.place = 2
if True:
    pygame.draw.rect(play_sur_face, pygame.Color(0, 0, 0), Rect(0, 0, 600, 600))
    for i in range(3):
        clock.tick(5)
        play_sur_face.blit(font.render("我好像，进来了？", True, text_color[i]), (20, 30))
        pygame.display.flip()
    clock.tick(1)
    for i in range(3):
        clock.tick(5)
        play_sur_face.blit(font.render("这里好温暖，好舒服", True, text_color[i]), (20, 70))
        pygame.display.flip()
    clock.tick(1)
    for i in range(3):
        clock.tick(5)
        play_sur_face.blit(font.render("好像还有好多好吃的", True, text_color[i]), (20, 110))
        pygame.display.flip()
    clock.tick(1)
    for i in range(3):
        clock.tick(5)
        play_sur_face.blit(tip_font.render("按任意键继续", True, text_color[i]), (250, 550))
        pygame.display.flip()
    wait_to_continue()

while germ.alive:
    # TODO 接下来是正常的游戏，新的剧情只会在游戏中触发。
    clock.tick(60)
    germ.show()# 检测退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            # 如果click则判断是否敲击
            if germ.click(mouse):
                germ.place = subgame.first_game(play_sur_face)
        # 回车进入身体，esc退出
        elif event.type == KEYDOWN:
            # 按esc键退出游戏
            if event.key == K_ESCAPE:  
                pygame.quit()
                sys.exit()
    mouse = pygame.mouse.get_pos()
    for i in range(len(germ.rect_size)):
        if germ.rect_size[i][0] + germ.rect_size[i][2] > mouse[0] > germ.rect_size[i][0] and germ.rect_size[i][1] + germ.rect_size[i][3] > mouse[1] > germ.rect_size[i][1]:
            pygame.draw.rect(play_sur_face, bright_green, germ.rect_size[i])
    pygame.display.flip()

# TODO 结局

# 背景设置为白色
pygame.draw.rect(play_sur_face, pygame.Color(255, 255, 255), Rect(0, 0, 600, 600))
# 介绍游戏规则
play_sur_face.blit(pygame.image.load("help.png") , (0, 0))
pygame.display.flip()
# 等待玩家响应
wait_to_continue()



# 结束游戏
pygame.quit()
sys.exit()
