import random
import sys
from time import sleep

import pygame  # 导入pygame模块
from pygame.locals import *  # 导入其中的local包，*表示全部导入

# --------------------------------分析---------------------------------------
'''
对象：
一、飞机：
    移动速度:移动一次的元素数量
    攻击速度:攻击一次的子弹数量
    血量
    大小
    护甲(0~1)
    穿甲(0~1):最终伤害=原始伤害*[1-自身护甲*(1-对方穿甲)]
二、控制器：
   W向上
   S向下
   A向左
   D向右
   SPACE发射子弹
三、子弹：
   移动速度:每秒移动的速度
   威力
   大小
四、窗口：
   背景
   背景音乐
   特效
   飞机
   子弹
出局:
    玩家：
       1.被敌方子弹攻击后降低血量，血量<=0时出局
       2.与敌方飞机接触时出局
    敌方飞机：
       1.被我方子弹攻击后降低血量，血量<=0时出局
       2.飞出屏幕时出局
    子弹：
       1.与对方飞机接触时出局
       2.飞出屏幕时出局
'''

# 步骤：
# 1.创建窗口
'''
pygame库安装
   安装命令(cmd中)：
      pip install pygame
在当前项目添加pygame
   在pycharm终端的venv环境输入pip install pygame
'''


# 2.创建双方飞机
# -----------------------------创建对象---------------------------
class Bullet:
    def __init__(self, dir, screen, image_path, x, y, damage=10, mv_spd=1, size_x=10, size_y=10):
        '''

        :param dir:方向 >=0表示向下，<0表示向上
        :param screen:窗口对象
        :param damage: 威力
        :param image_path: 图像路径
        :param x:
        :param y: 坐标
        :param mv_spd:移动速度
        :param size_x:
        :param size_y: 大小
        '''
        self.dir = dir
        self.screen = screen
        self.damage = damage
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (size_x, size_y))
        self.x = x
        self.y = y
        self.mv_spd = mv_spd
        self.size_x = size_x
        self.size_y = size_y
        pass

    def move(self):
        '''

        :return: 是否出局
        '''
        if self.y >= self.screen.get_size()[1] or self.y - self.size_y <= 0:
            return True

        if self.dir >= 0:
            self.y += self.mv_spd
            pass
        else:
            self.y -= self.mv_spd
            pass

        return False

    def show(self):
        self.screen.blit(self.image, (self.x, self.y))
        pass

    pass


