import pygame as pg
from PyQt5.QtWidgets import QFileDialog
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import*

pg.init()


# 對話紀錄檔class
class Data():
    path = ''  # 檔案路徑
    system = ''  # 手機系統
    individual_group = ''  # 個人或群組聊天


# 跳視窗匯檔案class
class Window(QtWidgets.QWidget):
    def msg(self):
        # 限定匯入txt檔
        fileName, filetype = QFileDialog.getOpenFileName(self, "選取檔案", "./", "Text Files (*.txt)")

        return fileName


# 設定顏色
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 48, 48)
green = (34, 177, 76)
blue = (30, 144, 255)
dark = (170, 170, 170)
light = (100, 100, 100)

# 設定字體大小
small_font = pg.font.SysFont('appleligothicmedium', 20)
med_font = pg.font.SysFont('appleligothicmedium', 30)
large_font = pg.font.SysFont('appleligothicmedium', 50)

# 設定視窗
width, height = 800, 600
screen = pg.display.set_mode((width, height))
pg.display.set_caption('聊天資料分析')

# 建立畫布
bg = pg.Surface(screen.get_size())
bg = bg.convert()
bg.fill(white)


# 文字物件樣式
def text_objects(text, color, size):
    if size == 'small':
        textSurface = small_font.render(text, True, color)
    elif size == 'medium':
        textSurface = med_font.render(text, True, color)
    elif size == 'large':
        textSurface = large_font.render(text, True, color)

    return textSurface, textSurface.get_rect()


