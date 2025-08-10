import pygame
from pygame.locals import  *  #加载pygame中所有常量
from itertools import cycle   #迭代工具
import random
import time
SCREENWITDH=800   #宽度
SCREENHEIGHT=260  #高度
FPS=30  #更新画面的时间
Cur_XSpeed = 5
Cur_YSpeed = 6
game_over_time = 0  # 定义game_over_time变量


#定义一个地图类
class MyMap:
    #加载背景图片
    def __init__(self,x,y):
        #加载白天和黑天背景图
        self.bg_light=pygame.image.load("image/bg_light.png")
        self.bg_night=pygame.image.load("image/bg_night.png")
        self.current_bg = self.bg_light
        self.x=x
        self.y=y
        self.switch_time = time.time()  # 记录切换时间

    def map_rolling(self, speed):
        if self.x<-790: #说明地图已经移动完毕
            self.x=800  #给地图新坐标
        else:
            self.x -= speed*0.6 # 移动speed个像素

    #更新地图
    def map_update(self):
        current_time = time.time()
        if current_time - self.switch_time >= 10:  # 每隔10秒切换背景
            self.current_bg = self.bg_night if self.current_bg == self.bg_light else self.bg_light
            self.switch_time = current_time  # 重置切换时间
        SCREEN.blit(self.current_bg,(self.x,self.y))

#恐龙类
class Dinasaur:
    def __init__(self):
        #初始化小恐龙矩形
        self.rect=pygame.Rect(0,0,0,0)
        self.jumpState=False  #跳跃的状态
        self.jumpHeight=200   #第一段跳跃高度
        self.secondJumpHeight=100  #第二段跳跃高度
        self.lowest_y=140     #最低坐标
        self.jumpValue=0      #跳跃增变量
        self.dinasaurIndex=0
        self.dinasaurIndexGen=cycle([0,1,2])
        self.last_speed_update = time.time()  # 初始化上次更新速度的时间
        self.jump_speed = Cur_YSpeed * 1.5  # 初始化跳跃速度，增加1.5倍
        self.jump_count = 0  # 跳跃次数

        # 加载并调整小恐龙图像的大小
        self.dinasaur_image=(
            pygame.transform.scale(pygame.image.load('image/dinosaur1.png').convert_alpha(), (90, 60)),
            pygame.transform.scale(pygame.image.load('image/dinosaur2.png').convert_alpha(), (90, 60)),
            pygame.transform.scale(pygame.image.load('image/dinosaur3.png').convert_alpha(), (90, 60)),
        )
        self.jump_audio=pygame.mixer.Sound('audio/jump.wav') #加载音效
        self.rect.size=self.dinasaur_image[0].get_size()     #设置小恐龙矩形大小
        self.x=50                                            #设置小恐龙的x坐标
        self.y=self.lowest_y                                 #设置小恐龙的y坐标
        self.rect.topleft=(self.x,self.y)                    #设置左上角为准

    #跳跃
    def jump(self):
        if self.jump_count < 2:  # 允许最多两次跳跃
            self.jumpState=True
            if self.jump_count == 0:  # 第一次跳跃
                self.jumpValue = -self.jump_speed  # 设置向上的初始速度
                self.jump_audio.play()  # 播放跳跃音效
            else:  # 第二次跳跃
                self.jumpValue = -self.jump_speed * 0.8 # 第二次跳跃的初始速度稍微小一点
            self.jump_count += 1
            self.jump_audio.play()  # 播放跳跃音效

    #小恐龙的移动
    def move(self):
        if self.jumpState:      #可以起跳
            if self.jump_count == 1:  # 第一段跳跃
                if self.rect.y > self.lowest_y - self.jumpHeight:
                    self.rect.y += self.jumpValue
                    self.jumpValue += 1  # 模拟重力
                else:
                    self.jumpValue = 1  # 开始下落
            elif self.jump_count == 2:  # 第二段跳跃
                if self.rect.y > self.lowest_y - self.jumpHeight - self.secondJumpHeight:
                    self.rect.y += self.jumpValue
                    self.jumpValue += 1  # 模拟重力
                else:
                    self.jumpValue = 1  # 开始下落
            
            if self.rect.y >= self.lowest_y:  # 如果落地
                self.rect.y = self.lowest_y
                self.jumpState = False
                self.jump_count = 0  # 重置跳跃次数

    #绘制恐龙
    def draw_dinasour(self):
        #匹配恐龙动图
        dinasaurindex=next(self.dinasaurIndexGen)
        #实现绘制
        SCREEN.blit(self.dinasaur_image[dinasaurindex],(self.x,self.rect.y))

