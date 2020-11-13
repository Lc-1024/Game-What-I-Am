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
    Ended = False
    while Ended == False:
        # 界面是否结束
        for event in pygame.event.get():
            # 退出游戏
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 按esc键退出游戏
                if event.key == K_ESCAPE:  
                    pygame.quit()
                    sys.exit()
                # 按下其他键继续游戏
                else:
                    Ended = True
                    break
        
        # 结束显示
        if Ended:
            break

class game:
    def __init__(self):
        self.place = 1          # 1体外；2身体；3心肺；4肠胃；5大脑
        self.num = 1            # 细菌数量
        self.time = 0
        self.alive = True
        self.rect_size = [(405, 200, 20, 20)]

        self.first = False      # 从体外入侵到头部/躯干的关卡，False表示尚未通关，通关后不再开启
        self.snake = 0          # 通过贪吃蛇进行增长，数字表示难度
        self.beens = 0          # 通过吃豆人进行增长，数字表示难度

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
            if self.rect_size[3][0] + self.rect_size[3][2] > mouse[0] > self.rect_size[3][0] and self.rect_size[3][1] + self.rect_size[3][3] > mouse[1] > self.rect_size[3][1]:
                self.snake = subgame.first_game(play_sur_face)
        if self.place == 3:
            if self.rect_size[3][0] + self.rect_size[3][2] > mouse[0] > self.rect_size[3][0] and self.rect_size[3][1] + self.rect_size[3][3] > mouse[1] > self.rect_size[3][1]:
                self.snake = subgame.first_game(play_sur_face)
        if self.place == 4:
            self.place = 4
        if self.place == 5:
            self.place = 5
        
        if self.rect_size[0][0] + self.rect_size[0][2] > mouse[0] > self.rect_size[0][0] and self.rect_size[0][1] + self.rect_size[0][3] > mouse[1] > self.rect_size[0][1]:
            self.snake, self.num = subgame.snake_game(play_sur_face, self.snake, self.num)
        if self.rect_size[1][0] + self.rect_size[1][2] > mouse[0] > self.rect_size[1][0] and self.rect_size[1][1] + self.rect_size[1][3] > mouse[1] > self.rect_size[1][1]:
            self.beens, self.num = subgame.beens_game(play_sur_face, self.beens, self.num)
        if self.rect_size[2][0] + self.rect_size[2][2] > mouse[0] > self.rect_size[2][0] and self.rect_size[2][1] + self.rect_size[2][3] > mouse[1] > self.rect_size[2][1]:
            self.snake = subgame.first_game(play_sur_face)
      

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

size = (600, 600)

clock = pygame.time.Clock()

germ = game()
# 这是游戏框
play_sur_face = pygame.display.set_mode(size)
# 设置标题
pygame.display.set_caption("细菌与人")
# 加载图标
pygame.display.set_icon(pygame.image.load("photo.png"))
# TODO 开始动画
# 更新显示
pygame.display.flip()

'''
# 插入开始图片
play_sur_face.blit(pygame.image.load("image/body.jpg"), (0, 0))
# 背景设置为白色
pygame.draw.rect(play_sur_face, pygame.Color(255, 255, 255), Rect(0, 0, 600, 600))
# 获得当前系统所有可用字体
font = pygame.font.SysFont("", 20) # 20 -- 字体大小
text_surface = font.render("Any key to continue", True, (0, 0, 0)) # True -- 锯齿边
play_sur_face.blit(text_surface, (200, 550))
'''
'''
# 第一关
while germ.first == False:
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
            print(event)
            if germ.rect_size[0][0] + germ.rect_size[0][2] > mouse[0] > germ.rect_size[0][0] and germ.rect_size[0][1] + germ.rect_size[0][3] > mouse[1] > germ.rect_size[0][1]:
                germ.first = subgame.first_game(play_sur_face)
        # 回车进入身体，esc退出
        elif event.type == KEYDOWN:
            # 按esc键退出游戏
            if event.key == K_ESCAPE:  
                pygame.quit()
                sys.exit()
            elif event.key == ord('l'):
                germ.first = True
            else:
                germ.first = subgame.first_game(play_sur_face)
    mouse = pygame.mouse.get_pos()
    if germ.rect_size[0][0] + germ.rect_size[0][2] > mouse[0] > germ.rect_size[0][0] and germ.rect_size[0][1] + germ.rect_size[0][3] > mouse[1] > germ.rect_size[0][1]:
        pygame.draw.rect(play_sur_face, bright_green, germ.rect_size[0])
    else:
        pygame.draw.rect(play_sur_face, green, germ.rect_size[0])
    pygame.display.update()
'''
germ.place = 5

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
            print(event)
            # 如果click则判断是否敲击
            if germ.click(mouse):
                germ.first = subgame.first_game(play_sur_face)
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
