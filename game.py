import random
import pygame
import sys
from pygame.locals import *
import subgame

def show_help(place):
    pygame.draw.rect(play_sur_face, pygame.Color(255,255,255), Rect(0, 0, 600, 600))
    font = pygame.font.SysFont("simhei", 20) # 20 -- 字体大小
    tip_font = pygame.font.SysFont("simhei", 12)
    sentences = [["这是一款关于细菌和人的小游戏", "你将成为一个小细菌", "你能突破第一道防线进入人体", "亦能吸收营养物质生长繁殖", "但是要小心不要被免疫细胞消灭了哦", "你可能能变得富有感染力、控制力", "又或许你可以融入这个地方", "最新版本/游戏源码可以到GitHub获取", "https://github.com/Lc-1024/Game-What-I-Am"],
                 ["你好像是一个弱小的细菌", "这里似乎可以当你的庇护所", "尝试进入他的体内吧", "那里会有享受不完的美食", "说不定，你还能变得更强大", "鼠标放在方块（不释放）上可以查看关卡信息哦"],
                 ["看呐，你成功进来了", "四处走走，看看有没有什么可以吃的", "说不定你还能繁殖出更多的后代呢", "你也可以到别的地方逛逛吧", "不知道会不会变异出什么新能力"], 
                 ["这好像是人类的心肺系统", "从这里可以走遍全身上下呢", "或许你可以尝试让他咳嗽？", "这样你的后代就能去其他人身上了", "那样数量是不是可以越来越多"], 
                 ["啊，这里有好多吃的", "在这里可以舒服的过完一辈子吧", "为什么这些细胞都在攻击我，我明明没有恶意", "要是我们能做朋友就好了"],
                 ["看呐，这里好多沟沟", "这是不是就是这个人类的大脑？", "这具身体太诱人了", "如果他能属于我就好了", "我要成为这里的王！"], 
                 ["恭喜你获取了一种新的能力", "每个能力都能增强对应的属性", "每种属性的三种能力都获得之后", "你可以选择变异成对应的细菌", "分化之后，就会走向结局"]]
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
            elif event.type == MOUSEBUTTONUP:
                return