#障碍物类
class Obstacle:
    score=1 #分数
    def __init__(self):
        #初始化障碍物的矩形
        self.rect=pygame.Rect(0,0,0,0)
        #加载障碍物的图片
        self.stone=pygame.image.load('image/stone.png').convert_alpha() #加载石头
        self.cacti=pygame.image.load('image/cacti.png').convert_alpha() #加载仙人掌
        # 加载分数图片
        self.numbers=(pygame.image.load('image/0.png').convert_alpha(), #convert_alpha()透明度
                      pygame.image.load('image/1.png').convert_alpha(),
                      pygame.image.load('image/2.png').convert_alpha(),
                      pygame.image.load('image/3.png').convert_alpha(),
                      pygame.image.load('image/4.png').convert_alpha(),
                      pygame.image.load('image/5.png').convert_alpha(),
                      pygame.image.load('image/6.png').convert_alpha(),
                      pygame.image.load('image/7.png').convert_alpha(),
                      pygame.image.load('image/8.png').convert_alpha(),
                      pygame.image.load('image/9.png').convert_alpha(),
                      )
        #加载加分的音效
        self.score_audio=pygame.mixer.Sound('audio/score.wav')
        #创建0，1之间的随机数,0是石头，1是仙人掌
        r=random.randint(0,1)
        if r ==0:
            self.image=self.stone
        else:
            self.image=self.cacti
        #根据障碍物位图的宽高设置矩形
        self.rect.size=self.image.get_size()
        #获取位图的宽高
        self.width,self.height=self.rect.size
        #障碍物绘制坐标
        self.x=800
        self.y=200-(self.height/2)
        self.rect.center=(self.x,self.y)

    #移动障碍物
    def obstacle_move(self, speed):
        self.rect.x -= speed   #移动速度为speed个像素

    #绘制障碍物
    def draw_obstacle(self):
        SCREEN.blit(self.image,(self.rect.x,self.rect.y))

    #获取分数
    def getScore(self):
        self.score
        tmp=self.score
        if tmp==1:
            self.score_audio.play()
        self.score=0
        return tmp

    #显示分数
    def showScore(self,score):
        self.scoreDigits=[int(x) for x in list(str(score))]
        totalWidth=0                #要显示的数字的总宽度
        for digit in self.scoreDigits:
            #获取积分图片的宽度
            totalWidth+=self.numbers[digit].get_width()
        #分数横向位置
        xoffset=(SCREENWITDH - totalWidth)/2
        for digit in self.scoreDigits:
            #绘制分数
            SCREEN.blit(self.numbers[digit],(xoffset,SCREENHEIGHT*0.1))
            #随着数字增加改变位置
            xoffset+=self.numbers[digit].get_width()

#  检查两个矩形是否有足够的重叠以触发碰撞
def collide_partially(rect1, rect2, threshold=0.1):
    dx = min(rect1.right, rect2.right) - max(rect1.left, rect2.left)
    dy = min(rect1.bottom, rect2.bottom) - max(rect1.top, rect2.top)
    if (dx >= 0) and (dy >= 0):
        overlap_area = dx * dy
        total_area = rect1.width * rect1.height + rect2.width * rect2.height
        common_area = total_area - (total_area - overlap_area)
        overlap_ratio = common_area / total_area
        return overlap_ratio > threshold
    return False

#游戏结束的方法
def game_over():
    bump_audio=pygame.mixer.Sound('audio/bump.wav')
    bump_audio.play()

    #获取窗口宽高
    screen_w=pygame.display.Info().current_w
    screen_h=pygame.display.Info().current_h

    #加载游戏结束的图片
    over_img=pygame.image.load('image/gameover.png').convert_alpha()

    # 获取原始图片的尺寸
    original_width, original_height = over_img.get_size()

    # 计算新的尺寸
    new_width = original_width * 2
    new_height = original_height * 2

    # 缩放图片
    scaled_over_img = pygame.transform.scale(over_img, (new_width, new_height))

    #绘制游戏结束的图标在窗体中间
    SCREEN.blit(scaled_over_img,((screen_w-over_img.get_width())/3,(screen_h-over_img.get_height())/2))