class Plane:

    def __init__(self, screen, image_path, bullet_im_path, blood=100, armor=0, pntra=0, mv_spd=15, att_spd=1, size_x=80,
                 size_y=80):
        '''

        :param bullet_im_path:子弹图像路径
        :param screen:屏幕对象
        :param image_path: 图像路径
        :param blood: 血量
        :param armor: 护甲
        :param pntra: 穿甲
        :param mv_spd: 移动速度
        :param att_spd: 攻击速度
        :param size_x:
        :param size_y: 大小
        '''
        self.b_i_p = bullet_im_path
        self.screen = screen
        self.x = screen.get_size()[0] // 2 - size_x // 2
        self.y = screen.get_size()[1] - size_y  # 坐标
        image = pygame.image.load(image_path)  # 创建玩家图片对象
        self.image = pygame.transform.scale(image, (size_x, size_y))  # 设置玩家图片的大小
        self.blood = blood
        self.armor = armor
        self.pntra = pntra
        self.mv_spd = mv_spd
        self.att_spd = att_spd
        self.size_x = size_x
        self.size_y = size_y

        pass

    def set_damage_image(self, path):
        image = pygame.image.load(path)
        self.d_im = pygame.transform.scale(image, (self.size_x, self.size_y))
        pass

    def damage(self, bullet):
        '''
        收到攻击
        :param bullet: 对方子弹
        :return: 血量是否<=0
        '''
        self.blood -= bullet.damage

        if self.blood <= 0:
            return True
        self.d_im = pygame.transform.scale(self.d_im, (bullet.size_x * 2, bullet.size_y * 2))

        return False

    def show(self):
        self.screen.blit(self.image, (self.x, self.y))
        pass

    # --------------移动--------------------
    def mv_left(self):
        if self.x - self.mv_spd > 0:
            self.x -= self.mv_spd
            pass
        else:
            self.x = 0
        pass

    def mv_right(self):
        if self.x + self.size_x + self.mv_spd < self.screen.get_size()[0]:  # 如果下次移动不会出去
            self.x += self.mv_spd
            pass
        else:
            self.x = self.screen.get_size()[0] - self.size_x
        pass

    def mv_up(self):
        if self.y - self.mv_spd > 0:
            self.y -= self.mv_spd
            pass
        else:
            self.y = 0
        pass

    def mv_down(self):
        if self.y + self.size_y + self.mv_spd < self.screen.get_size()[1]:
            self.y += self.mv_spd
            pass
        else:
            self.y = self.screen.get_size()[1] - self.size_y
        pass

    def attack(self):
        '''

        :return: 返回一个子弹对象
        '''
        return Bullet(-1, self.screen, self.b_i_p, self.x + self.size_x // 2, self.y)

    def move(self):

        for event in pygame.event.get():  # 获取事件列表,返回eventlist列表对象
            if event.type == QUIT:  # 如果QUIT,即窗口的关闭按钮
                sys.exit(0)
                pass
            elif event.type == KEYDOWN:  # 如果是按键

                if event.key == K_a:
                    self.mv_left()
                    pass
                elif event.key == K_w:
                    self.mv_up()
                    pass
                elif event.key == K_s:
                    self.mv_down()
                    pass
                elif event.key == K_d:
                    self.mv_right()
                    pass
                elif event.key == K_SPACE:
                    bullet = self.attack()  # 创建子弹
                    window.add_p_bullet(bullet)  # 将子弹添加到列表中
                    pass
                pass
            pass
        pass

    pass


class Enemy(Plane):

    def __init__(self, screen, image_path, bullet_im_path, boss=False, blood=10, armor=0, pntra=0, mv_spd=0.3,
                 att_spd=1, size_x=50,
                 size_y=50):
        '''
        :param boss:是否为boss
        :param bullet_im_path:子弹图像路径
        :param screen:屏幕对象
        :param image_path: 图像路径
        :param blood: 血量
        :param armor: 护甲
        :param pntra: 穿甲
        :param mv_spd: 移动速度
        :param att_spd: 攻击速度
        :param size_x:
        :param size_y: 大小
        '''
        super().__init__(screen, image_path, bullet_im_path, blood, armor, pntra, mv_spd, att_spd, size_x, size_y)
        self.y = 0
        self.boss = boss
        self.x = random.randint(0, screen.get_size()[0] - size_x)  # 随机生成位置
        pass

    def show_death(self):
        self.screen.blit(self.d_im, (self.x, self.y))

    def mv_down(self):
        self.y += self.mv_spd
        pass

    def attack(self):
        return Bullet(1, self.screen, self.b_i_p, self.x + self.size_x // 2, self.y + self.size_y)

    def move(self):
        '''

        :return: 是否出局
        '''
        a = random.randint(0, 500)  # 0.2%
        if a == 0:
            bullet = self.attack()
            window.add_e_bullet(bullet)
            pass
        if not self.boss:
            self.mv_down()
            if self.y >= self.screen.get_size()[1]:  # 到达边界就消失
                return True
            pass
        else:
            a = random.randint(0, self.screen.get_size()[0])
            if a >= self.x:
                self.mv_right()
                pass
            else:
                self.mv_left()
                pass
            pass
        return False

    pass


class Window:
    def __init__(self, scr_size, bg_path, bgm_path):
        '''
        初始化窗口
        :param scr_size: #屏幕大小
        :param bg: 背景图片路径
        :param bgm_path: 背景音乐路径
        '''
        self.score = 0  # 得分
        self.screen = pygame.display.set_mode(scr_size)  # 创建一个窗口对象screen，大小为600*800，用于显示内容
        self.bg = pygame.image.load(bg_path)  # 创建一个背景图片对象
        self.bg = pygame.transform.scale(self.bg, scr_size)  # 改变背景图片的大小
        self.enemies = []  # 敌方飞机列表
        self.e_bullets = []  # 敌方子弹列表
        self.p_bullets = []  # 玩家子弹列表
        pygame.display.set_caption('飞机大战')  # 设定窗口标题
        # -----背景音乐-----
        pygame.mixer.init()
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.set_volume(0.2)  # 设置音量
        pygame.mixer.music.play(-1)  # 设置循环次数，-1表示无限循环
        pass

    def set_player(self, player):
        self.player = player
        pass

    def add_enemy(self, enemy):  # 添加敌人
        self.enemies.append(enemy)
        pass

    def pop_enemy(self, enemy):  # 删除敌人
        self.enemies.remove(enemy)
        pass

    def add_e_bullet(self, e_bullet):
        self.e_bullets.append(e_bullet)
        pass

    def pop_e_bullet(self, e_bullet):
        self.e_bullets.remove(e_bullet)
        pass

    def add_p_bullet(self, p_bullet):
        self.p_bullets.append(p_bullet)
        pass

    def pop_p_bullet(self, p_bullet):
        self.p_bullets.remove(p_bullet)
        pass

    def create_enemies(self):
        a = random.randint(0, 1000)  # 0.1%
        if a == 0:
            enemy = Enemy(self.screen, './res/enemy2.png', './res/bullet2.png')
            enemy.set_damage_image('./res/enemy_explore.png')
            self.add_enemy(enemy)
            pass
        pass

    def move_all(self):  # 单位移动
        self.player.move()
        for enemy in self.enemies:
            if enemy.move():  # 如果出局
                self.pop_enemy(enemy)
                del enemy
                pass
            pass
        for e_bullet in self.e_bullets:
            if e_bullet.move():
                self.pop_e_bullet(e_bullet)
                del e_bullet
                pass
            pass
        for p_bullet in self.p_bullets:
            if p_bullet.move():
                self.pop_p_bullet(p_bullet)
                del p_bullet
                pass
            pass
        pass

    def logic(self):
        '''
        逻辑判断
        攻击
        受伤
        :return:
        '''

        for enemy in self.enemies:
            #     if is_inside(self.player.x, self.player.y, self.player.size_x, self.player.size_y, enemy.x, enemy.y,
            #                  enemy.size_x, enemy.size_y):  # 如果重合,则玩家死亡
            #         sys.exit(0)
            #         pass
            for p_bullet in self.p_bullets:
                if is_inside(p_bullet.x, p_bullet.y, p_bullet.size_x, p_bullet.size_y, enemy.x, enemy.y,
                             enemy.size_x, enemy.size_y):  # 若被子弹攻击到,则扣血
                    if enemy.damage(p_bullet):  # 若血量<=0
                        self.pop_enemy(enemy)
                        self.pop_p_bullet(p_bullet)
                        for i in range(10):
                            self.display()
                            enemy.show_death()
                            pygame.display.update()
                            pass
                        del enemy
                        del p_bullet
                        self.score += 10  # 加分
                        break
                        pass
                    pass
                pass

        for e_bullet in self.e_bullets:
            if is_inside(e_bullet.x, e_bullet.y, e_bullet.size_x, e_bullet.size_y, self.player.x, self.player.y,
                         self.player.size_x, self.player.size_y):  # 若被子弹攻击到,则扣血
                if self.player.damage(e_bullet):  # 若血量<=0
                    sys.exit(0)
                    pass
                self.pop_e_bullet(e_bullet)
                for i in range(10):
                    self.display()
                    self.screen.blit(self.player.d_im, (e_bullet.x, e_bullet.y))
                    pygame.display.update()
                    pass
                del e_bullet
                pass
            pass
        pass

    def output(self):  # 输出文字
        GREEN = (0, 255, 0)  # 设置颜色
        RED = (255, 0, 0)
        pygame.font.init()
        fontObj = pygame.font.Font('./res/simfang.ttf', 22)  # 新建一个font对象
        textSurface = fontObj.render('得分：' + str(self.score), True, RED)  # 新建一个surface对象
        textSurface1 = fontObj.render('血量：' + str(self.player.blood), True, RED)
        textRect = textSurface.get_rect()
        self.screen.blit(textSurface, (0, self.screen.get_size()[1] // 2))
        self.screen.blit(textSurface1, (0, self.screen.get_size()[1] // 2 + 22))

    def show_all(self):
        self.player.show()
        for item in self.enemies:
            item.show()
            pass
        for item in self.e_bullets:
            item.show()
            pass
        for item in self.p_bullets:
            item.show()
            pass

    def display(self):
        self.create_enemies()
        self.move_all()
        self.logic()
        self.screen.blit(self.bg, (0, 0))  # 设定显示背景图片
        self.output()
        # pygame.draw.rect(self.screen,0,((self.player.x,self.player.y),(self.player.size_x,self.player.size_y)))
        # if len(self.enemies)>0:
        #     pygame.draw.rect(self.screen,0,((self.enemies[0].x,self.enemies[0].y),(self.enemies[0].size_x,self.enemies[0].size_y)))

        self.show_all()

        pass

    pass


def is_inside(x1, y1, size_x1, size_y1, x2, y2, size_x2, size_y2):
    '''

    :param x1:
    :param y1:
    :param size_x1:
    :param size_y1:
    :param x2:
    :param y2:
    :param size_x2:
    :param size_y2:

    :return: 是否重合
    '''
    if x1 < x2 and x1 + size_x1 > x2 + size_x2:
        return True
    if x2 < x1 < x2 + size_x2 and y2 < y1 < y2 + size_y2:
        return True
    if x2 < x1 + size_x1 < x2 + size_x2 and y2 < y1 < y2 + size_y2:
        return True
    if x2 < x1 < x2 + size_x2 and y2 < y1 + size_y1 < y2 + size_y2:
        return True
    if x2 < x1 + size_x1 < x2 + size_x2 and y2 < y1 + size_y1 < y2 + size_y2:
        return True

    if x1 < x2 < x1 + size_x1 and y1 < y2 < y1 + size_y1:
        return True
    if x1 < x2 + size_x2 < x1 + size_x1 and y1 < y2 < y1 + size_y1:
        return True
    if x1 < x2 + size_x2 < x1 + size_x1 and y1 < y2 + size_y2 < y1 + size_y1:
        return True
    if x1 < x2 < x1 + size_x1 and y1 < y2 + size_y2 < y1 + size_y1:
        return True
    return False


# ----------------------------搭建界面---------------------------

scr_size = (600, 800)  # 屏幕大小
window = Window(scr_size, './res/planefight-bg.png', './res/张杰 - 天下.mp3')


def main():
    player = Plane(window.screen, './res/PaperPlane.png', './res/bullet2.png')  # 创建玩家飞机
    player.set_damage_image('./res/enemy_explore.png')
    window.set_player(player)
    while True:
        window.display()
        pygame.display.update()  # 更新显示的内容
    pass


# --------------------------------运行--------------------------------------
if __name__ == '__main__':
    main()