class game:
    def __init__(self):
        self.place = 1          # 1体外；2身体；3心肺；4肠胃；5大脑
        self.num = 1            # 细菌数量
        self.time = 0
        self.rect_size = [(345, 283, 20, 20)]
        self.scale = [0, (0, 0, 300, 300), (230, 200, 380, 370), (220, 200, 400, 400), (200, 350, 450, 550), (250, 150, 350, 280)]
        self.sen = [[],
                    ["从口腔破损处进入人体"], 
                    ["去血液中寻找食物", "去组织细胞间寻找食物", "去心肺看看吧(数量>=1e4)", "去大脑转转(数量>=1e8)"], 
                    ["去血液中寻找食物", "去肌肉细胞间寻找食物", "去上面转转(数量>=1e4)", "去肠胃看看吧(数量>=1e6)"], 
                    ["去血液中寻找食物", "去肠道细胞间寻找食物", "去心肺看看吧(数量>=1e6)"], 
                    ["去血液中寻找食物", "去神经细胞间寻找食物", "去下面看看吧(数量>=1e4)"]]
        self.got = [False, False, False, False, False, False, False, False, False, False, False, False]
        self.abil = [["咳嗽", "增加传染性"],
                     ["喷嚏", "增加传染性"],
                     ["肺炎", "增加传染性"],
                     ["头晕", "增强控制力"],
                     ["失眠", "增强控制力"],
                     ["癫痫", "增强控制力"],
                     ["随和", "增强亲和力"],
                     ["亲和", "增强亲和力"],
                     ["免疫", "增加亲和力"],
                     ["你的传染性很强", "向着病原体发展"], 
                     ["你的控制力很强", "向着脑细胞出发"],
                     ["你的亲和度很高", "向着益生菌发展"]]

        self.first = False      # 从体外入侵到头部/躯干的关卡，False表示尚未通关，通关后不再开启
        self.level = 0          # 通过贪吃蛇、吃豆人进行增长，数字表示难度
        self.picture = pygame.image.load("image/germ.bmp")
        self.x = [0, 80, 230, 300, 350, 300]
        self.y = [0, 80, 200, 200, 350, 200]

        self.end = 0            # 0死亡；1传染性细菌；3共生细菌；2僵尸型细菌

    def show_got(self):
        shape = [(20, 200, 160, 100), (220, 200, 160, 100), (420, 200, 160, 100)]
        choice = -1
        t = [random.randint(0, 8), random.randint(0, 8), random.randint(0, 8)]
        if self.got[0] and self.got[1] and self.got[2]:
            t[0] = 9
        if self.got[3] and self.got[4] and self.got[5]:
            t[1] = 10
        if self.got[6] and self.got[7] and self.got[8]:
            t[2] = 11
        while self.got[t[0]] == True:
            t[0] = random.randint(0, 8)
        while self.got[t[1]] == True or t[1] == t[0]:
            t[1] = random.randint(0, 8)
        while self.got[t[2]] == True or t[2] == t[0] or t[2] == t[1]:
            t[2] = random.randint(0, 8)
        while choice == -1:
            pygame.draw.rect(play_sur_face, (255, 235, 215), (0, 0, 600, 600))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:  
                        pygame.quit()
                        sys.exit()
                elif event.type == MOUSEBUTTONUP:
                    mouse = pygame.mouse.get_pos()
                    for i in range(3):
                        if shape[i][0] + shape[i][2] > mouse[0] > shape[i][0] and shape[i][1] + shape[i][3] > mouse[1] > shape[i][1]:
                            choice = t[i]
                            break
                    if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
                        show_help(6)
            mouse = pygame.mouse.get_pos()
            for i in range(3):
                if shape[i][0] + shape[i][2] > mouse[0] > shape[i][0] and shape[i][1] + shape[i][3] > mouse[1] > shape[i][1]:
                    pygame.draw.rect(play_sur_face, help_color[1], shape[i])
                else:
                    pygame.draw.rect(play_sur_face, help_color[0], shape[i])
                if t[i] != 9+i:
                    play_sur_face.blit(font.render(self.abil[t[i]][0], True, (0,0,0)), (shape[i][0]+60, shape[i][1]+15))
                    play_sur_face.blit(font.render(self.abil[t[i]][1], True, (0,0,0)), (shape[i][0]+30, shape[i][1]+60))
                else:
                    play_sur_face.blit(font.render(self.abil[t[i]][0], True, (0,0,0)), (shape[i][0]+10, shape[i][1]+15))
                    play_sur_face.blit(font.render(self.abil[t[i]][1], True, (0,0,0)), (shape[i][0]+10, shape[i][1]+60))

            if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
                pygame.draw.rect(play_sur_face, help_color[1], help_size)
            else:
                pygame.draw.rect(play_sur_face, help_color[0], help_size)
            play_sur_face.blit(tip_font.render("Help", True, (0,0,0)), (help_size[0]+8, help_size[1]+3))
            pygame.display.update()
        
        if 11 >= choice >= 9:
            self.end = choice - 9
        else:
            self.got[choice] = True

            

    def random_move(self, time):
        if time % 10 == 0:
            tmpX = random.randint(-5, 5)
            tmpY = random.randint(-5, 5)
            if self.scale[self.place][0] < self.x[self.place] + tmpX < self.scale[self.place][2]:
                self.x[self.place] += tmpX
            if self.scale[self.place][1] < self.y[self.place] + tmpY < self.scale[self.place][3]:
                self.y[self.place] += tmpY
        play_sur_face.blit(germ.picture, (germ.x[germ.place], germ.y[germ.place]))
        return time+1

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
        got = False
        if self.place == 2:
            if self.num >= 1e4 and self.rect_size[2][0] + self.rect_size[2][2] > mouse[0] > self.rect_size[2][0] and self.rect_size[2][1] + self.rect_size[2][3] > mouse[1] > self.rect_size[2][1]:
                self.place, self.num, got = subgame.move(play_sur_face, 2, 3, self.num)
            if self.num >= 1e8 and self.rect_size[3][0] + self.rect_size[3][2] > mouse[0] > self.rect_size[3][0] and self.rect_size[3][1] + self.rect_size[3][3] > mouse[1] > self.rect_size[3][1]:
                self.place, self.num, got = subgame.move(play_sur_face, 2, 5, self.num)
        elif self.place == 3:
            if self.num >= 1e4 and self.rect_size[2][0] + self.rect_size[2][2] > mouse[0] > self.rect_size[2][0] and self.rect_size[2][1] + self.rect_size[2][3] > mouse[1] > self.rect_size[2][1]:
                self.place, self.num, got = subgame.move(play_sur_face, 3, 2, self.num)
            if self.num >= 1e6 and self.rect_size[3][0] + self.rect_size[3][2] > mouse[0] > self.rect_size[3][0] and self.rect_size[3][1] + self.rect_size[3][3] > mouse[1] > self.rect_size[3][1]:
                self.place, self.num, got = subgame.move(play_sur_face, 3, 4, self.num)
        elif self.place == 4:
            if self.num >= 1e6 and self.rect_size[2][0] + self.rect_size[2][2] > mouse[0] > self.rect_size[2][0] and self.rect_size[2][1] + self.rect_size[2][3] > mouse[1] > self.rect_size[2][1]:
                self.place, self.num, got = subgame.move(play_sur_face, 4, 3, self.num)
        elif self.place == 5:
            if self.num >= 1e4 and self.rect_size[2][0] + self.rect_size[2][2] > mouse[0] > self.rect_size[2][0] and self.rect_size[2][1] + self.rect_size[2][3] > mouse[1] > self.rect_size[2][1]:
                self.place, self.num, got = subgame.move(play_sur_face, 5, 2, self.num)
        
        if self.rect_size[0][0] + self.rect_size[0][2] > mouse[0] > self.rect_size[0][0] and self.rect_size[0][1] + self.rect_size[0][3] > mouse[1] > self.rect_size[0][1]:
            self.level, self.num, got = subgame.snake_game(play_sur_face, self.level, self.num)
        if self.rect_size[1][0] + self.rect_size[1][2] > mouse[0] > self.rect_size[1][0] and self.rect_size[1][1] + self.rect_size[1][3] > mouse[1] > self.rect_size[1][1]:
            self.level, self.num, got = subgame.beens_game(play_sur_face, self.level, self.num)

        if got:
            self.show_got()

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
time = 0
font = pygame.font.SysFont("simhei", 20) # simhei是简体字，也可以到C:/Windows/Fonts/找个中文字体
tip_font = pygame.font.SysFont("simhei", 12)

