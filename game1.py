import random
import pygame
import sys
from pygame.locals import *
import subgame

def show_help(place):
    pygame.draw.rect(play_sur_face, pygame.Color(255,255,255), Rect(0, 0, 600, 600))
    font = pygame.font.SysFont("simhei", 20) # 20 -- 字体大小
    tip_font = pygame.font.SysFont("simhei", 10)
    sentences = [["这是一款关于细菌和人的小游戏", "你将成为一个小细菌", "你能突破第一道防线进入人体", "亦能吸收营养物质生长繁殖", "但是要小心不要被免疫细胞消灭了哦", "你可能能变得富有感染力、控制力", "又或许你可以融入这个地方"],
                 ["你好像是一个弱小的细菌", "这里似乎可以当你的庇护所", "尝试进入他的体内吧", "那里会有享受不完的美食", "说不定，你还能变得更强大"],
                 ["看呐，你成功进来了", "四处走走，看看有没有什么可以吃的", "说不定你还能繁殖出更多的后代呢", "你也可以到别的地方逛逛吧", "不知道会不会变异出什么新能力"], 
                 ["这好像是人类的心肺系统", "从这里可以走遍全身上下呢", "或许你可以尝试让他咳嗽？", "这样你的后代就能去其他人身上了", "那样数量是不是可以越来越多"], 
                 ["啊，这里有好多吃的", "在这里可以舒服的过完一辈子吧", "为什么这些细胞都在攻击我，我明明没有恶意", "要是我们能做朋友就好了"],
                 ["看呐，这里好多沟沟", "这是不是就是这个人类的大脑？", "这具身体太诱人了", "如果他能属于我就好了", "我要成为这里的王！"]]
    for i, sen in enumerate(sentences[place]):
        play_sur_face.blit(font.render(sen, True, (0,0,0)), (20, 30+i*40))
    play_sur_face.blit(tip_font.render("按任意键返回", True, (0,0,0)), (250, 550))
    pygame.display.flip()
    wait_to_continue()

# 等待玩家继续或退出
def wait_to_continue():
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
            pygame.draw.rect(play_sur_face, move_color[0], self.rect_size[3])
        if self.place == 3:
            play_sur_face.blit(pygame.image.load("image/heart.jpg"), (0, 0))
            # rect[2]-身体，rect[3]-肠胃
            self.rect_size = [(210,365,20,20),(380,260,20,20), (303,145,22,22), (355,415,22,22)]
            pygame.draw.rect(play_sur_face, move_color[0], self.rect_size[3])
        if self.place == 4:
            play_sur_face.blit(pygame.image.load("image/gut.jpg"), (0, 0))
            # rect[2]-肠胃
            self.rect_size = [(210,445,20,20),(370,520,20,20), (354,299,25,25)]
        if self.place == 5:
            play_sur_face.blit(pygame.image.load("image/brain.jpg"), (0, 0))
            # rect[2]-身体
            self.rect_size = [(245,200,20,20),(350,180,20,20), (318,325,23,23)]
        pygame.draw.rect(play_sur_face, snake_color[0], self.rect_size[0])
        pygame.draw.rect(play_sur_face, beens_color[0], self.rect_size[1])
        pygame.draw.rect(play_sur_face, move_color[0], self.rect_size[2])

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
back_color  = (255,255,255)
help_color  = [(220,220,220), (250,250,250)]
move_color  = [(255,218,185), (250,240,230)]
snake_color = [(200,0,0), (255,0,0)]
beens_color = [(238,238,0), (255,255,0)]
all_color   = [snake_color, beens_color, move_color, move_color]
text_color  = [(96,96,96), (192,192,192), (255,255,255)]

size = (600, 600)
help_size = (550, 10, 40, 20)
clock = pygame.time.Clock()
font = pygame.font.SysFont("simhei", 20) # simhei是简体字，也可以到C:/Windows/Fonts/找个中文字体
tip_font = pygame.font.SysFont("simhei", 12)

germ = game()
# 这是游戏框
play_sur_face = pygame.display.set_mode(size)
# 设置标题
pygame.display.set_caption("What I Am?")
# 加载图标
pygame.display.set_icon(pygame.image.load("image/photo.png"))

# 开始动画
if germ.place == 1:
    waiting = True
    while waiting:
        play_sur_face.blit(pygame.image.load("image/out.jpg"), (0, 0))
        play_sur_face.blit(font.render("开始游戏", True, (0,0,0)), (250, 200))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE): 
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
                    show_help(0)
                else:
                    waiting = False
            elif event.type == KEYDOWN:
                waiting = False
        mouse = pygame.mouse.get_pos()
        if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
            pygame.draw.rect(play_sur_face, help_color[1], help_size)
        else:
            pygame.draw.rect(play_sur_face, help_color[0], help_size)
        play_sur_face.blit(tip_font.render("Help", True, (0,0,0)), (help_size[0]+8, help_size[1]+3))
        pygame.display.flip()
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
            if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
                show_help(germ.place)
        # 回车进入身体，esc退出
        elif event.type == KEYDOWN:
            # 按esc键退出游戏
            if event.key == K_ESCAPE:  
                pygame.quit()
                sys.exit()
            elif event.key == ord('l'):
                germ.place = 2
    mouse = pygame.mouse.get_pos()
    if germ.rect_size[0][0] + germ.rect_size[0][2] > mouse[0] > germ.rect_size[0][0] and germ.rect_size[0][1] + germ.rect_size[0][3] > mouse[1] > germ.rect_size[0][1]:
        pygame.draw.rect(play_sur_face, move_color[1], germ.rect_size[0])
    else:
        pygame.draw.rect(play_sur_face, move_color[0], germ.rect_size[0])
    if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
        pygame.draw.rect(play_sur_face, help_color[1], help_size)
    else:
        pygame.draw.rect(play_sur_face, help_color[0], help_size)
    play_sur_face.blit(tip_font.render("Help", True, (0,0,0)), (help_size[0]+8, help_size[1]+3))
    pygame.display.update()

germ.place = 2
if germ.place == 2:
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
    clock.tick(60)
    germ.show()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            germ.click(mouse)
            if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
                show_help(germ.place)
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  
                pygame.quit()
                sys.exit()
    mouse = pygame.mouse.get_pos()
    for i in range(len(germ.rect_size)):
        if germ.rect_size[i][0] + germ.rect_size[i][2] > mouse[0] > germ.rect_size[i][0] and germ.rect_size[i][1] + germ.rect_size[i][3] > mouse[1] > germ.rect_size[i][1]:
            pygame.draw.rect(play_sur_face, all_color[i][1], germ.rect_size[i])
        else:
            pygame.draw.rect(play_sur_face, all_color[i][0], germ.rect_size[i])
    if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
        pygame.draw.rect(play_sur_face, help_color[1], help_size)
    else:
        pygame.draw.rect(play_sur_face, help_color[0], help_size)
    play_sur_face.blit(tip_font.render("数量："+str(germ.num), True, (0, 0, 0)), (10, 10))
    play_sur_face.blit(tip_font.render("Help", True, (0,0,0)), (help_size[0]+8, help_size[1]+3))
    pygame.display.flip()


pygame.draw.rect(play_sur_face, pygame.Color(255, 255, 255), Rect(0, 0, 600, 600))
play_sur_face.blit(pygame.image.load("help.png") , (0, 0))
pygame.display.flip()
wait_to_continue()

pygame.quit()
sys.exit()