# 螢幕上印出文字「置中」
def message_to_screen_center(msg, color, y_displace=0, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (width / 2), (height / 2) + y_displace
    screen.blit(textSurf, textRect)  # 顯示


# 螢幕上印出文字「靠左對齊」
def message_to_screen_side(msg, color, x_displace=0, y_displace=0, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    screen.blit(textSurf, [x_displace, y_displace])  # 顯示


# 在 button 上的文字
def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size='small'):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = ((buttonx + (buttonwidth/2)), buttony + (buttonheight/2))
    screen.blit(textSurf, textRect)  # 顯示


# 按鈕組合
def button(text, x, y, width, height, inactive_color, active_color):
    mouse = pg.mouse.get_pos()  # 儲存滑鼠游標 (x,y) 位置

    # 若滑鼠在 button 上方就變顏色
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        button_rect = pg.draw.rect(screen, active_color, (x, y, width, height))
    else:
        button_rect = pg.draw.rect(screen, inactive_color, (x, y, width, height))

    text_to_button(text, black, x, y, width, height)
    return button_rect


# 匯入資料
def import_data():
    if __name__ == "__main__":
        app = QtWidgets.QApplication(sys.argv)
        myshow = Window()
        Data.path = myshow.msg()


# 個人頁面
def individual():
    back = False
    while not back:
        screen.fill(white)
        message_to_screen_side("個人頁面", green, 50, 50, 'medium')

        button_word = button("字數", 50, 100, 100, 50, dark, light)
        button_sentence = button("句數", 200, 100, 100, 50, dark, light)
        button_call = button("通話", 350, 100, 100, 50, dark, light)
        button_often = button("常用的字", 500, 100, 100, 50, dark, light)
        button_back = button("回首頁", 650, 100, 100, 50, dark, light)

        pg.display.update()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_word .collidepoint(ev.pos):
                    pass
                elif button_sentence .collidepoint(ev.pos):
                    pass
                elif button_call .collidepoint(ev.pos):
                    pass
                elif button_often .collidepoint(ev.pos):
                    pass
                elif button_back .collidepoint(ev.pos):
                    game_intro()


# 群組頁面
def group():
    back = False
    while not back:
        screen.fill(white)
        message_to_screen_side("群組頁面", green, 50, 50, 'medium')

        button_most = button("誰的話最多", 50, 100, 100, 50, dark, light)
        button_dot = button("句點王", 250, 100, 100, 50, dark, light)
        button_active = button("活躍時間", 450, 100, 100, 50, dark, light)
        button_back = button("回首頁", 650, 100, 100, 50, dark, light)

        pg.display.update()
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_most.collidepoint(ev.pos):
                    pass
                elif button_dot.collidepoint(ev.pos):
                    pass
                elif button_active.collidepoint(ev.pos):
                    pass
                elif button_back.collidepoint(ev.pos):
                    game_intro()


# 選擇手機系統、個人群組頁面
def choice():
    back = False
    while not back:
        screen.fill(white)
        message_to_screen_center("基本設定", black, -220, 'medium')
        message_to_screen_side('您手機的系統為：', black, 250, 150)
        message_to_screen_side('輸入的對話紀錄為：', black, 250, 350)
        if Data.system != '':
            message_to_screen_side(Data.system, blue, 450, 150)
        if Data.individual_group != '':
            message_to_screen_side(Data.individual_group, blue, 450, 350)

        button_android = button("android", 250, 200, 100, 50, dark, light)
        button_ios = button("ios", 450, 200, 100, 50, dark, light)
        button_individual = button("個人聊天", 250, 400, 100, 50, dark, light)
        button_group = button("群組聊天", 450, 400, 100, 50, dark, light)
        button_back = button("回首頁", 50, 500, 100, 50, dark, light)
        button_start = button("開始分析", 650, 500, 100, 50, dark, light)

        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_ios.collidepoint(ev.pos):  # 按下ios
                    Data.system = 'ios'

                elif button_android.collidepoint(ev.pos):  # 按下android
                    Data.system = 'android'

                elif button_individual.collidepoint(ev.pos):  # 按下個人聊天
                    Data.individual_group = '個人聊天'

                elif button_group.collidepoint(ev.pos):  # 按下群組聊天
                    Data.individual_group = '群組聊天'

                elif button_back.collidepoint(ev.pos):  # 按下回首頁
                    game_intro()

                elif button_start.collidepoint(ev.pos):  # 開始分析
                    if Data.individual_group != '' and Data.system != '':
                        if Data.individual_group == '個人聊天':
                            individual()
                        elif Data.individual_group == '群組聊天':
                            group()


# 遊戲首頁
def game_intro():
    intro = True
    while intro:

        screen.fill(white)
        message_to_screen_center("歡迎來到遊戲", blue, -220, 'large')
        message_to_screen_center("使用說明", black, -130, 'medium')
        message_to_screen_center("請先確認您的手機為「24小時制」且為「中文版本」", red, -90)
        message_to_screen_center("再由「手機的line」匯出對話紀錄 txt.檔並儲存至您的電腦", black, -60)
        message_to_screen_center("點選「匯入資料」匯入您的對話紀錄，並根據手機系統點選「android」或「ios」", black, -30)
        message_to_screen_center("依據您的對話紀錄點選「個人聊天」或是「群組聊天」", black, 0)
        message_to_screen_center("就會進入對話紀錄分析的頁面囉！", black, 30)
        if Data.path == '':
            message_to_screen_center('*** 請匯入資料 ***', green, 150)
        else:
            message_to_screen_center('資料路徑：' + Data.path, light, 150)

        button_import = button("匯入資料", 350, 365, 100, 50, dark, light)
        button_quit = button("離開", 200, 500, 100, 50, dark, light)
        button_next = button("下一頁", 500, 500, 100, 50, dark, light)

        pg.display.update()

        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                quit()
            if ev.type == pg.MOUSEBUTTONDOWN:
                # If the button collides with the mouse position.
                if button_import .collidepoint(ev.pos):
                    import_data()  # 匯入資料
                    print(Data.path)  # 檔案路徑 Data.path

                elif button_next.collidepoint(ev.pos):
                    if Data.path != '':  # 有路徑才能按下一頁
                        choice()

                elif button_quit.collidepoint(ev.pos):
                    pg.quit()
                    quit()


game_intro()

# 關閉
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:  # 使用者按右上角的關閉鈕
            running = False

pg.quit()  # 關閉繪圖視窗
quit()