# 显示游戏规则公告板
def show_rules():
    rules_font = pygame.font.SysFont(None, 24)  # 增大字号以提高可读性
    rules = [
        "Game Rules:",
        "1. Press space to jump",
        "2. Press space twice for double jump",
        "3. Avoid all obstacles",
        "4. The longer you survive, the higher your score",
        "Press space to start the game"
    ]
    
    # 加载白天背景图片
    bg_light = pygame.image.load("image/bg_light.png")
    
    # 创建一个半透明的遮罩层
    overlay = pygame.Surface((SCREENWITDH, SCREENHEIGHT), pygame.SRCALPHA)
    overlay.fill((255, 255, 255, 180))  # 白色半透明
    
    # 将背景和遮罩层绘制到屏幕上
    SCREEN.blit(bg_light, (0, 0))
    SCREEN.blit(overlay, (0, 0))
    
    for i, rule in enumerate(rules):
        text = rules_font.render(rule, True, (0, 0, 0))  # 黑色文字
        text_rect = text.get_rect(center=(SCREENWITDH // 2, SCREENHEIGHT // 2 - 100 + i * 40))
        SCREEN.blit(text, text_rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                waiting = False
def mainGame():
    score=0 #记录分值
    over=False
    global SCREEN,FPSLOCK
    pygame.init() #初始化pygame
    FPSLOCK=pygame.time.Clock() #刷新屏幕的时间锁
    SCREEN=pygame.display.set_mode((SCREENWITDH,SCREENHEIGHT)) #设置屏幕的大小
    pygame.display.set_caption("恐龙酷跑")  #随意定义的游戏标题

    show_rules()  # 显示游戏规则

    bg_light1=MyMap(0,0) #地图1
    bg_light2=MyMap(800,0) #地图2

    #创建小恐龙
    dinasaur=Dinasaur()

    addobstacleTimer=0 #初始化障碍物时间为0

    obstacle_list=[] #障碍物对象的列表

    while True:
        #判断是否单击了关闭窗口
        for event in pygame.event.get():
            if event.type==QUIT:
                over=True
                exit() #退出程序
            if event.type==KEYDOWN and event.key==K_SPACE:
                if over:  # 如果游戏结束
                    current_time = time.time()
                    if current_time - game_over_time > 0.5:  # 确保游戏结束后2秒才能重新开始
                        # 重置游戏
                        score = 0
                        over = False
                        obstacle_list.clear()
                        dinasaur = Dinasaur()
                        addobstacleTimer = 0
                        # 重置背景为白天
                        bg_light1.current_bg = bg_light1.bg_light
                        bg_light2.current_bg = bg_light2.bg_light
                        bg_light1.switch_time = time.time()
                        bg_light2.switch_time = time.time()
                else:
                    dinasaur.jump()  # 否则正常跳跃

        if not over:
            Xspeed = Cur_XSpeed  # 局部X轴速度变量
            Xspeed *= 1.2 ** (score // 3)  # 每100分增加5%的速度

            bg_light1.map_update() #绘制地图到更新的作用
            bg_light1.map_rolling(Xspeed) #地图移动
            bg_light2.map_update()
            bg_light2.map_rolling(Xspeed)
                
            dinasaur.move() #移动小恐龙
            #绘制恐龙
            dinasaur.draw_dinasour()

            #计算障碍物产生间隔的时间
            if addobstacleTimer>=1300:
                r=random.randint(0,100)
                if r>10:
                    #创建障碍物对象
                    obstacle=Obstacle()
                    #将障碍物推向添加到列表中
                    obstacle_list.append(obstacle)

                #重置添加障碍物的时间
                addobstacleTimer=0

            #遍历障碍物
            for i in range(len(obstacle_list)):
                #移动障碍物
                obstacle_list[i].obstacle_move(Xspeed)
                #绘制障碍物
                obstacle_list[i].draw_obstacle()
                if collide_partially(dinasaur.rect, obstacle_list[i].rect):
                    over=True
                    game_over()
                    game_over_time = time.time()  # 记录游戏结束的时间
                else:
                    if(obstacle_list[i].rect.x+obstacle_list[i].rect.width)<dinasaur.rect.x:
                        #加分
                        score+=obstacle_list[i].getScore()
                obstacle_list[i].showScore(score)

        addobstacleTimer +=20  #增加障碍物时间
        pygame.display.update() #更新窗口
        FPSLOCK.tick(FPS) #多久更新一次



if __name__ == '__main__':
    mainGame()