germ = game()
germ.place = 3
# 这是游戏框
play_sur_face = pygame.display.set_mode(size)
# 设置标题
pygame.display.set_caption("What I Am?")
# 加载图标
pygame.display.set_icon(pygame.image.load("image/germ.jpg"))


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
            elif event.type == MOUSEBUTTONUP:
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
    time = germ.random_move(time)
    # 检测退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
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
        play_sur_face.blit(tip_font.render(germ.sen[germ.place][0], True, (0,0,0)), (germ.rect_size[0][0]+20, germ.rect_size[0][1]+4))
    else:
        pygame.draw.rect(play_sur_face, move_color[0], germ.rect_size[0])
    if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
        pygame.draw.rect(play_sur_face, help_color[1], help_size)
    else:
        pygame.draw.rect(play_sur_face, help_color[0], help_size)
    play_sur_face.blit(tip_font.render("Help", True, (0,0,0)), (help_size[0]+8, help_size[1]+3))
    pygame.display.update()

# 转场动画
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

# 第二关
while germ.num > 0 and germ.end == 0:
    clock.tick(60)
    germ.show()
    time = germ.random_move(time)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
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
            play_sur_face.blit(tip_font.render(germ.sen[germ.place][i], True, (0,0,0)), (germ.rect_size[i][0]+20, germ.rect_size[i][1]+4))
        else:
            pygame.draw.rect(play_sur_face, all_color[i][0], germ.rect_size[i])
    if help_size[0] + help_size[2] > mouse[0] > help_size[0] and help_size[1] + help_size[3] > mouse[1] > help_size[1]:
        pygame.draw.rect(play_sur_face, help_color[1], help_size)
    else:
        pygame.draw.rect(play_sur_face, help_color[0], help_size)
    play_sur_face.blit(tip_font.render("数量："+str(germ.num), True, (0, 0, 0)), (10, 10))
    play_sur_face.blit(tip_font.render("Help", True, (0,0,0)), (help_size[0]+8, help_size[1]+3))
    pygame.display.flip()

def show_end(end):
    pygame.draw.rect(play_sur_face, pygame.Color(255,255,255), Rect(0, 0, 600, 600))
    font = pygame.font.SysFont("simhei", 20) # 20 -- 字体大小
    tip_font = pygame.font.SysFont("simhei", 12)
    sentences = [["很可惜，你被驱逐了", "人类可能不喜欢你呢", "但有可能只是暂时的", "走吧", "", "", "最新版本/游戏源码可以到GitHub获取", "https://github.com/Lc-1024/Game-What-I-Am"],
                 ["你终于成长为了富有传染性的细菌", "你的后代离开了第一个宿主", "他们走向了越来越多的人类", "渐渐的，你的子孙存在于全世界", "", "", "最新版本/游戏源码可以到GitHub获取", "https://github.com/Lc-1024/Game-What-I-Am"],
                 ["你做到了，你入侵了脑细胞", "现在这个人类已经是你的傀儡了", "你可以做所有你想做的事", "去吧，成为一个人类吧", "", "", "最新版本/游戏源码可以到GitHub获取", "https://github.com/Lc-1024/Game-What-I-Am"], 
                 ["他们，终于把你当成朋友了", "你可以在这里生活了", "吃饱喝足的生活真美啊", "也不用再担惊受怕了", "你似乎也帮上忙了呢", "", "", "最新版本/游戏源码可以到GitHub获取", "https://github.com/Lc-1024/Game-What-I-Am"]]
    for i, sen in enumerate(sentences[end]):
        play_sur_face.blit(font.render(sen, True, (0,0,0)), (20, 30+i*40))
    play_sur_face.blit(tip_font.render("按任意键结束游戏", True, (0,0,0)), (250, 550))
    pygame.display.flip()
    wait_to_continue()

show_end(germ.end)

pygame.quit()
sys.exit()
